from flask import Blueprint
from controllers.qr_controller import generate_qr, check_qr_status, mark_qr_scanned

qr_bp = Blueprint("qr_bp", __name__)

# POST /api/v1/qr/generate
@qr_bp.route("/generate", methods=["POST"])
def create_qr():
    return generate_qr()

# GET /api/v1/qr/status/<qr_id>
@qr_bp.route("/status/<string:qr_id>", methods=["GET"])
def qr_status(qr_id):
    return check_qr_status(qr_id)

# POST /api/v1/qr/scan
@qr_bp.route("/scan", methods=["POST"])
def scan_qr():
    return mark_qr_scanned()
