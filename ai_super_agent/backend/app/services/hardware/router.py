from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/iot/devices")
async def list_iot_devices():
	# Stub: would query MQTT/MDNS/Zeroconf
	return {"devices": []}


@router.get("/bci/openbci/status")
async def openbci_status():
	# Stub: status placeholder
	return {"connected": False, "ports": []}