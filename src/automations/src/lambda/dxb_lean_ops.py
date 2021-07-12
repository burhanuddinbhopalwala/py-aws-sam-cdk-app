# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import base64
import json
import logging
import os

import boto3
import pandas as pd
import pg8000 as dbapi
from botocore.exceptions import ClientError

ENV = os.environ.get('ENV', 'dev')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-1')

SNS_ARN = os.environ.get('SNS_ARN')
SECRET_ID = os.environ.get('SECRET_ID')

handler = 'dxb_lean_ops_lambda'
logger = logging.getLogger(handler)
logger.setLevel(LOG_LEVEL.upper())

session = boto3.session.Session()
ssm_client = session.client(
    service_name='secretsmanager', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)


def sns_publish(message) -> None:
    """@desc Publish to SNS topic."""
    try:
        sns_client.publish(
            TargetArn=SNS_ARN,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
    except Exception as e:
        raise e


def post_to_sns_details(message) -> None:
    """@desc Prepare message to publish to SNS."""
    try:
        message = {'DXB Lean Ops': message}
        sns_publish(message)
    except ClientError as e:
        raise e


def get_secret(secret_id):
    """@desc Getting SSM secret."""
    try:
        get_secret_value_response = ssm_client.get_secret_value(
            SecretId=secret_id)
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(
                get_secret_value_response['SecretBinary'])
        return json.loads(secret)


def get_redshift_conn():
    """@desc Getting prod Redshift conn."""
    try:
        conn = None
        secret = get_secret(SECRET_ID)
        print('>>>>>>', secret)
        conn = dbapi.connect(database=secret['database'], host=secret['host'],
                             port=secret['port'], user=secret['username'],
                             password=secret['password'])
        return conn
    except Exception as e:
        raise e


def execute_redshift_query(query, conn=get_redshift_conn()):
    """@desc Exec SQL on Redshift."""
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        raise e


def lambda_handler(event, context):
    """@desc DXB lean ops - main function."""
    try:
        ct_sql = """
        WITH
        -- STAGE 1: FIND ALL NON-FINALIZED SHIPMENTS
        open_awbs as (
        select awbs.id, awbs.awb, awbs.origin, awbs.destination, awbs.origin_country, awbs.dest_country, awbs.dest_city, awbs.dest_state,
            awbs.product_group, awbs.type, awbs.pickup_date as pu_date, aa.origin_received_status_action_date as or_date, di.scheduleddate
        from public.awbs as awbs

        inner join public.awbs_analysis as aa
        on awbs.id = aa.awb_id

        left join public.awbs_delivery_info as di
        on awbs.id = di.shipmentid
        and di.scheduleddate IS NOT NULL
        and di.scheduleddate <> '1900-01-01'

        where awbs.destination='DXB'
        and awbs.skeleton = False
        and NOT (aa.final_status_pi_number is not null)
        and awbs.product_group='EXP'
        --and aa.origin_received_status_action_date >= '2020/10/01'
        and DATEDIFF(month, CURRENT_DATE, awbs.pickup_date) BETWEEN -5 and 1

        ),

        -- STAGE 2: MAP COMPANIES TO COUNTRIES AND RETRIEVE TIME ZONE DETAILS
        cmp_vs_cn as (
        select cmp.id, cmp.code, cmp.country_code, cmp.time_zone, cn.timezone
        from public.companies as cmp
        inner join public.countries as cn
        on cmp.country_code = cn.code
        ),

        -- STAGE 3: RETREIVE CONSOL DETAILS FOR ALL OPEN SHIPMENTS. CONVERT TIMESTAMPS TO UTC.
        consols_tmp as (
        select oa.id, oa.origin, oa.destination, oa.origin_country, oa.dest_country,
        cva.consol_id, c.origin_entity, c.dest_entity, c.flt_1_etd, c.net_eta,
        cvc_1.country_code as origin_consol_country,
        cvc_2.country_code as dest_consol_country,
        cvc_1.time_zone as origin_cmp_tz,
        cvc_1.timezone as origin_cn_tz,
        cvc_2.time_zone as dest_cmp_tz,
        cvc_2.timezone as dest_cn_tz,
        DATEADD(hour, CAST(case nvl("origin_cmp_tz","origin_cn_tz",0) when 0 THEN 0 ELSE nvl("origin_cmp_tz","origin_cn_tz") end as integer)*-1, oa.pu_date) as pu_date_utc,
        DATEADD(hour, CAST(case nvl("origin_cmp_tz","origin_cn_tz",0) when 0 THEN 0 ELSE nvl("origin_cmp_tz","origin_cn_tz") end as integer)*-1, oa.or_date) as or_date_utc,
        DATEADD(hour, CAST(case nvl("origin_cmp_tz","origin_cn_tz",0) when 0 THEN 0 ELSE nvl("origin_cmp_tz","origin_cn_tz") end as integer)*-1, flt_1_etd) as flt_1_etd_utc,
        DATEADD(hour, CAST(case nvl("dest_cmp_tz","dest_cn_tz",0) when 0 THEN 0 ELSE nvl("dest_cmp_tz","dest_cn_tz") end as integer)*-1, net_eta) as net_eta_utc

        from open_awbs as oa
        inner join public.consols_vs_awbs as cva
        on oa.id = cva.awb_id
        inner join public.consols as c
        on cva.consol_id = c.id
        inner join cmp_vs_cn as cvc_1
        on c.origin_entity = cvc_1.id
        inner join cmp_vs_cn as cvc_2
        on c.dest_entity = cvc_2.id

        WHERE   c.origin_entity <> c.dest_entity
        AND   c.recovery_not_required = 0
        AND   c.airline <> '99'
        AND   c.product_group = 'EXP'
        ),


        -- STAGE 4: GET ORIGIN ETD TIME (from 1st origin consol)
        get_first_origin_consol as (
        select id, consol_id, flt_1_etd_utc, rank_id
        from (select ctmp.*, RANK() OVER(PARTITION BY ctmp.id ORDER BY ctmp.consol_id ASC) as rank_id from consols_tmp as ctmp
                where origin_country = origin_consol_country)
        where rank_id = 1
        ),


        -- STAGE 5: GET DEST ETA TIME (from 1st destination consol))
        get_first_dest_consol as (
        select id, consol_id, net_eta_utc, rank_id
        from (select ctmp.*, RANK() OVER(PARTITION BY ctmp.id ORDER BY ctmp.consol_id ASC) as rank_id from consols_tmp as ctmp
                where dest_country = dest_consol_country)
        where rank_id = 1
        ),


        -- STAGE 6: GET BRANCH FROM CALCULATED ROUTE
        get_SH523 AS (
        select temp.id, temp.pi_number, temp.comments_1, temp.action_date, temp.rank_id, r.routecode, b.id as branch_id, b.name as branch_name
            from(select oa.*, hist.pi_number, hist.action_date, hist.comments_1, RANK() OVER(PARTITION BY oa.id ORDER BY hist.ts DESC) as rank_id
                from open_awbs as oa
                    inner join public.awbs_history as hist
                    on oa.id = hist.hawb_id
                where hist.pi_number = 'SH523') as temp

                inner join public.routes as r
                on temp.comments_1 = r.routecode

                inner join public.branches as b
                on r.branchid = b.id

        where rank_id = 1
        --and NULLIF(comments_1, '') IS NOT NULL
        ),


        -- STAGE 7: GET 1ST AND LAST DESTINATION INBOUND BRANCH DETAIL
        get_dest_SH001 AS (

        select DISTINCT id, first_inbound_branch, last_inbound_branch
            FROM (
                select oa.id, hist.entity_id, hist.branch_id, b.name as branch_name,
                    FIRST_VALUE(b.name) OVER(PARTITION BY oa.id
                                            ORDER BY hist.ts ASC
                                            ROWS between unbounded preceding and unbounded following) as first_inbound_branch,
                    LAST_VALUE(b.name) OVER(PARTITION BY oa.id
                                            ORDER BY hist.ts ASC
                                            ROWS between unbounded preceding and unbounded following) as last_inbound_branch
                    FROM open_awbs as oa
                        inner join public.awbs_history as hist
                        on oa.id = hist.hawb_id
                        and hist.pi_number IN ('SH001', 'SH253', 'SH489')

                        inner join public.companies as c
                        on hist.entity_id = c.id
                        and oa.dest_country = c.country_code

                        inner join public.branches as b
                        on hist.branch_id = b.id
                )
        )

        -- STAGE 8: PUTTING EVERYTHING TOGETHER
        select
        oa.*,
        foc.flt_1_etd_utc AS first_origin_consol_utc,
        fdc.net_eta_utc AS first_dest_consol_utc,
        b.routecode as route_code, b.branch_id as calc_branch_id, COALESCE(b.branch_name, 'Aramex Umm Ramool') as calc_branch_name,
        c.first_inbound_branch, c.last_inbound_branch,
        CASE WHEN ((c.last_inbound_branch IS NOT NULL) AND (c.last_inbound_branch <> 'Dubai Express Hub')) THEN 'Outstanding'
            WHEN ((c.last_inbound_branch = 'Dubai Express Hub') OR (first_dest_consol_utc IS NOT NULL)) THEN 'In Transit'
            WHEN (CURRENT_TIME > first_origin_consol_utc) THEN 'In Transit or At Origin'
            ELSE 'At Origin' END AS shipment_status,
        COALESCE(oa.scheduleddate, DATE_TRUNC('day', first_dest_consol_utc)) as forecast_date,
        CASE WHEN forecast_date = CURRENT_DATE THEN 1 ELSE 0 END as DAY_0,
        CASE WHEN forecast_date = DATEADD(day, 1, CURRENT_DATE) THEN 1 ELSE 0 END as DAY_1,
        CASE WHEN forecast_date = DATEADD(day, 2, CURRENT_DATE) THEN 1 ELSE 0 END as DAY_2,
        CASE WHEN forecast_date = DATEADD(day, 3, CURRENT_DATE) THEN 1 ELSE 0 END as DAY_3

        from open_awbs as oa
            left join get_first_origin_consol as foc
            on oa.id = foc.id

            left join get_first_dest_consol as fdc
            on oa.id = fdc.id

            left join get_SH523 as b
            on oa.id = b.id

            left join get_dest_SH001 as c
            on oa.id = c.id

        ;
        """
        payload = execute_redshift_query(ct_sql).to_json()
        payload_dict = {'payload': payload}
        post_to_sns_details(payload_dict)
        return payload_dict
    except Exception as e:
        logger.exception('## EXCEPTION %s', e)
        raise e

# * Unit test
# lambda_handler({}, {})
