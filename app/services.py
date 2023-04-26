from datetime import datetime
from .models import Worker, Shift
from datetime import datetime

class WorkPlanningService:
    def __init__(self):
        self.workers = {}
        self.shifts = {}
        
    def create_worker(self, name):
        worker_id = len(self.workers) + 1
        worker = Worker(worker_id, name)
        self.workers[worker_id] = worker
        return worker
    
    def create_shift(self, worker_id, date, start_time, end_time):        
        start_time = datetime.strptime(f'{start_time}:0:0', '%H:%M:%S').time()
        end_time = datetime.strptime(f'{start_time.hour + 8}:0:0', '%H:%M:%S').time()
        date = datetime.strptime(date, '%Y-%m-%d').date()
        shift_id = len(self.shifts) + 1
        shift = Shift(shift_id, worker_id, date, start_time, end_time)
        self.shifts[shift_id] = shift
        self.workers[worker_id].shifts.append(shift)
        return shift
    
    def get_shifts(self):
        return self.shifts.values()
    
    def get_shifts_by_worker(self, worker_id):
        return [shift for shift in self.shifts.values() if shift.worker_id == worker_id]
    
    def get_workers(self):
        return self.workers.values()
