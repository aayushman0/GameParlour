from db.models import session, Device
from datetime import datetime


def create(name: str, is_running: bool, start_time: datetime, max_time: int) -> Device:
    device = Device(name, is_running, start_time, max_time)
    session.add(device)
    session.commit()
    return device


def edit(name: str, is_running: bool, start_time: datetime, max_time: int, new_name: str | None = None) -> Device | None:
    device: Device | None = session.query(Device).filter(Device.name == name).scalar()
    if not device:
        return None
    if new_name:
        device.name = new_name
    device.is_running = is_running
    device.start_time = start_time
    device.max_time = max_time
    session.commit()
    return device


def delete(name: str) -> None:
    device: Device | None = session.query(Device).filter(Device.name == name).scalar()
    if not device:
        return None
    session.delete(device)
    session.commit()


def get_all() -> list[Device]:
    return session.query(Device)


def get_by_name(name: str) -> Device | None:
    return session.query(Device).filter(Device.name == name).scalar()
