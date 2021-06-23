# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_codebuild as cb
from aws_cdk import aws_codepipeline as cp
from aws_cdk import aws_codepipeline_actions as cp_actions
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_secretsmanager as sm
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class CodePipelineBackendStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, artifactbucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        artifact_bucket = s3.Bucket.from_bucket_name(
            self, 'artifactbucket', artifactbucket)

        github_token = core.SecretValue.secrets_manager(
            env_name+'/github-token', json_field='github-token'
        )

        build_project = cb.PipelineProject(self, 'buildproject',
                                           project_name=env_name+'-'+prj_name+'-build-project',
                                           description='package lambda functions',
                                           environment=cb.BuildEnvironment(
                                               build_image=cb.LinuxBuildImage.STANDARD_3_0,
                                               environment_variables={
                                                 'ENV': cb.BuildEnvironmentVariable(value='dev'),
                                                 'PRJ': cb.BuildEnvironmentVariable(value=prj_name),
                                                 'STAGE': cb.BuildEnvironmentVariable(value='dev')
                                               }
                                           ),
                                           cache=cb.Cache.bucket(
                                               artifact_bucket, prefix='codebuild-cache'),
                                           build_spec=cb.BuildSpec.from_object({
                                               'version': '0.2',
                                               'phases': {
                                                   'install': {
                                                       'commands': [
                                                           'echo "--INSTALL PHASE--" ',
                                                           'npm install --silent --no-progress serverless -g'
                                                       ]
                                                   },
                                                   'pre_build': {
                                                       'commands': [
                                                           'echo "--PRE BUILD PHASE--"',
                                                           'npm install --silent --no-progress'
                                                       ]
                                                   },
                                                   'build': {
                                                       'commands': [
                                                           'echo "--BUILD PHASE--" ',
                                                           'serverless deploy -s $STAGE'
                                                       ]
                                                   }
                                               },
                                               'artifacts': {
                                                   'files': ['**/*'],
                                                   'base-directory': '.serverless'
                                               }
                                           })
                                           )

        pipeline = cp.Pipeline(self, 'backend-pipeline',
                               pipeline_name=env_name+'-'+prj_name+'-backend-pipeline',
                               artifact_bucket=artifact_bucket,
                               restart_execution_on_update=False
                               )

        source_output = cp.Artifact(artifact_name='source')
        build_output = cp.Artifact(artifact_name='build')

        pipeline.add_stage(stage_name='Source', actions=[
            cp_actions.GitHubSourceAction(
                oauth_token=github_token,
                output=source_output,
                repo='devops',
                branch='master',
                owner='nixsupport',
                action_name='GitHubSource'
            )
        ])
        pipeline.add_stage(stage_name='Deploy', actions=[
            cp_actions.CodeBuildAction(
                action_name='DeployToDev',
                input=source_output,
                project=build_project,
                outputs=[build_output]
            )
        ])
        '''
        build_project.role.add_to_policy(iam.PolicyStatement(
            actions=['cloudformation:*','s3:*','iam:*','lambda:*','apigateway:*'],
            resources=['*']
        ))
        '''
        build_project.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AdministratorAccess')
        )

        account_id = core.Aws.ACCOUNT_ID
        region = core.Aws.REGION

        ssm.StringParameter(self, 'accountid',
                            parameter_name='/'+env_name+'/account-id',
                            string_value=account_id
                            )

        ssm.StringParameter(self, 'region',
                            parameter_name='/'+env_name+'/region',
                            string_value=region
                            )
