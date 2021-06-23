# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        account_id = core.Aws.ACCOUNT_ID
        lambda_bucket = s3.Bucket(self, 'lambda-bucket',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  bucket_name=account_id+'-'+env_name+'-lambda-deploy-packages',
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  removal_policy=core.RemovalPolicy.RETAIN
                                  )

        ssm.StringParameter(self, 'ssm-lambda-bucket',
                            parameter_name='/'+env_name+'/lambda-s3-bucket',
                            string_value=lambda_bucket.bucket_name
                            )

        # To Store Build Artifacts

        artifacts_bucket = s3.Bucket(self, 'build-artifacts',
                                     access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                     encryption=s3.BucketEncryption.S3_MANAGED,
                                     bucket_name=account_id+'-'+env_name+'-build-artifacts',
                                     block_public_access=s3.BlockPublicAccess(
                                         block_public_acls=True,
                                         block_public_policy=True,
                                         ignore_public_acls=True,
                                         restrict_public_buckets=True
                                     ),
                                     removal_policy=core.RemovalPolicy.DESTROY
                                     )

        core.CfnOutput(self, 's3-build-artifacts-export',
                       value=artifacts_bucket.bucket_name,
                       export_name='build-artifacts-bucket'
                       )

        # To Store Frontend App

        frontend_bucket = s3.Bucket(self, 'frontend',
                                    access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                    encryption=s3.BucketEncryption.S3_MANAGED,
                                    bucket_name=account_id+'-'+env_name+'-frontend',
                                    block_public_access=s3.BlockPublicAccess(
                                        block_public_acls=True,
                                        block_public_policy=True,
                                        ignore_public_acls=True,
                                        restrict_public_buckets=True
                                    )

                                    )

        core.CfnOutput(self, 's3-frontend-export',
                       value=frontend_bucket.bucket_name,
                       export_name='frontend-bucket'
                       )

        # CloudTrail Bucket

        self.cloudtrail_bucket = s3.Bucket(self, 'cloudtrail',
                                           access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                           encryption=s3.BucketEncryption.S3_MANAGED,
                                           bucket_name=account_id+'-'+env_name+'-cloudtrail',
                                           block_public_access=s3.BlockPublicAccess(
                                               block_public_acls=True,
                                               block_public_policy=True,
                                               ignore_public_acls=True,
                                               restrict_public_buckets=True
                                           )

                                           )
