import base64
import json
import tempfile
import uuid

import requests
from requests import ConnectTimeout
from requests.auth import HTTPDigestAuth

from exceptions import HikBaseException


def check(uri: str, username: str, password: str):
    try:
        response = requests.request(method="GET", url=uri + "/ISAPI/Security/userCheck",
                                    auth=HTTPDigestAuth(username, password), timeout=3)
        if response.status_code == 401:
            res = {
                "status_code": 207,
                "message": "username or password incorrect"
            }
            raise HikBaseException(error=res, status_code=207)
    except ConnectTimeout as e:
        res = {
            "status_code": 204,
            "message": "connect timeout"
        }
        raise HikBaseException(error=res, status_code=204)


headers = {
    'Content-Type': 'application/json'
}


def url(ip):
    return f"http://{ip}"


def person(data):
    return {
        "UserInfo": {
            "employeeNo": str(data.employeeId),
            "name": str(data.employeeName),
            "userType": "normal",
            "Valid": {
                "enable": False,
                "beginTime": "2024-07-04T00:00:00",
                "endTime": "2034-07-04T23:59:59",
                "timeType": "local"
            },
            "doorRight": "1",
            "RightPlan": [
                {
                    "doorNo": 1,
                    "planTemplateNo": "1"
                }
            ],
            "gender": "unknown",
            "localUIRight": False,
            "maxOpenDoorTime": 0,
            "userVerifyMode": "",
            "groupId": 1,
            "userLevel": "Employee",
            "password": ""
        }
    }


def person_delete(data):
    ids = [{"employeeNo": str(data.employeeId)}]
    return {
        "UserInfoDelCond": {
            "EmployeeNoList": ids,
        }
    }


def delete_person(synchronize_response):
    return {
        "UserInfoDelCond": {
            "EmployeeNoList": [{'employeeNo': str(employee_id)} for employee_id in synchronize_response.json()],
        }
    }


def files(data):
    image_data = base64.b64decode(data.image)
    with tempfile.NamedTemporaryFile(delete=False) as temp_image_file:
        temp_image_file.write(image_data)
        temp_image_file.flush()
        temp_image_file_path = temp_image_file.name

    return [
        ('img', (temp_image_file_path, open(temp_image_file_path, 'rb'), 'image/jpeg'))
    ]


def search_payload(page, size):
    return json.dumps({
        "UserInfoSearchCond": {
            "searchID": str(uuid.uuid4()),
            "searchResultPosition": page * size,
            "maxResults": size
        }
    }, indent=4)


def add_event(event_id: int, success: bool, error: str = None):
    return {
        "eventId": event_id,
        "success": success,
        "error": error
    }


def tourniquet_data(tourniquet_employees, tourniquet):
    return {
        "tourniquetId": int(tourniquet.id),
        "employees": tourniquet_employees,
    }
