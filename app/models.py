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

class Shift:
    """Shift model."""
    def __init__(self, id, date, start_time, end_time):
        self.id = id
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
