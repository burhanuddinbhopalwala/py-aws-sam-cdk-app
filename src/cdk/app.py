#!/usr/bin/env python3
# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import core

from stacks.acm_stack import ACMStack
from stacks.apigw_stack import APIStack
from stacks.bastion_stack import BastionStack
from stacks.cdn_stack import CDNStack
from stacks.cloudtrail_stack import CloudTrailStack
from stacks.codepipeline_backend import CodePipelineBackendStack
from stacks.codepipeline_frontend import CodePipelineFrontendStack
from stacks.cognito_stack import CognitoStack
from stacks.kibana_stack import KibanaStack
from stacks.kms_stack import KMSStack
from stacks.lambda_stack import LambdaStack
from stacks.notifications import NotificationStack
from stacks.rds_stack import RDSStack
from stacks.redis_stack import RedisStack
from stacks.route53_stack import DnsStack
from stacks.s3_stack import S3Stack
from stacks.security_stack import SecurityStack
from stacks.vpc_stack import VPCStack
from stacks.waf_stack import WafStack

app = core.App()

vpc_stack = VPCStack(app, 'vpc')
security_stack = SecurityStack(app, 'security-stack', vpc=vpc_stack.vpc)
bastion_stack = BastionStack(
    app, 'bastion', vpc=vpc_stack.vpc, sg=security_stack.bastion_sg)
kms_stack = KMSStack(app, 'kms')
s3_stack = S3Stack(app, 's3buckets')
rds_stack = RDSStack(app, 'rds', vpc=vpc_stack.vpc, lambdasg=security_stack.lambda_sg,
                     bastionsg=security_stack.bastion_sg, kmskey=kms_stack.kms_rds)
redis_stack = RedisStack(app, 'redis', vpc=vpc_stack.vpc,
                         redissg=core.Fn.import_value('redis-sg-export'))
cognito_stack = CognitoStack(app, 'cognito')
apigw_stack = APIStack(app, 'apigw')
lambda_stack = LambdaStack(app, 'lambda')
cp_backend = CodePipelineBackendStack(
    app, 'cp-backend', artifactbucket=core.Fn.import_value('build-artifacts-bucket'))
notification = NotificationStack(app, 'notification')
cp_frontend = CodePipelineFrontendStack(
    app, 'cp-frontend', webhostingbucket=core.Fn.import_value('frontend-bucket'))
waf_stack = WafStack(app, 'waf')
acm_stack = ACMStack(app, 'acm')
cdn_stack = CDNStack(app, 'cdn', s3bucket=core.Fn.import_value(
    'frontend-bucket'), acmcert=acm_stack.cert_manager)
route53 = DnsStack(app, 'route53', cdnid=cdn_stack.cdn_id)
cloudtrail = CloudTrailStack(
    app, 'cloudtrail', s3bucket=s3_stack.cloudtrail_bucket)
kibana = KibanaStack(app, 'kibana', vpc=vpc_stack.vpc,
                     kibanasg=security_stack.kibana_sg)

app.synth()
