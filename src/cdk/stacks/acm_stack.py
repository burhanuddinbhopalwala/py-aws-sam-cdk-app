# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cdn
from aws_cdk import aws_iam as iam
from aws_cdk import aws_route53 as r53
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class ACMStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        zone_id = ssm.StringParameter.from_string_parameter_name(
            self, 'zone-id-ssm', string_parameter_name='/'+env_name+'/zone-id')

        dns_zone = r53.HostedZone.from_hosted_zone_attributes(self, 'hosted-zone',
                                                              hosted_zone_id=zone_id.string_value,
                                                              zone_name='cloudevangelist.ca'
                                                              )

        self.cert_manager = acm.DnsValidatedCertificate(self, 'acm-id',
                                                        hosted_zone=dns_zone,
                                                        domain_name='cloudevangelist.ca',
                                                        subject_alternative_names=[
                                                            '*.cloudevangelist.ca']
                                                        )
