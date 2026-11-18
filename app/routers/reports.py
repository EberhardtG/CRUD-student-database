from datetime import datetime
from typing import Any

import logging
import time

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from ..exceptions import NotFoundError


# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# In-Memory Storage
# ---------------------------------------------------------
reports: dict[int, dict[str, Any]] = {}
notification_log: list[dict[str, Any]] = []


# ---------------------------------------------------------
# Schemas
# ---------------------------------------------------------
class ReportRequest(BaseModel):
    report_type: str
    rows: list


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------
router = APIRouter()


# ---------------------------------------------------------
# Background Task: Generate Report
# ---------------------------------------------------------
def generate_report(
    report_id: int,
    report_type: str,
    rows: list,
) -> None:

    try:
        logger.info(
            f"Starting report {report_id} ({report_type})"
        )

        reports[report_id]["status"] = "processing"

        logger.info(
            f"[{report_id}] Status: processing"
        )

        time.sleep(3)

        reports[report_id]["status"] = "complete"
        reports[report_id]["completed_at"] = datetime.now()

        filename = f"report_{report_id}.txt"

        with open(filename, "w") as report_file:
            report_file.write(
                f"Report ID: {report_id}\n"
            )
            report_file.write(
                f"Report Type: {report_type}\n"
            )
            report_file.write(
                f"Generated At: "
                f"{reports[report_id]['completed_at']}\n"
            )
            report_file.write(
                f"Rows: {len(rows)}\n"
            )
            report_file.write(
                "Report content goes here...\n"
            )

        logger.info(
            f"Report {report_id} written to {filename}"
        )

    except Exception as e:
        logger.error(
            f"Error generating report "
            f"{report_id}: {e}"
        )


# ---------------------------------------------------------
# Background Task: Send Notification
# ---------------------------------------------------------
def send_notification(
    recipient: str,
    message: str,
) -> None:

    try:
        logger.info(
            f"Sending notification to "
            f"{recipient}: {message}"
        )

        time.sleep(1)

        entry = {
            "recipient": recipient,
            "message": message,
            "timestamp": datetime.now(),
        }

        notification_log.append(entry)

        logger.info(
            f"Notification sent to {recipient}"
        )

    except Exception as e:
        logger.error(
            f"Error sending notification to "
            f"{recipient}: {e}"
        )


# ---------------------------------------------------------
# POST /reports
# ---------------------------------------------------------
@router.post("")
def create_report(
    payload: ReportRequest,
    background_tasks: BackgroundTasks,
):

    report_id = len(reports) + 1

    reports[report_id] = {
        "id": report_id,
        "type": payload.report_type,
        "rows": payload.rows,
        "status": "pending",
        "created_at": datetime.now(),
        "completed_at": None,
    }

    logger.info(
        f"Received report request "
        f"{payload.report_type}"
    )

    background_tasks.add_task(
        generate_report,
        report_id,
        payload.report_type,
        payload.rows,
    )

    background_tasks.add_task(
        send_notification,
        recipient="user@example.com",
        message=(
            f"Your report is being generated: "
            f"{report_id}"
        ),
    )

    return {
        "message": "Report generation started",
        "report_id": report_id,
        "status": "pending",
    }


# ---------------------------------------------------------
# GET /reports/{report_id}
# ---------------------------------------------------------
@router.get("/{report_id}")
def get_report(report_id: int):

    logger.info(
        f"Fetching report {report_id}"
    )

    report = reports.get(report_id)

    if not report:
        raise NotFoundError(
            "Report not found."
        )

    return report


# ---------------------------------------------------------
# POST /reports/notifications
# ---------------------------------------------------------
@router.post("/notifications")
def create_notification(
    recipient: str,
    message: str,
    background_tasks: BackgroundTasks,
):

    logger.info(
        f"Scheduling notification "
        f"to {recipient}"
    )

    background_tasks.add_task(
        send_notification,
        recipient,
        message,
    )

    return {
        "message": "Notification scheduled",
        "recipient": recipient,
        "content": message,
    }


# ---------------------------------------------------------
# GET /reports/notifications/log
# ---------------------------------------------------------
@router.get("/notifications/log")
def get_notification_log():

    logger.info(
        "Fetching notification log"
    )

    return {
        "notifications": notification_log
    }