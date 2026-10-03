"""
WHY:
This module implements all report‑related and notification‑related functionality
required by the assignment. It simulates long‑running background operations
using time.sleep(), allowing the API to demonstrate asynchronous behavior
without relying on external infrastructure such as Celery, Redis, or a
database. All report and notification state is stored in simple in‑memory
structures so the lifecycle of each background task can be inspected easily
through API endpoints and Swagger UI.

DESIGN:
1. ReportRequest defines the JSON body schema for POST /reports, ensuring
   report_type and rows are validated before background processing begins.

2. generate_report() simulates a multi‑phase long‑running job by updating an
   in‑memory report entry through pending → processing → complete states.
   Timestamps are recorded, artificial delays mimic real workloads, and a
   text file is written to represent a finished report artifact.

3. send_notification() simulates asynchronous message delivery by printing
   activity, delaying with time.sleep(), and appending a timestamped entry to
   the shared notification_log list. This provides a lightweight stand‑in for
   real outbound notification systems.

4. The POST /reports endpoint creates an initial pending report entry and
   schedules generate_report() as a background task, returning immediately so
   the client can poll for status updates. It also schedules a notification to
   demonstrate multiple background tasks running concurrently.

5. The GET /reports/{id} endpoint exposes the current state of any report,
   allowing clients to observe status transitions and retrieve final results
   once processing completes.

6. Notification endpoints provide a simple asynchronous messaging workflow:
   POST /reports/notifications schedules a background notification, while
   GET /reports/notifications/log returns the accumulated history of all
   notifications sent so far.

Together, these components form a complete, self‑contained background task
simulation layer that fulfills the assignment requirements while keeping the
implementation lightweight, testable, and free of external dependencies.
"""






from pydantic import BaseModel
from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
import time
from app.exceptions import AppException, NotFoundError,DuplicateError,AppValidationError

# In-memory stores
reports = {}
notification_log = []

class ReportRequest(BaseModel):
    report_type: str
    rows: list

router = APIRouter()

# In-memory report store
reports = {}

def generate_report(report_id: int, report_type: str, rows: list):
    # Create initial report entry
    reports[report_id] = {
        "id": report_id,
        "type": report_type,
        "rows": rows,
        "status": "pending",
        "created_at": datetime.now(),
        "completed_at": None
    }

    print(f"[{report_id}] Status: pending")
    time.sleep(1)

    # Move to processing
    reports[report_id]["status"] = "processing"
    print(f"[{report_id}] Status: processing")
    time.sleep(3)

    # Finish report
    reports[report_id]["status"] = "complete"
    reports[report_id]["completed_at"] = datetime.now()
    print(f"[{report_id}] Status: complete")

    # Optionally write a file
    with open(f"report_{report_id}.txt", "w") as f:
        f.write(f"Report ID: {report_id}\n")
        f.write(f"Report Type: {report_type}\n")
        f.write(f"Generated at: {reports[report_id]['completed_at']}\n")
        f.write(f"Rows: {len(rows)}\n")
        f.write("Report content goes here...\n")

    return reports[report_id]



notification_log = []

def send_notification(recipient: str, message: str):
    print(f"Notification: sending {message} to {recipient}")
    time.sleep(1)
    entry = (recipient, message, datetime.now())
    notification_log.append(entry)
    print(f"Notification: sent {message} to {recipient}")
    return entry

#---------------------------------------------------------
# Post /reports- generate a unique report id and store the initial pending status in the in-memory reports dictionary. Then, call the generate_report function to simulate report generation.
#---------------------------------------------------------
@router.post("/reports")
def create_report(payload: ReportRequest, background_tasks: BackgroundTasks):
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

    return {
        "message": "Report generation started",
        "report_id": report_id,
        "status": "pending"
    }



#---------------------------------------------------------
# GET /reports/{report_id} - Retrieve report status and details
#---------------------------------------------------------
@router.get("/reports/{report_id}")
def get_report(report_id: int):
    report = reports.get(report_id)
    if not report:
        raise NotFoundError("Report not found.")

    return report


#---------------------------------------------------------
# POST /reports/notifications schedule a notification in the background and return immediately
#---------------------------------------------------------
@router.post("/reports/notifications")
def create_notification(recipient: str, message: str, background_tasks: BackgroundTasks):
    # Schedule background task
    background_tasks.add_task(send_notification, recipient=recipient, message=message)

    # Return immediately

    return {"message": "Notification scheduled", "recipient": recipient, "content": message}

#---------------------------------------------------------
#GET /reports/notifications/log — return the log of notifications sent so far
#---------------------------------------------------------
@router.get("/reports/notifications/log")
def get_notification_log():
    # Return the log of notifications sent so far
    return {"notifications": notification_log}
