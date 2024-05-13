from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://127.0.0.1:8000/"  # URL correcta del host

    @task
    def login(self):
        response = self.client.get("login")
        csrf_token = response.cookies.get("csrftoken")

        response = self.client.post("login", {
            "username": "Pablo@gmail.com",
            "password": "Pablo",
            "csrfmiddlewaretoken": csrf_token  # Asegúrate de incluir el token CSRF en la solicitud POST
        })


    @task
    def logout(self):
        # Incluye el token CSRF en la solicitud de logout
        self.client.post("logout/", {"csrfmiddlewaretoken": self.client.cookies['csrftoken']})
