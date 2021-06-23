# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        self.vpc = ec2.Vpc(self, 'devVPC',
                           cidr='172.32.0.0/16',
                           max_azs=2,
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name='Public',
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name='Private',
                                   subnet_type=ec2.SubnetType.PRIVATE,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name='Isolated',
                                   subnet_type=ec2.SubnetType.ISOLATED,
                                   cidr_mask=24
                               )
                           ],
                           nat_gateways=1
                           )

        priv_subnets = [
            subnet.subnet_id for subnet in self.vpc.private_subnets]

        count = 1
        for ps in priv_subnets:
            ssm.StringParameter(self, 'private-subnet-'+str(count),
                                string_value=ps,
                                parameter_name='/'+env_name +
                                '/private-subnet-'+str(count)
                                )
            count += 1
