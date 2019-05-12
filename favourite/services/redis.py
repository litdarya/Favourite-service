class RedisManager:

    def __init__(self, session):
        self.session = session

    async def delete_user_item(self, *, user, item):
        key = user + ';' + item
        return await self.session.delete(key)

    async def check_if_user_item_exists(self, *, user, item) -> bool:
        key = user + ';' + item
        result = await self.session.get(key)
        if result is None:
            return False
        return True

    async def insert_user_item(self, *, user, item):
        key = user + ';' + item
        # time to expire should be average time that consumers spend on the session
        result = await self.session.set(key, 1, expire=5*60)
        return result
