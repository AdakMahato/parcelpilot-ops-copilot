import re
with open("backend/app/main.py", "r") as f:
    content = f.read()

import_stmt = "from app.models import Base"
if "ActivityLog" not in content:
    content = content.replace(import_stmt, "from app.models import Base, ActivityLog")

endpoint = """
@app.get("/api/activity")
def get_activity_log(auth=Depends(get_auth_context)):
    db = SessionLocal()
    try:
        logs = db.query(ActivityLog).order_by(ActivityLog.id.desc()).limit(50).all()
        return [
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "event_type": log.event_type,
                "description": log.description,
                "actor": log.actor
            } for log in logs
        ]
    finally:
        db.close()
"""
if "/api/activity" not in content:
    content = content + "\n" + endpoint

with open("backend/app/main.py", "w") as f:
    f.write(content)
