import aioredis
import click
from aiocassandra import aiosession
from tornado import ioloop
from tornado.web import Application
import asyncio

from favourite.settings import DEFAULT_PORT
from favourite.web.urls import get_all_urls

import cassandra.io.asyncioreactor
import cassandra.policies
from cassandra.cluster import Cluster

from favourite.settings import CASSANDRA_CONF
from favourite.settings import REDIS_CONF

from favourite.services.cassandra import CassandraManager
from cassandra.cluster import ExecutionProfile

from cassandra.cluster import EXEC_PROFILE_DEFAULT

from favourite.services.redis import RedisManager
from favourite.services.db_proxy import DBProxy


class FavouriteApplication(Application):
    def __init__(self, handlers, **kwargs):
        super(FavouriteApplication, self).__init__(handlers=handlers, **kwargs)

    def prepare(self):
        node_profile = ExecutionProfile(load_balancing_policy=cassandra.policies.RoundRobinPolicy())

        self.cassandra_cluster = Cluster(
            **CASSANDRA_CONF,
            execution_profiles={EXEC_PROFILE_DEFAULT: node_profile}
        )
        self.cassandra_session = self.cassandra_cluster.connect('favourite')
        aiosession(self.cassandra_session)

        self.cassandra_manager = CassandraManager(self.cassandra_session)

        self.redis = asyncio.get_event_loop().run_until_complete(
            aioredis.create_redis(address=(REDIS_CONF['host'], REDIS_CONF['port']))
        )

        self.redis_manager = RedisManager(self.redis)

        self.db_proxy = DBProxy(redis_manager=self.redis_manager, cassandra_manager=self.cassandra_manager)


@click.command()
@click.option('--port', default=DEFAULT_PORT)
def serve(port: int):
    handlers = get_all_urls()
    application = FavouriteApplication(handlers)
    application.listen(port)
    application.prepare()
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    serve()
