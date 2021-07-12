# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import logging
import os

import boto3
# TODO: Xray recorder dec

ENV = os.environ.get('ENV', 'development')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')

handle = 's3_athena_auto_load'
logger = logging.getLogger(handle)
logger.setLevel(LOG_LEVEL)

athena_client = boto3.client('athena', region_name=AWS_REGION)

S3_BUCKET_NAME = 'gts-pings-logs'
ATHENA_DATABASE_NAME = 'default'
ATHENA_PULL_TABLE_NAME = 'fareye_3pl_pull_track_logs'
ATHENA_PUSH_TABLE_NAME = 'fareye_3pl_push_track_logs'


def lambda_handler(event, context):
    """@desc Athena auto load paritioning - main function."""
    try:
        result_config = {
            'OutputLocation': 's3://' + S3_BUCKET_NAME + '/athena-query-results/',
            'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}}
        # * Query exec parameters
        pull_table_sql = 'MSCK REPAIR TABLE {}.{}'.format(
            ATHENA_DATABASE_NAME, ATHENA_PULL_TABLE_NAME)
        push_table_sql = 'MSCK REPAIR TABLE {}.{}'.format(
            ATHENA_DATABASE_NAME, ATHENA_PUSH_TABLE_NAME)
        query_exec_context = {'Database': ATHENA_DATABASE_NAME}
        logger.info(result_config)
        logger.info(pull_table_sql, push_table_sql)
        logger.info(query_exec_context)

        athena_client.start_query_execution(
            QueryString=pull_table_sql,
            QueryExecutionContext=query_exec_context,
            ResultConfiguration=result_config)
        athena_client.start_query_execution(
            QueryString=push_table_sql,
            QueryExecutionContext=query_exec_context,
            ResultConfiguration=result_config)
    except Exception as e:
        logger.exception('## EXCEPTION %s', e)
        raise e

# * Unit test
# lambda_handler({}, {})
