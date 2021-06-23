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


class BastionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bastion_host = ec2.Instance(self, 'bastion-host',
                                    instance_type=ec2.InstanceType('t2.micro'),
                                    machine_image=ec2.AmazonLinuxImage(
                                        edition=ec2.AmazonLinuxEdition.STANDARD,
                                        generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                        virtualization=ec2.AmazonLinuxVirt.HVM,
                                        storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                    ),
                                    vpc=vpc,
                                    key_name='devops',
                                    vpc_subnets=ec2.SubnetSelection(
                                        subnet_type=ec2.SubnetType.PUBLIC
                                    ),
                                    security_group=sg
                                    )
