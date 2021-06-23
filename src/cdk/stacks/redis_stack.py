# Copyright 2021 Burhanuddin Bhopalwala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticache as redis
from aws_cdk import aws_ssm as ssm
from aws_cdk import core


class RedisStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, redissg, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        subnets = [subnet.subnet_id for subnet in vpc.private_subnets]

        subnet_group = redis.CfnSubnetGroup(self, 'redis-subnet-group',
                                            subnet_ids=subnets,
                                            description='subnet group for redis'
                                            )

        redis_cluster = redis.CfnCacheCluster(self, 'redis',
                                              cache_node_type='cache.t2.small',
                                              engine='redis',
                                              num_cache_nodes=1,
                                              cluster_name=prj_name+'-redis-'+env_name,
                                              cache_subnet_group_name=subnet_group.ref,
                                              vpc_security_group_ids=[redissg],
                                              auto_minor_version_upgrade=True
                                              )
        redis_cluster.add_depends_on(subnet_group)

        ssm.StringParameter(self, 'redis-endpoint',
                            parameter_name='/'+env_name+'/redis-endpoint',
                            string_value=redis_cluster.attr_redis_endpoint_address
                            )

        ssm.StringParameter(self, 'redis-port',
                            parameter_name='/'+env_name+'/redis-port',
                            string_value=redis_cluster.attr_redis_endpoint_port
                            )
