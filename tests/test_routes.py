import json
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime
from app.app import create_app
from app.models import Worker, Shift
from app.services import WorkPlanningService


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def work_planning_service():
    return WorkPlanningService()

def workers():
    worker1 = Worker(id=1, name="John")
    worker2 = Worker(id=2, name="Jane")
    return [worker1, worker2]
    
def shifts():
    shift1 = Shift(id=1, worker_id=1, date=datetime(2023, 5, 1), start_time=datetime(2023, 5, 1, 8, 0, 0).time(), end_time=datetime(2023, 5, 1, 16, 0, 0).time())
    return [shift1]

def test_get_workers(client):
    with patch("app.services.WorkPlanningService.get_workers") as mock_get_workers:
        mock_get_workers.return_value = workers()
        response = client.get("/workers/")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[0]["name"] == "John"
        assert data[1]["id"] == 2
        assert data[1]["name"] == "Jane"


def test_create_worker(client):
    with patch("app.services.WorkPlanningService.create_worker") as mock_create_worker:
        mock_create_worker.return_value = workers()[0]
        response = client.post("/workers/", json={"name": "John"})
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["id"] == 1
        assert data["name"] == "John"
    response = client.post("/workers/", json={})
    assert response.status_code == 400


def test_get_shifts_by_worker(client):
    with patch("app.services.WorkPlanningService.get_shifts_by_worker") as mock_get_shifts_by_worker:
        mock_get_shifts_by_worker.return_value = shifts()
        response = client.get("/workers/1/shifts")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1


@patch("app.routes.is_shift_existing")
@patch("app.routes.is_worker_existing")
@patch("app.services.WorkPlanningService.create_shift")
def test_create_shift(mock_creat_shift, mock_is_worker_existing, mock_is_shift_existing, client):
    mock_is_shift_existing.return_value = False
    mock_is_worker_existing.return_value = True
    mock_creat_shift.return_value = shifts()[0]
    response = client.post("/workers/1/shifts", json={"date": "2023-05-01", "start_time": 8})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["id"] == 1
    assert data["worker_id"] == 1
    assert data["date"] == shifts()[0].date.strftime('%Y-%m-%d')
    assert data["start_time"] == shifts()[0].start_time.strftime('%H:%M:%S')
    assert data["end_time"] == shifts()[0].end_time.strftime('%H:%M:%S')

@patch("app.routes.is_shift_existing")
@patch("app.routes.is_worker_existing")
@patch("app.services.WorkPlanningService.create_shift")
@patch("app.services.WorkPlanningService.get_shifts_by_worker")
def test_create_shift_overlapping(mock_get_shifts_by_worker, mock_create_shift, mock_is_worker_existing, mock_is_shift_existing, client):
    mock_is_shift_existing.return_value = False
    mock_is_worker_existing.return_value = True
    mock_get_shifts_by_worker.return_value = shifts()
    mock_create_shift.return_value = shifts()[0]

    response = client.post("/workers/1/shifts", json={"date": "2023-05-01", "start_time": 8})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "Shift is overlapping"
