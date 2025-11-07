from flask import Blueprint, request
from controllers.verifier_controller import get_verifier_dashboard, upsert_verifier

verifier_bp = Blueprint("verifier_bp", __name__)

# GET /api/v1/verifier/<id>
@verifier_bp.route("/<int:verifier_id>", methods=["GET"])
def get_dashboard(verifier_id: int):
    return get_verifier_dashboard(verifier_id)

# POST /api/v1/verifier/upsert
@verifier_bp.route("/upsert", methods=["POST"])
def seed_verifier():
    data = request.get_json() or {}
    return upsert_verifier(data)
