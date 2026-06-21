from locust import HttpUser, task, between

class WedehagerUserSimulation(HttpUser):
    # Simulate realistic delay: passengers wait 1 to 3 seconds between clicks
    wait_time = between(1, 3)

    @task(3)
    def view_homepage(self):
        self.client.get("/")

    @task(1)
    def mock_ticket_query(self):
        # Simulates users calling your balance/ticket database check endpoints
        self.client.post("/users/recover-balance/", data={
            "firstname": "Abebe",
            "lastname": "Kebede",
            "depcity": "Addisababa",
            "descity": "Bahirdar",
            "date": "2026-06-01"
        })
