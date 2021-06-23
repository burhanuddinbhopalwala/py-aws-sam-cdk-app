# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_cloudfront as cdn
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class CDNStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, s3bucket, acmcert, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        bucketName = s3.Bucket.from_bucket_name(self, 's3bucket', s3bucket)

        self.cdn_id = cdn.CloudFrontWebDistribution(self, 'webhosting-cdn',
                                                    origin_configs=[cdn.SourceConfiguration(
                                                        behaviors=[
                                                            cdn.Behavior(
                                                                is_default_behavior=True)
                                                        ],
                                                        origin_path='/build',
                                                        s3_origin_source=cdn.S3OriginConfig(
                                                            s3_bucket_source=bucketName,
                                                            origin_access_identity=cdn.OriginAccessIdentity(
                                                                self, 'webhosting-origin')
                                                        )

                                                    )],
                                                    error_configurations=[cdn.CfnDistribution.CustomErrorResponseProperty(
                                                        error_code=400,
                                                        response_code=200,
                                                        response_page_path='/'

                                                    ),
                                                        cdn.CfnDistribution.CustomErrorResponseProperty(
                                                        error_code=403,
                                                        response_code=200,
                                                        response_page_path='/'
                                                    ),
                                                        cdn.CfnDistribution.CustomErrorResponseProperty(
                                                        error_code=404,
                                                        response_code=200,
                                                        response_page_path='/'
                                                    )
                                                    ],
                                                    alias_configuration=cdn.AliasConfiguration(
                                                        acm_cert_ref=acmcert.certificate_arn,
                                                        names=[
                                                            'app.cloudevangelist.ca']
                                                    )

                                                    )

        ssm.StringParameter(self, 'cdn-dist-id',
                            parameter_name='/'+env_name+'/app-distribution-id',
                            string_value=self.cdn_id.distribution_id
                            )

        ssm.StringParameter(self, 'cdn-url',
                            parameter_name='/'+env_name+'/app-cdn-url',
                            string_value='https://'+self.cdn_id.domain_name
                            )
