# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticsearch as es
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class KibanaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, kibanasg, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        subnets = [subnet.subnet_id for subnet in vpc.private_subnets]

        es_domain = es.CfnDomain(self, 'esdomain',
                                 domain_name=prj_name+'-'+env_name+'-domain',
                                 elasticsearch_cluster_config=es.CfnDomain.ElasticsearchClusterConfigProperty(
                                     dedicated_master_enabled=False,
                                     instance_count=1,
                                     instance_type='t2.small.elasticsearch'
                                 ),
                                 ebs_options=es.CfnDomain.EBSOptionsProperty(
                                     ebs_enabled=True,
                                     volume_type='gp2',
                                     volume_size=10
                                 ),
                                 vpc_options=es.CfnDomain.VPCOptionsProperty(
                                     security_group_ids=[
                                         kibanasg.security_group_id],
                                     subnet_ids=[subnets.pop()]

                                 ),
                                 elasticsearch_version='7.4'

                                 )
        es_domain.access_policies = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Principal': {
                        'AWS': '*'
                    },
                    'Action': 'es:*',
                    'Resource': '*'
                }
            ]
        }
