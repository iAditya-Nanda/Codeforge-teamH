import os
import random
from datetime import datetime
from flask import jsonify, request
from werkzeug.utils import secure_filename
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, ForeignKey, text
from db import Base, engine, SessionLocal
from utils.blockchain import blockchain  # ✅ Blockchain integration

# -------------------------------------------
# ⚙️ Upload Config
# -------------------------------------------
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has a valid extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------------------------------
# 🧾 Tourist Submissions Table
# -------------------------------------------
class TouristSubmission(Base):
    __tablename__ = "tourist_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False, default="tourist")
    title = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    image_url = Column(String(1000), nullable=True)
    status = Column(String(20), nullable=False, default="pending")  # pending|approved|rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    reviewer_id = Column(Integer, nullable=True)
    remarks = Column(String(500), nullable=True)

    __table_args__ = (
        CheckConstraint("type = 'tourist'", name="ck_only_tourist_type"),
        CheckConstraint("status IN ('pending','approved','rejected')", name="ck_valid_submission_status"),
        {"implicit_returning": False},  # avoid OUTPUT trigger issues in SQL Server
    )


# -------------------------------------------
# 🧮 User Points Table
# -------------------------------------------
class UserPoints(Base):
    __tablename__ = "user_points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    submission_id = Column(Integer, ForeignKey("tourist_submissions.id"), nullable=False)
    points = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# -------------------------------------------
# 📤 Upload Image
# -------------------------------------------
def upload_submission_image():
    """Uploads a proof image for tourist submission"""
    if "file" not in request.files:
        return jsonify({"error": "file is required"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "unsupported file type"}), 400

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    unique_name = f"{timestamp}_{filename}"
    path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(path)

    return jsonify({
        "message": "uploaded",
        "url": f"/uploads/{unique_name}"
    }), 201


# -------------------------------------------
# ➕ Add Tourist Submission
# -------------------------------------------
def add_tourist_submission(data=None):
    """Add a new tourist submission"""
    if not data:
        try:
            data = request.get_json(force=True, silent=True)
        except Exception:
            data = None
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    missing = [f for f in ["user_id", "title", "location"] if f not in data or not str(data[f]).strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        user_id = int(data["user_id"])
    except Exception:
        return jsonify({"error": "user_id must be an integer"}), 400

    db = SessionLocal()
    try:
        sub = TouristSubmission(
            user_id=user_id,
            title=data["title"].strip(),
            location=data["location"].strip(),
            image_url=(data.get("image_url") or None),
            status="pending"
        )
        db.add(sub)
        db.commit()
        db.refresh(sub)

        # ✅ Add blockchain log for submission creation
        blockchain.add_block({
            "event": "tourist_submission_created",
            "submission_id": sub.id,
            "user_id": sub.user_id,
            "title": sub.title,
            "location": sub.location,
            "status": sub.status,
            "timestamp": str(sub.created_at)
        })

        return jsonify({
            "message": "submission created",
            "submission": {
                "id": sub.id,
                "user_id": sub.user_id,
                "title": sub.title,
                "location": sub.location,
                "image": sub.image_url,
                "status": sub.status,
                "timestamp": sub.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.rollback()
        print("❌ Error while inserting submission:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# -------------------------------------------
# 📋 Get All Submissions
# -------------------------------------------
def get_all_tourist_submissions():
    """Fetch all submissions, optionally filtered by status or user_id"""
    status = (request.args.get("status") or "").strip().lower()
    user_id = request.args.get("user_id")

    db = SessionLocal()
    try:
        q = db.query(TouristSubmission)
        if status in {"pending", "approved", "rejected"}:
            q = q.filter(TouristSubmission.status == status)
        if user_id:
            q = q.filter(TouristSubmission.user_id == int(user_id))

        apps = q.order_by(TouristSubmission.created_at.desc()).all()
        data = [{
            "id": a.id,
            "user_id": a.user_id,
            "title": a.title,
            "location": a.location,
            "status": a.status,
            "image": a.image_url,
            "timestamp": a.created_at.isoformat(),
            "reviewer_id": a.reviewer_id,
            "remarks": a.remarks
        } for a in apps]

        return jsonify({"submissions": data}), 200
    except Exception as e:
        print("❌ Error while fetching submissions:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# -------------------------------------------
# ✅ Approve/Reject Submission + Award Points + Update Verifier Stats + Blockchain Log
# -------------------------------------------
def review_submission(submission_id: int, data: dict):
    """Approve or reject a tourist submission and award points if approved"""
    action = (data.get("action") or "").lower()
    if action not in {"approve", "reject"}:
        return jsonify({"error": "action must be 'approve' or 'reject'"}), 400

    db = SessionLocal()
    try:
        sub = db.query(TouristSubmission).get(submission_id)
        if not sub:
            return jsonify({"error": "submission not found"}), 404

        reviewer_id = data.get("reviewer_id")
        sub.status = "approved" if action == "approve" else "rejected"
        sub.reviewed_at = datetime.utcnow()
        sub.reviewer_id = reviewer_id
        sub.remarks = data.get("remarks")

        # ✅ Award random points (0–10) if approved
        points_awarded = None
        if sub.status == "approved":
            points_awarded = random.randint(0, 10)
            new_points = UserPoints(
                user_id=sub.user_id,
                submission_id=sub.id,
                points=points_awarded,
                reason=sub.title
            )
            db.add(new_points)

        db.commit()

        # ✅ Blockchain log for review
        blockchain.add_block({
            "event": f"submission_{sub.status}",
            "submission_id": sub.id,
            "reviewer_id": reviewer_id,
            "user_id": sub.user_id,
            "points_awarded": points_awarded,
            "remarks": sub.remarks,
            "timestamp": str(sub.reviewed_at)
        })

        # ✅ Update verifier statistics
        if reviewer_id:
            stats_sql = text("""
                UPDATE verifiers
                SET
                    pending_verifications = (
                        SELECT COUNT(*) FROM tourist_submissions
                        WHERE reviewer_id = :rid AND status = 'pending'
                    ),
                    approved_actions = (
                        SELECT COUNT(*) FROM tourist_submissions
                        WHERE reviewer_id = :rid AND status = 'approved'
                    ),
                    rejected_items = (
                        SELECT COUNT(*) FROM tourist_submissions
                        WHERE reviewer_id = :rid AND status = 'rejected'
                    )
                WHERE id = :rid
            """)
            db.execute(stats_sql, {"rid": reviewer_id})
            db.commit()

        return jsonify({
            "message": f"submission {sub.status}",
            "submission": {
                "id": sub.id,
                "user_id": sub.user_id,
                "status": sub.status,
                "reviewer_id": sub.reviewer_id,
                "remarks": sub.remarks,
                "points_awarded": points_awarded
            }
        }), 200

    except Exception as e:
        db.rollback()
        print("❌ Error during review:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
