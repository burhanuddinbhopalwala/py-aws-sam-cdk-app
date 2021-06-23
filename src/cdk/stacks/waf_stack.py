# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_wafv2 as waf
from aws_cdk import core


class WafStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        basic_rule = waf.CfnWebACL.RuleProperty(
            name='AWSManagedCommonRule',
            priority=0,
            statement=waf.CfnWebACL.StatementOneProperty(
                managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name='AWSManagedRulesCommonRuleSet',
                    vendor_name='AWS'
                )
            ),
            override_action=waf.CfnWebACL.OverrideActionProperty(count={}),
            visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name='AWSManagedCommonRule',
                sampled_requests_enabled=True
            )
        )

        web_acl = waf.CfnWebACL(self, 'web-acl-id',
                                default_action=waf.CfnWebACL.DefaultActionProperty(
                                    allow={}),
                                scope='CLOUDFRONT',
                                visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                                    cloud_watch_metrics_enabled=True,
                                    metric_name=prj_name+'-'+env_name,
                                    sampled_requests_enabled=True
                                ),
                                name=prj_name+'-'+env_name+'webacl',
                                rules=[basic_rule]
                                )

        ssm.StringParameter(self, 'webacl-id-ssm',
                            parameter_name='/'+env_name+'/webacl-id',
                            string_value=web_acl.attr_id
                            )
