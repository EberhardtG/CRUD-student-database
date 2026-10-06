"""
WHY
----
This module implements all report‑related and notification‑related functionality
required by the assignment. It simulates long‑running background operations using
time.sleep(), allowing the API to demonstrate asynchronous behavior without
external infrastructure such as Celery or Redis. All report and notification
state is stored in simple in‑memory structures so task lifecycles can be easily
inspected through API endpoints and Swagger UI.

DESIGN
------
1. Logging is initialized at module load so all background tasks and API
   endpoints write to app.log. This allows instructors and developers to trace
   execution, diagnose failures, and verify correct background behavior.

2. ReportRequest validates incoming report payloads, ensuring report_type and
   rows are well‑formed before background processing begins.

3. generate_report() simulates a multi‑phase long‑running job by transitioning
   an in‑memory report entry through pending → processing → complete states.
   Timestamps are recorded, artificial delays mimic real workloads, and a text
   file is written to represent a finished report artifact. All phases are
   logged for debugging and reliability.

4. send_notification() simulates asynchronous message delivery by logging
   activity, delaying with time.sleep(), and appending a timestamped entry to
   the shared notification_log list. Logging ensures visibility into background
   message delivery.

5. The POST /reports endpoint initializes a pending report entry and schedules
   generate_report() as a background task, returning immediately so clients can
   poll for status updates. A notification task is also scheduled to demonstrate
   concurrent background execution.

6. The GET /reports/{id} endpoint exposes the current state of any report,
   allowing clients to observe status transitions and retrieve final results
   once processing completes.

7. Notification endpoints provide a simple asynchronous messaging workflow:
   POST /reports/notifications schedules a background notification, while
   GET /reports/notifications/log returns the accumulated history of all
   notifications sent so far.

Together, these components form a complete, self‑contained background task
simulation layer that fulfills the assignment requirements while remaining
lightweight, testable, and fully instrumented with logging for improved
reliability and debugging.
"""

from pydantic import BaseModel
from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
import time
from ..exceptions import AppException, NotFoundError, DuplicateError, AppValidationError
import logging


# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# In-memory stores
# ---------------------------------------------------------
reports = {}
notification_log = []

# ---------------------------------------------------------
# Schema
# ---------------------------------------------------------
class ReportRequest(BaseModel):
    report_type: str
    rows: list

router = APIRouter()

# ---------------------------------------------------------
# Background Task: Generate Report
# ---------------------------------------------------------
def generate_report(report_id: int, report_type: str, rows: list):
    try:
        logger.info(f"Starting report {report_id} ({report_type})")

        reports[report_id] = {
            "id": report_id,
            "type": report_type,
            "rows": rows,
            "status": "pending",
            "created_at": datetime.now(),
            "completed_at": None
        }

        logger.info(f"[{report_id}] Status: pending")
        time.sleep(1)

        reports[report_id]["status"] = "processing"
        logger.info(f"[{report_id}] Status: processing")
        time.sleep(3)

        reports[report_id]["status"] = "complete"
        reports[report_id]["completed_at"] = datetime.now()
        logger.info(f"[{report_id}] Status: complete")

        # Write report file
        filename = f"report_{report_id}.txt"
        with open(filename, "w") as f:
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Report Type: {report_type}\n")
            f.write(f"Generated at: {reports[report_id]['completed_at']}\n")
            f.write(f"Rows: {len(rows)}\n")
            f.write("Report content goes here...\n")

        logger.info(f"Report {report_id} written to {filename}")

    except Exception as e:
        logger.error(f"Error generating report {report_id}: {e}")

# ---------------------------------------------------------
# Background Task: Send Notification
# ---------------------------------------------------------
def send_notification(recipient: str, message: str):
    try:
        logger.info(f"Sending notification to {recipient}: {message}")
        time.sleep(1)

        entry = (recipient, message, datetime.now())
        notification_log.append(entry)

        logger.info(f"Notification sent to {recipient}")
        return entry

    except Exception as e:
        logger.error(f"Error sending notification to {recipient}: {e}")

# ---------------------------------------------------------
# POST /reports — Start Report Generation
# ---------------------------------------------------------
@router.post("/reports")
def create_report(payload: ReportRequest, background_tasks: BackgroundTasks):
    logger.info(f"Received report request: {payload.report_type}")

    report_id = len(reports) + 1

    reports[report_id] = {
        "id": report_id,
        "type": payload.report_type,
        "rows": payload.rows,
        "status": "pending",
        "created_at": datetime.now(),
        "completed_at": None
    }

    background_tasks.add_task(generate_report, report_id, payload.report_type, payload.rows)
    background_tasks.add_task(
        send_notification,
        recipient="user@example.com",
        message=f"Your report is being generated: {report_id}"
    )

    logger.info(f"Scheduled background tasks for report {report_id}")

    return {
        "message": "Report generation started",
        "report_id": report_id,
        "status": "pending"
    }

# ---------------------------------------------------------
# GET /reports/{id} — Retrieve Report Status
# ---------------------------------------------------------
@router.get("/reports/{report_id}")
def get_report(report_id: int):
    logger.info(f"Fetching report {report_id}")

    report = reports.get(report_id)
    if not report:
        logger.warning(f"Report {report_id} not found")
        raise NotFoundError("Report not found.")

    return report

# ---------------------------------------------------------
# POST /reports/notifications — Schedule Notification
# ---------------------------------------------------------
@router.post("/reports/notifications")
def create_notification(recipient: str, message: str, background_tasks: BackgroundTasks):
    logger.info(f"Scheduling notification to {recipient}: {message}")

    background_tasks.add_task(send_notification, recipient=recipient, message=message)

    return {"message": "Notification scheduled", "recipient": recipient, "content": message}

# ---------------------------------------------------------
# GET /reports/notifications/log — View Notification Log
# ---------------------------------------------------------
@router.get("/reports/notifications/log")
def get_notification_log():
    logger.info("Fetching notification log")
    return {"notifications": notification_log}
