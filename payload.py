from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any


class TourniquetDto:
    def __init__(self, id: int, ip: str, name: str, username: str, password: str):
        self.id = id
        self.ip = ip
        self.name = name
        self.username = username
        self.password = password

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data['id'],
            ip=data['ip'],
            name=data['name'],
            username=data['username'],
            password=data['password']
        )

    def to_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "name": self.name,
            "username": self.username,
            "password": self.password
        }


class HikVisionEventType(Enum):
    ADD = "ADD"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class UpdaterDataResponse:
    def __init__(self, employeeId: int, employeeName: Optional[str] = None, image: Optional[str] = None):
        self.employeeId = employeeId
        self.employeeName = employeeName
        self.image = image

    @classmethod
    def from_json(cls, data):
        return cls(
            employeeId=data['employeeId'],
            employeeName=data.get('employeeName'),
            image=data.get('image')
        )


class HikVisionResponse:
    def __init__(self, eventId: int, eventType: HikVisionEventType, tourniquetId: int, data: UpdaterDataResponse):
        self.eventId = eventId
        self.eventType = eventType
        self.tourniquetId = tourniquetId
        self.data = data

    @classmethod
    def from_json(cls, data):
        return cls(
            eventId=data['eventId'],
            eventType=data['type'],
            tourniquetId=data['tourniquetId'],
            data=UpdaterDataResponse.from_json(data['data'])
        )


@dataclass
class TourniquetEmployeeUpdateRequest:
    eventId: int
    success: bool
    error: Any = None
