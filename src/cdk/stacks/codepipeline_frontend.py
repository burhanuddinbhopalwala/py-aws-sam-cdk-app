# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_codebuild as cb
from aws_cdk import aws_codecommit as ccm
from aws_cdk import aws_codepipeline as cp
from aws_cdk import aws_codepipeline_actions as cp_actions
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class CodePipelineFrontendStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, webhostingbucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        webhosting_bucket = s3.Bucket.from_bucket_name(
            self, 'webhosting-id', bucket_name=webhostingbucket)
        cdn_id = ssm.StringParameter.from_string_parameter_name(
            self, 'cdnid', string_parameter_name='/'+env_name+'/app-distribution-id')
        source_repo = ccm.Repository.from_repository_name(
            self, 'repoid', repository_name='devops')

        artifact_bucket = s3.Bucket(self, 'artifactbucketid',
                                    encryption=s3.BucketEncryption.S3_MANAGED,
                                    access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL
                                    )

        build_project = cb.PipelineProject(self, 'buildfrontend',
                                           project_name='BuildFrontend',
                                           description='frontend project for SPA',
                                           environment=cb.BuildEnvironment(
                                               build_image=cb.LinuxBuildImage.STANDARD_3_0,
                                               environment_variables={
                                                   'distributionid': cb.BuildEnvironmentVariable(value=cdn_id.string_value)
                                               }
                                           ),
                                           cache=cb.Cache.bucket(bucket=artifact_bucket,
                                                                 prefix='codebuild-cache'),
                                           build_spec=cb.BuildSpec.from_object({
                                               'version': '0.2',
                                               'phases': {
                                                   'install': {
                                                       'commands': [
                                                           'pip install awscli'
                                                       ]
                                                   },
                                                   'pre_build': {
                                                       'commands': [
                                                           'yarn install'
                                                       ]
                                                   },
                                                   'build': {
                                                       'commands': [
                                                           'yarn run build'
                                                       ]
                                                   },
                                                   'post_build': {
                                                       'commands': [
                                                           'aws cloudfront create-invalidation --distribution-id $distributionid --paths "/*" '
                                                       ]
                                                   }
                                               },
                                               'artifacts': {
                                                   'files': [
                                                       'build/**/*'
                                                   ]
                                               },
                                               'cache': {
                                                   'paths': ['./node_modules/**/*']
                                               }
                                           })
                                           )

        pipeline = cp.Pipeline(self, 'frontend-pipeline',
                               pipeline_name=prj_name+'-'+env_name+'-frontend-pipeline',
                               artifact_bucket=artifact_bucket,
                               restart_execution_on_update=False
                               )

        source_output = cp.Artifact(artifact_name='source')
        build_output = cp.Artifact(artifact_name='build')

        pipeline.add_stage(stage_name='Source', actions=[
            cp_actions.CodeCommitSourceAction(
                action_name='CodeCommitSource',
                repository=source_repo,
                output=source_output,
                branch='master'
            )
        ])

        pipeline.add_stage(stage_name='Build', actions=[
            cp_actions.CodeBuildAction(
                action_name='Build',
                input=source_output,
                project=build_project,
                outputs=[build_output]
            )
        ])

        pipeline.add_stage(stage_name='Deploy', actions=[
            cp_actions.S3DeployAction(
                bucket=webhosting_bucket,
                input=build_output,
                action_name='Deploy',
                extract=True
            )
        ])

        build_project.role.add_to_policy(iam.PolicyStatement(
            actions=['cloudfront:CreateInvalidation'],
            resources=['*']
        ))
