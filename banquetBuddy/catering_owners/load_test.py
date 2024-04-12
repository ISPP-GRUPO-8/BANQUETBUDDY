from locust import HttpUser, task, between

#prueba para ver si funciona locust
#se puede borrar posteriormente
class MyUser(HttpUser):
    wait_time = between(5, 9)  # Tiempo de espera entre las solicitudes, en segundos

    @task
    def index_page(self):
        self.client.get("/")

    @task(3)
    def view_item(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")