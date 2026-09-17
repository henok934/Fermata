# locustfile.py

from locust import HttpUser, task, between

class BusfermataUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_home(self):
        self.client.get("/")

    @task(2)
    def view_get_ticket(self):
        # በ hyphen (-) የነበረውን ወደ underscore (_) አስተካክለው
        self.client.get("/get_ticket/")

    @task(1)
    def submit_ticket_flow(self):
        self.client.post("/ticket/", data={
            "firstname[]": "Abebe",
            "lastname[]": "Bikila",
            "phone[]": "0911000000",
            "gender[]": "male",
            "passenger_type[]": "adult",
            "email[]": "test@example.com",
            "no_seat[]": "12"
        })
