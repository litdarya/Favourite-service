import string
import random

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    def on_start(self):
        self.name = self._gen_str(10)
        self.items = []

    def _gen_str(self, N):
        return "".join(random.choices(string.ascii_letters + string.digits, k=N))

    @task(1)
    def add_item(self):
        self.items.append(self._gen_str(10))
        data = {"user": self.name, "item": self.items[-1]}
        self.client.post("/add-to-favourite/", json=data)

    @task(3)
    def check_if_exists(self):
        if len(self.items) > 0:
            ind = random.randint(0, len(self.items) - 1)
            item = self.items[ind]
        else:
            item = self._gen_str(10)
        data = {"user": self.name, "item": item}
        self.client.post("/check-if-favourite/", json=data)

    @task(2)
    def delete_item(self):
        if len(self.items) > 0:
            ind = random.randint(0, len(self.items) - 1)
            item = self.items[ind]
            data = {"user": self.name, "item": item}
            self.client.post("/remove-from-favourite/", json=data)

    @task(4)
    def get_all(self):
        self.client.post("/get-all-favourite/", json={"user": self.name})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 9000