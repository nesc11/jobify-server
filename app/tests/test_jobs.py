# from fastapi.testclient import TestClient

# from app.main import app

# client = TestClient(app)


# def test_read_job():
#     response = client.get("/jobs/1")
#     assert response.status_code == 401
#     print(response.json())
#     print(type(response.json()))
#     assert response.json() == {"detail": "Not authenticated"}
