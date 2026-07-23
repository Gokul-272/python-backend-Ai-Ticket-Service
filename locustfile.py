from locust import HttpUser, between, task
 
 
class TicketApiUser(HttpUser):
    wait_time = between(1, 3)
 
    @task(3)
    def check_health(self) -> None:
        self.client.get("/health", name="GET /health")
 
    @task(2)
    def list_tickets(self) -> None:
        self.client.get("/tickets/view", name="GET /tickets")
 
    @task(1)
    def create_ticket(self) -> None:
        self.client.post(
            "/tickets/",
            name="POST /tickets",
            json={
                 "title": "string",
                 "priority": "low",
                 "email": "Z-pK+Z1Y9-eNVIifl7WnCqr4EC1@bdt0R8nt2d6mx7slv6CZ8WnmJkDifObR8pz3Kbs7zQEnUIZ.5ktQhKrT.NMVRkAj-kFy5NQ-J"
            },
        )