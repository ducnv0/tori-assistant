from locust import HttpUser, between, task


class UserBehavior(HttpUser):
    wait_time = between(1, 3)  # Simulates users waiting between requests
    host = 'http://localhost:8000'

    @task
    def get_users(self):
        self.client.get('/api/user', params={'page': 1, 'page_size': 10})
