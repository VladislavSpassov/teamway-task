from datetime import datetime

def get_date_by_integer(integer):
    return datetime.strptime(f'{integer}:0:0', '%H:%M:%S')

def get_date_by_string(string):
    return datetime.strptime(string, '%Y-%m-%d').date()