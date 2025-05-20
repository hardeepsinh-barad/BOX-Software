from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from app.database import get_db
from app import models
from sqlalchemy import select, func

router = APIRouter(prefix="/reason-alert", tags=["reason_alert"])

class ReasonAlertResponse(object):
    total_alerts: int
    alerts_by_reason: Dict[str, int]

@router.get("/")
async def get_reason_alerts(device_uuid: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieves reason alerts for a specific device.
    """
    # Subquery to get the device ID from the device UUID
    device_subquery = select(models.Device.id).where(models.Device.uuid == device_uuid).scalar_subquery()

    # Query to get the total alert count for the device
    total_alerts_query = select(func.count(models.DeviceReasonLog.id)).where(models.DeviceReasonLog.device_id == device_subquery)
    total_alerts = await db.execute(total_alerts_query)
    total_alerts = total_alerts.scalar() or 0

    # Query to get the alert counts grouped by reason name
    alerts_by_reason_query = (
        select(models.Reason.reason, func.count(models.DeviceReasonLog.id))
        .join(models.DeviceReasonLog, models.Reason.id == models.DeviceReasonLog.reason_id)
        .where(models.DeviceReasonLog.device_id == device_subquery)
        .group_by(models.Reason.reason)
    )
    alerts_by_reason_result = await db.execute(alerts_by_reason_query)
    alerts_by_reason = dict(alerts_by_reason_result.all())

    return {
        "total_alerts": total_alerts,
        "alerts_by_reason": alerts_by_reason,
    }
