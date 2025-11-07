import random
import uuid
from datetime import datetime
from flask import jsonify, request
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from db import Base, engine, SessionLocal

# -------------------------------------------
# ✅ QR Table
# -------------------------------------------
class BusinessQR(Base):
    __tablename__ = "business_qr"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String(100), unique=True, nullable=False)  # unique QR ID
    business_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)  # refill | purchase | eco-action
    is_scanned = Column(Boolean, default=False)
    points_awarded = Column(Integer, nullable=True)
    scanned_by_user = Column(Integer, nullable=True)  # user_id
    created_at = Column(DateTime, default=datetime.utcnow)
    scanned_at = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)


# -------------------------------------------
# ✅ Generate New QR for a Business
# -------------------------------------------
def generate_qr():
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data or "business_id" not in data or "action" not in data:
            return jsonify({"error": "business_id and action are required"}), 400

        qr_id = str(uuid.uuid4())[:8].upper()  # short unique ID like "AB12CD34"

        new_qr = BusinessQR(
            qr_code=qr_id,
            business_id=data["business_id"],
            action=data["action"]
        )
        db.add(new_qr)
        db.commit()
        db.refresh(new_qr)

        return jsonify({
            "message": "QR generated successfully",
            "qr": {
                "qr_id": new_qr.qr_code,
                "business_id": new_qr.business_id,
                "action": new_qr.action,
                "is_scanned": new_qr.is_scanned,
                "created_at": str(new_qr.created_at)
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# -------------------------------------------
# ✅ Check QR Status (for refresh every 2–3s)
# -------------------------------------------
def check_qr_status(qr_id):
    db = SessionLocal()
    try:
        qr = db.query(BusinessQR).filter_by(qr_code=qr_id).first()
        if not qr:
            return jsonify({"error": "QR not found"}), 404

        return jsonify({
            "qr_id": qr.qr_code,
            "business_id": qr.business_id,
            "action": qr.action,
            "is_scanned": qr.is_scanned,
            "points_awarded": qr.points_awarded,
            "scanned_by_user": qr.scanned_by_user,
            "scanned_at": str(qr.scanned_at) if qr.scanned_at else None
        }), 200
    finally:
        db.close()


# -------------------------------------------
# ✅ Mark QR as Scanned + Reward Points
# -------------------------------------------
def mark_qr_scanned():
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data or "qr_id" not in data or "user_id" not in data:
            return jsonify({"error": "qr_id and user_id are required"}), 400

        qr = db.query(BusinessQR).filter_by(qr_code=data["qr_id"]).first()
        if not qr:
            return jsonify({"error": "QR not found"}), 404
        if qr.is_scanned:
            return jsonify({"message": "QR already scanned"}), 200

        qr.is_scanned = True
        qr.scanned_by_user = data["user_id"]
        qr.points_awarded = random.randint(1, 10)
        qr.scanned_at = datetime.utcnow()

        db.commit()

        return jsonify({
            "message": "QR scan confirmed, points issued",
            "qr_id": qr.qr_code,
            "points_awarded": qr.points_awarded,
            "scanned_by_user": qr.scanned_by_user,
            "scanned_at": str(qr.scanned_at)
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
