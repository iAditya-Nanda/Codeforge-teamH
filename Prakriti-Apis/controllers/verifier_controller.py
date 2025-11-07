from flask import jsonify, request
from sqlalchemy import Column, Integer, String
from db import Base, engine, SessionLocal
from utils.blockchain import blockchain  # ✅ Local blockchain ledger
from datetime import datetime

# -------------------------------------------
# ✅ Verifier Table
# -------------------------------------------
class Verifier(Base):
    __tablename__ = "verifiers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    pending_verifications = Column(Integer, default=0)
    approved_actions = Column(Integer, default=0)
    rejected_items = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)


# -------------------------------------------
# ✅ Get Verifier Dashboard
# -------------------------------------------
def get_verifier_dashboard(verifier_id: int):
    """
    Fetch verifier dashboard stats.
    Also logs a blockchain event for transparency.
    """
    db = SessionLocal()
    try:
        verifier = db.query(Verifier).get(verifier_id)
        if not verifier:
            return jsonify({"error": "Verifier not found"}), 404

        # ✅ Blockchain log for data retrieval
        blockchain.add_block({
            "event": "verifier_dashboard_fetched",
            "verifier_id": verifier.id,
            "timestamp": str(datetime.utcnow()),
            "stats": {
                "pending_verifications": verifier.pending_verifications,
                "approved_actions": verifier.approved_actions,
                "rejected_items": verifier.rejected_items
            }
        })

        return jsonify({
            "verifier_id": verifier.id,
            "name": verifier.name,
            "pendingVerifications": verifier.pending_verifications,
            "approvedActions": verifier.approved_actions,
            "rejectedItems": verifier.rejected_items
        }), 200
    finally:
        db.close()


# -------------------------------------------
# ✅ Upsert Verifier (Insert/Update)
# -------------------------------------------
def upsert_verifier(data):
    """
    Creates or updates a verifier record.
    Logs every change in blockchain for traceability.
    """
    db = SessionLocal()
    try:
        # Validate input
        if "id" not in data or not data["id"]:
            return jsonify({"error": "id is required"}), 400
        if "name" not in data:
            return jsonify({"error": "name is required"}), 400

        verifier_id = int(data["id"])

        # Fetch existing record
        verifier = db.query(Verifier).get(verifier_id)
        is_new = False

        if verifier:
            # Update existing record
            verifier.name = data.get("name", verifier.name)
            verifier.pending_verifications = data.get("pendingVerifications", verifier.pending_verifications)
            verifier.approved_actions = data.get("approvedActions", verifier.approved_actions)
            verifier.rejected_items = data.get("rejectedItems", verifier.rejected_items)
        else:
            # Create new record
            is_new = True
            verifier = Verifier(
                id=verifier_id,
                name=data["name"],
                pending_verifications=data.get("pendingVerifications", 0),
                approved_actions=data.get("approvedActions", 0),
                rejected_items=data.get("rejectedItems", 0)
            )
            db.add(verifier)

        db.commit()
        db.refresh(verifier)

        # ✅ Blockchain record
        blockchain.add_block({
            "event": "verifier_created" if is_new else "verifier_updated",
            "verifier_id": verifier.id,
            "name": verifier.name,
            "pending_verifications": verifier.pending_verifications,
            "approved_actions": verifier.approved_actions,
            "rejected_items": verifier.rejected_items,
            "timestamp": str(datetime.utcnow())
        })

        return jsonify({
            "message": "Verifier upserted successfully",
            "verifier": {
                "id": verifier.id,
                "name": verifier.name,
                "pendingVerifications": verifier.pending_verifications,
                "approvedActions": verifier.approved_actions,
                "rejectedItems": verifier.rejected_items
            }
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
