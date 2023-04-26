from flask import Blueprint,jsonify, request
from .services import WorkPlanningService
from datetime import datetime

work_planning_service = WorkPlanningService()
bp = Blueprint("workers", __name__, url_prefix="/workers")


@bp.route("/", methods=["GET"])
def get_workers():
    workers = work_planning_service.get_workers()
    return jsonify([worker.to_dict() for worker in workers])


@bp.route("/", methods=["POST"])
def create_worker():
    name = request.json.get("name")
    if name is None:
        return jsonify({"error": "Name is required"}), 400
    worker = work_planning_service.create_worker(name)
    return jsonify(worker.to_dict()), 201

@bp.route("/<int:worker_id>/shifts", methods=["GET"])
def get_shifts_by_worker(worker_id):
    shifts = work_planning_service.get_shifts_by_worker(worker_id)
    return jsonify([shift.to_dict() for shift in shifts])

@bp.route("/<int:worker_id>/shifts", methods=["POST"])
def create_shift(worker_id):
    date = request.json.get("date")
    start_time = request.json.get("start_time")
    if date is None or start_time is None:
        return jsonify({"error": "Date and start_time are required"}), 400
    
    if start_time not in (0,8,16):
        return jsonify({"error": "Start time must be 0, 8 or 16"}), 400
    
    print(is_worker_existing)
    print(is_worker_existing(worker_id))
    if is_worker_existing(worker_id):
        if is_shift_existing(worker_id, start_time):
            return jsonify({"error": "Shift already exists"}), 400
    else:
        return jsonify({"error": "Worker does not exist"}), 400

    try :
        datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Date format must be YYYY-MM-DD"}), 400
    shift = work_planning_service.create_shift(worker_id, date, start_time, start_time + 8 % 24)
    return jsonify(shift.to_dict()), 201

def is_worker_existing(worker_id):
    return worker_id in work_planning_service.workers

def is_shift_existing(worker_id, start_time):
    for shift in work_planning_service.workers[worker_id].shifts:
        if shift.start_time == datetime.strptime(start_time, '%H:%M:%S').time():
            return True
    return False