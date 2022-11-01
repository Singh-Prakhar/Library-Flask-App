from app import app


def test_hello():
    test_response = app.test_client.get("/hello")




