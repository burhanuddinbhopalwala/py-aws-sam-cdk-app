# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class CognitoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        user_pool = cognito.CfnUserPool(self, 'cognitouserpool',
                                        auto_verified_attributes=[
                                            'email'
                                        ],
                                        username_attributes=[
                                            'email', 'phone_number'
                                        ],
                                        user_pool_name=prj_name+'-user-pool',
                                        schema=[
                                            {
                                                'attributeDataType': 'String',
                                                'name': 'param1',
                                                'mutable': True
                                            }
                                        ],
                                        policies=cognito.CfnUserPool.PoliciesProperty(
                                            password_policy=cognito.CfnUserPool.PasswordPolicyProperty(
                                                minimum_length=10,
                                                require_lowercase=True,
                                                require_numbers=True,
                                                require_symbols=False,
                                                require_uppercase=True
                                            )
                                        )
                                        )

        user_pool_client = cognito.CfnUserPoolClient(self, 'pool-client',
                                                     user_pool_id=user_pool.ref,
                                                     client_name=env_name+'-app-client'
                                                     )

        identity_pool = cognito.CfnIdentityPool(self, 'identitypool',
                                                allow_unauthenticated_identities=False,
                                                cognito_identity_providers=[
                                                    cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                                                        client_id=user_pool_client.ref,
                                                        provider_name=user_pool.attr_provider_name
                                                    )
                                                ],
                                                identity_pool_name=prj_name+'-identity-pool'
                                                )

        ssm.StringParameter(self, 'app-id',
                            parameter_name='/'+env_name+'/cognito-app-client-id',
                            string_value=user_pool_client.ref
                            )

        ssm.StringParameter(self, 'user-pool-id',
                            parameter_name='/'+env_name+'/cognito-user-pool-id',
                            string_value=user_pool_client.user_pool_id
                            )

        ssm.StringParameter(self, 'identity-pool-id',
                            parameter_name='/'+env_name+'/cognito-identity-pool-id',
                            string_value=identity_pool.ref
                            )
