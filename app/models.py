from datetime import datetime

class Worker:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.shifts = []

    def add_shift(self, shift):
        self.shifts.append(shift)

    def get_shifts(self, date=None):
        if date is None:
            return self.shifts

        return [shift for shift in self.shifts if shift.date == date]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Shift:
    def __init__(self, id, worker_id, date, start_time, end_time):
        self.id = id
        self.worker_id = worker_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def time_range(self):
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        return start, end
    
    def to_dict(self):
        return {
            'id': self.id,
            'worker_id': self.worker_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'start_time': self.start_time.strftime('%H:%M:%S'),
            'end_time': self.end_time.strftime('%H:%M:%S'),
        }