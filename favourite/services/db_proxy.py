from favourite.services.redis import RedisManager
from favourite.services.cassandra import CassandraManager


class DBProxy:

    def __init__(self, *, redis_manager: RedisManager, cassandra_manager: CassandraManager):
        self.redis = redis_manager
        self.cassandra = cassandra_manager

    async def get_all_favourite(self, *, user) -> list:
        return await self.cassandra.get_all_favourite(user=user)

    async def delete_user_item(self, *, user, item) -> bool:
        await self.redis.delete_user_item(user=user, item=item)
        return await self.cassandra.delete_user_item(user=user, item=item)

    async def check_if_user_item_exists(self, *, user, item) -> bool:
        result = await self.redis.check_if_user_item_exists(user=user, item=item)
        if result:
            return True
        db_result = await self.cassandra.check_if_user_item_exists(user=user, item=item)
        if db_result:
            await self.redis.insert_user_item(user=user, item=item)
        return db_result

    async def insert_user_item_if_not_exists(self, *, user, item) -> bool:
        result = await self.cassandra.insert_user_item_if_not_exists(user=user, item=item)
        if result:
            await self.redis.insert_user_item(user=user, item=item)
        return result
