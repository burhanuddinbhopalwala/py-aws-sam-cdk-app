# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class APIStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        account = core.Aws.ACCOUNT_ID
        region = core.Aws.REGION

        api_gateway = apigw.RestApi(self, 'restapi',
                                    endpoint_types=[
                                        apigw.EndpointType.REGIONAL],
                                    rest_api_name=prj_name+'-service'
                                    )
        api_gateway.root.add_method('ANY')

        ssm.StringParameter(self, 'api-gw',
                            parameter_name='/'+env_name+'/api-gw-url',
                            string_value='https://'+api_gateway.rest_api_id +
                            '.execute-api.'+region+'.amazonaws.com/'
                            )
        ssm.StringParameter(self, 'api-gw-id',
                            parameter_name='/'+env_name+'api-gw-id',
                            string_value=api_gateway.rest_api_id
                            )
