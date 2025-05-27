from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Any
from app.database import get_db
from app import models
from sqlalchemy import select, func
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reason-alert", tags=["reason_alert"])

class ReasonAlertResponse(object):
    total_alerts: int
    alerts_by_reason: Dict[str, int]
    analytics: List[Dict[str, Any]]  # Add analytics field

@router.get("/")
async def get_reason_alerts(device_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves reason alerts for a specific device.
    """
    try:

        # Query to get the total alert count for the device
        total_alerts_query = select(func.count(models.DeviceReasonLog.id)).where(models.DeviceReasonLog.device_id == device_id)
        total_alerts_result = await db.execute(total_alerts_query)
        total_alerts = total_alerts_result.scalar() or 0
        print(f"Total alerts for device {device_id}: {total_alerts}")
        # Query to get the alert counts grouped by reason name
        alerts_by_reason_query = (
            select(models.Reason.reason, func.count(models.DeviceReasonLog.id))
            .join(models.DeviceReasonLog, models.Reason.id == models.DeviceReasonLog.reason_id)
            .where(models.DeviceReasonLog.device_id == device_id)
            .group_by(models.Reason.reason)
        )
        alerts_by_reason_result = await db.execute(alerts_by_reason_query)
        alerts_by_reason = dict(alerts_by_reason_result.all())

        # Analytics: Most frequent alerts
        most_frequent_alerts = []
        if alerts_by_reason:
            most_frequent_reason = max(alerts_by_reason, key=alerts_by_reason.get)
            most_frequent_count = alerts_by_reason[most_frequent_reason]
            most_frequent_alerts.append({
                "reason": most_frequent_reason,
                "count": most_frequent_count,
            })

        # Placeholder for other analytics reports
        other_analytics = [
            {"report_name": "Example Report", "value": "Some Value"}
        ]

        analytics = [
            {"type": "most_frequent_alerts", "data": most_frequent_alerts},
            # {"type": "other_analytics", "data": other_analytics},
        ]

        return {
            "total_alerts": total_alerts,
            "alerts_by_reason": alerts_by_reason,
            "analytics": analytics,
        }
    except Exception as e:
        logger.error(f"Error getting reason alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve reason alerts")
