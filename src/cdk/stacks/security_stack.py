# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class SecurityStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        self.lambda_sg = ec2.SecurityGroup(self, 'lambdasg',
                                           security_group_name='lambda-sg',
                                           vpc=vpc,
                                           description='SG for Lambda Functions',
                                           allow_all_outbound=True
                                           )

        self.bastion_sg = ec2.SecurityGroup(self, 'bastionsg',
                                            security_group_name='bastion-sg',
                                            vpc=vpc,
                                            description='SG for Bastion Host',
                                            allow_all_outbound=True
                                            )

        self.bastion_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), 'SSH Access')

        redis_sg = ec2.SecurityGroup(self, 'redissg',
                                     security_group_name='redis-sg',
                                     vpc=vpc,
                                     description='SG for Redis Cluster',
                                     allow_all_outbound=True
                                     )
        redis_sg.add_ingress_rule(self.lambda_sg, ec2.Port.tcp(
            6379), 'Access from Lambda functions')

        # Kibana
        self.kibana_sg = ec2.SecurityGroup(self, 'kibanasg',
                                           security_group_name='kibana-sg',
                                           vpc=vpc,
                                           description='SG for Kibana',
                                           allow_all_outbound=True
                                           )
        self.kibana_sg.add_ingress_rule(
            self.bastion_sg, ec2.Port.tcp(443), 'Access from jumpbox')

        kibana_role = iam.CfnServiceLinkedRole(self, 'kibanarole',
                                               aws_service_name='es.amazonaws.com'
                                               )

        lambda_role = iam.Role(self, 'lambdarole',
                               assumed_by=iam.ServicePrincipal(
                                   service='lambda.amazonaws.com'),
                               role_name='lambda-role',
                               managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                   managed_policy_name='service-role/AWSLambdaVPCAccessExecutionRole'
                               )]
                               )

        lambda_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=['s3:*', 'rds:*'],
                resources=['*']
            )
        )

        core.CfnOutput(self, 'redis-export',
                       export_name='redis-sg-export',
                       value=redis_sg.security_group_id
                       )
        # SSM Parameters
        ssm.StringParameter(self, 'lambdasg-param',
                            parameter_name='/'+env_name+'/lambda-sg',
                            string_value=self.lambda_sg.security_group_id
                            )

        ssm.StringParameter(self, 'lambdarole-param-arn',
                            parameter_name='/'+env_name+'/lambda-role-arn',
                            string_value=lambda_role.role_arn
                            )
        ssm.StringParameter(self, 'lambdarole-param-name',
                            parameter_name='/'+env_name+'/lambda-role-name',
                            string_value=lambda_role.role_name
                            )
