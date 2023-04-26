import pytest
from datetime import date, time
from app.services import WorkPlanningService

@pytest.fixture
def work_planning_service():
    return WorkPlanningService()

def test_create_worker(work_planning_service):
    worker = work_planning_service.create_worker("John Doe")
    assert worker.name == "John Doe"

def test_create_shift(work_planning_service):
    worker = work_planning_service.create_worker("John Doe")
    shift = work_planning_service.create_shift(worker.id, "2023-05-01", 8, 16)
    assert shift.date == date(2023, 5, 1)
    assert shift.start_time == time(8, 0, 0)
    assert shift.end_time == time(16, 0, 0)

def test_get_shifts(work_planning_service):
    worker = work_planning_service.create_worker("John Doe")
    shift1 = work_planning_service.create_shift(worker.id, "2023-05-01", 0, 8)
    shift2 = work_planning_service.create_shift(worker.id, "2023-05-02", 8, 16)
    shifts = work_planning_service.get_shifts()
    assert len(shifts) == 2
    assert shift1 in shifts
    assert shift2 in shifts

def test_get_shifts_by_worker(work_planning_service):
    worker1 = work_planning_service.create_worker("John Doe")
    worker2 = work_planning_service.create_worker("Jane Smith")
    shift1 = work_planning_service.create_shift(worker1.id, "2023-05-01", 8,16)
    shift2 = work_planning_service.create_shift(worker1.id, "2023-05-02", 8,16)
    shift3 = work_planning_service.create_shift(worker2.id, "2023-05-03", 8,16)
    shifts = work_planning_service.get_shifts_by_worker(worker1.id)
    assert len(shifts) == 2
    assert shift1 in shifts
    assert shift2 in shifts
    assert shift3 not in shifts

def test_get_workers(work_planning_service):
    worker1 = work_planning_service.create_worker("John Doe")
    worker2 = work_planning_service.create_worker("Jane Smith")
    workers = work_planning_service.get_workers()
    assert len(workers) == 2
    assert worker1 in workers
    assert worker2 in workers
