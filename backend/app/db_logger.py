import datetime
from app.database import SessionLocal
from app.models import ActivityLog

def log_activity(event_type: str, description: str, actor: str = "System"):
    try:
        db = SessionLocal()
        # Ensure timestamp matches the snapshot context somewhat, or just use current time
        # The user requested 'real events' using 'actual application execution data'
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = ActivityLog(
            timestamp=now_str,
            event_type=event_type,
            description=description,
            actor=actor
        )
        db.add(log)
        db.commit()
    except Exception as e:
        print("Failed to log activity:", e)
    finally:
        db.close()
