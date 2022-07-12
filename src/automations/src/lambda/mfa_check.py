# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import logging
import os
from datetime import datetime

import boto3

# * Fetching default env vars
ENV = os.environ.get('ENV', 'development')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# * Fetching custom env vars
SNS_ARN = os.environ.get(
    'SNS_ARN', 'arn:aws:sns:us-east-1:551596986909:SecOps-testing')

# * Enabling logging
handler = 'mfa_check'
logger = logging.getLogger(handler)
logger.setLevel(LOG_LEVEL.upper())

# * Creating service clients using default session
iam_client = boto3.client('iam', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)

EXCEPTION_LIST = ['github-ci-cd',
                  'github-deploy',
                  'github-actions',
                  'github-actions-2']

def lambda_handler(context, event):
    """@desc MFA check lambda handler - main function."""
    try:
        response = iam_client.list_users()
        user_virtual_mfa = iam_client.list_virtual_mfa_devices()

        virtual_enabled = []
        mfa_not_enabled = []
        sns_message = ''

        # * Loop through virtual mfa to find users that actually have it
        for virtual in user_virtual_mfa['VirtualMFADevices']:
            virtual_enabled.append(virtual['User']['UserId'])

        # * Loop through users to find physical MFA
        for user in response['Users']:
            user_mfa = iam_client.list_mfa_devices(UserName=user['UserName'])

            if len(user_mfa['MFADevices']) == 0:
                if user['UserId'] not in virtual_enabled:
                    mfa_not_enabled.append(user['UserName'])

        # * Filtering from EXCEPTION_LIST
        mfa_not_enabled = list(set(mfa_not_enabled) - set(EXCEPTION_LIST))

        # * MfA user filtering
        if len(mfa_not_enabled) > 0:
            sns_message = 'Physical & Virtual MFA is not enabled for the following users: \n\n' + \
                '\n'.join(mfa_not_enabled)

            date = datetime.now().strftime('%d-%b-%Y')
            sns_subject = 'MFA Status AWS {} - {}'.format(ENV, date)

            # * Sending notification
            response = sns_client.publish(
                TopicArn=SNS_ARN,
                Subject=sns_subject,
                Message=sns_message
            )
        else:
            sns_message = 'All Users have Physical and Virtual MFA enabled'

        logger.info(mfa_not_enabled)
        return mfa_not_enabled
    except Exception as e:
        logger.exception('## EXCEPTION %s', e)
        raise e


# * Unit test
# lambda_handler({}, {})
