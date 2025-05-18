import json

import requests
from flask import Flask, request, jsonify
from requests.auth import HTTPDigestAuth, HTTPBasicAuth

from exceptions import HikBaseException
from payload import TourniquetDto, HikVisionResponse, HikVisionEventType
from utils import check, headers, person, url, person_delete, files, add_event, search_payload, tourniquet_data, \
    delete_person

app = Flask(__name__)

users = {
    "admin": "secret"
}
HR_HOOK_APP_URL = "https://hrpro.uz/api/v1/hook"
TOURNIQUETS_URL = HR_HOOK_APP_URL + "/tourniquets"
SYNCHRONIZE_URL = HR_HOOK_APP_URL + "/synchronize"


# @auth.verify_password
# def verify_password(username, password):
#     if username in users and users[username] == password:
#         return username
#
#
@app.errorhandler(HikBaseException)
def handle_hik_base_exception(error):
    response = jsonify(error.error)
    response.status_code = 400
    return response


@app.errorhandler(requests.exceptions.ConnectionError)
def handle_connection_error(error):
    response = {
        "error": "Connection failed",
        "message": str(error)
    }
    return jsonify(response), 400


# @auth.error_handler
# def unauthorized():
#     return jsonify({'error': 'Unauthorized access'}), 401


# @app.route('/api/v1/person/count/', methods=['POST'])
# def person_count():
#     api_path = "/ISAPI/AccessControl/UserInfo/Count?format=json"
#     request_data = request.get_json(silent=True)
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     response = requests.request(method="GET", url=url, auth=HTTPDigestAuth(username, password))
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)


# @app.route('/api/v1/person/', methods=['POST'])
# # @auth.login_required
# def search():
#     api_path = "/ISAPI/AccessControl/UserInfo/Search?format=json"
#     request_data = request.get_json(silent=True)
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     payload = json.dumps(request_data['payload'], indent=4)
#     response = requests.request(method="POST", url=url, data=payload, headers=headers,
#                                 auth=HTTPDigestAuth(username, password), verify=False)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)


# @app.route("/api/v1/person/add/", methods=['POST'])
# # @auth.login_required
# def add_person():
#     api_path = "/ISAPI/AccessControl/UserInfo/Record?format=json"
#     request_data = request.get_json(silent=True)
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     p = {
#         "UserInfo": {
#             "employeeNo": request_data['payload']['UserInfo']['employeeNo'],
#             "name": request_data['payload']['UserInfo']['name'],
#             "userType": "normal",
#             "Valid": {
#                 "enable": False,
#                 "beginTime": "2024-07-04T00:00:00",
#                 "endTime": "2034-07-04T23:59:59",
#                 "timeType": "local"
#             },
#             "doorRight": "1",
#             "RightPlan": [
#                 {
#                     "doorNo": 1,
#                     "planTemplateNo": "1"
#                 }
#             ],
#             "gender": "unknown",
#             "localUIRight": False,
#             "maxOpenDoorTime": 0,
#             "userVerifyMode": "",
#             "groupId": 1,
#             "userLevel": "Employee",
#             "password": ""
#         }
#     }
#     print(json.dumps(p, indent=4))
#     response = requests.request(method="POST", url=url, data=json.dumps(p, indent=4), headers=headers,
#                                 auth=HTTPDigestAuth(username, password))
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)


# @app.route("/api/v1/person/edit/", methods=['PUT'])
# @auth.login_required
# def update_person():
#     api_path = "/ISAPI/AccessControl/UserInfo/Modify?format=json"
#     request_data = request.get_json(silent=True)
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     payload = json.dumps(request_data['payload'], indent=4)
#     response = requests.request(method="PUT", url=url, data=payload, headers=headers,
#                                 auth=HTTPDigestAuth(username, password))
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)


# @app.route("/api/v1/person/delete/", methods=['DELETE'])
# # @auth.login_required
# def delete_person():
#     api_path = "/ISAPI/AccessControl/UserInfo/Delete?format=json"
#     request_data = request.get_json(silent=True)
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     delete_ids = request_data['payload']
#     ids = []
#     for delete_id in delete_ids:
#         ids.append({
#             "employeeNo": str(delete_id)
#         })
#
#     payload = {
#         "UserInfoDelCond": {
#             "EmployeeNoList": ids,
#         }
#     }
#     payload = json.dumps(payload, indent=1)
#     response = requests.request(method="PUT", url=url, data=payload, headers=headers,
#                                 auth=HTTPDigestAuth(username, password))
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)


# @app.route("/api/v1/face/check/", methods=['POST'])
# @auth.login_required
# def checkFace():
#     api_path = "/ISAPI/Intelligent/FDLib/FDSearch?format=json"
#     request_data = request.get_json(silent=True)
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     person_id = request_data['payload']
#     payload = {
#         "searchResultPosition": 0,
#         "maxResults": 30,
#         "faceLibType": "blackFD",
#         "FDID": "1",
#         "FPID": str(person_id)
#     }
#     payload = json.dumps(payload, indent=2)
#     response = requests.request(method="POST", url=url, data=payload, headers=headers,
#                                 auth=HTTPDigestAuth(username, password))
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)


# @app.route("/api/v1/face/add/", methods=["POST"])
# # @auth.login_required
# def add_face():
#     api_path = "/ISAPI/Intelligent/FDLib/FaceDataRecord?format=json"
#     request_data = request.form
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     person_id = request_data['person_id']
#     image = request.files.get("img")
#     payload = {'FaceDataRecord': '{"faceLibType":"blackFD","FDID":"1","FPID":"' + str(person_id) + '"}'}
#     files = [
#         ('img', (image.name, image, image.mimetype))
#     ]
#     response = requests.request(method="POST", url=url, data=payload, files=files, headers={},
#                                 auth=HTTPDigestAuth(username, password))
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)


# @app.route("/api/v1/face/delete/", methods=['POST'])
# @auth.login_required
# def delete():
#     api_path = "/ISAPI/Intelligent/FDLib/FDSearch/Delete?format=json&FDID=1&faceLibType=blackFD"
#     request_data = request.get_json(silent=True)
#     uri = request_data['url']
#     url = uri + api_path
#     username = request_data['username']
#     password = request_data['password']
#     check(uri, username, password)
#     person_id = request_data['payload']
#     payload = {
#         "FPID": [
#             {
#                 "value": str(person_id)
#             }
#         ]
#     }
#     payload = json.dumps(payload, indent=3)
#     response = requests.request(method="PUT", url=url, data=payload, headers=headers,
#                                 auth=HTTPDigestAuth(username, password))
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HikBaseException(response.json(), response.status_code)

person_add_path = "/ISAPI/AccessControl/UserInfo/Record?format=json"
person_delete_path = "/ISAPI/AccessControl/UserInfo/Delete?format=json"
person_update_path = "/ISAPI/AccessControl/UserInfo/Modify?format=json"
face_add_path = "/ISAPI/Intelligent/FDLib/FaceDataRecord?format=json"
face_update_path = "/ISAPI/Intelligent/FDLib/FDModify?format=json&FDID=1&faceLibType=blackFD"


@app.route('/api/v1/tourniquets', methods=['GET'])
def get_tourniquets():
    username = request.args.get("username")
    password = request.args.get("password")
    tourniquet_response = requests.get(url=TOURNIQUETS_URL, auth=HTTPBasicAuth(username, password))
    event_list = []

    if tourniquet_response.status_code == 200:
        tourniquets = tourniquet_list(tourniquet_response)
        check_tourniquets(tourniquets)

        for tourniquet in tourniquets:
            employees_response = requests.get(url=f"{HR_HOOK_APP_URL}/{tourniquet.id}",
                                              auth=HTTPBasicAuth(username, password))

            if employees_response.status_code == 200:
                employees_data_list = [HikVisionResponse.from_json(item) for item in employees_response.json()]

                for employee_data in employees_data_list:

                    if employee_data.eventType == HikVisionEventType.ADD.name:
                        add_employees(employee_data, tourniquet, event_list)

                    elif employee_data.eventType == HikVisionEventType.DELETE.name:
                        delete_employees(employee_data, tourniquet, event_list)

                    elif employee_data.eventType == HikVisionEventType.UPDATE.name:
                        update_employees(employee_data, tourniquet, event_list)

            else:
                raise HikBaseException(employees_response.json(), employees_response.status_code)
    else:
        raise HikBaseException(tourniquet_response.json(), tourniquet_response.status_code)

    requests.request(method="PUT", url=HR_HOOK_APP_URL, data=json.dumps(event_list, indent=1),
                     auth=HTTPBasicAuth(username, password), headers=headers)
    return ""


max_capability_path = "/ISAPI/AccessControl/UserInfo/capabilities?format=json"
person_count_path = "/ISAPI/AccessControl/UserInfo/Count?format=json"
person_search_path = "/ISAPI/AccessControl/UserInfo/Search?format=json"


@app.route('/api/v1/synchronize', methods=['POST'])
def synchronize_employees():
    username = request.args.get("username")
    password = request.args.get("password")
    tourniquet_response = requests.get(url=TOURNIQUETS_URL, auth=HTTPBasicAuth(username, password))

    if tourniquet_response.status_code == 200:
        tourniquets = tourniquet_list(tourniquet_response)
        check_tourniquets(tourniquets)
        for tourniquet in tourniquets:
            tourniquet_employees = []
            capability_response = requests.request(method="GET", url=f"{url(tourniquet.ip)}{max_capability_path}",
                                                   auth=HTTPDigestAuth(tourniquet.username, tourniquet.password))
            if capability_response.status_code == 200 and max_capability_exist(capability_response.json()):
                count_response = requests.request(method="GET", url=f"{url(tourniquet.ip)}{person_count_path}",
                                                  auth=HTTPDigestAuth(tourniquet.username, tourniquet.password))
                if count_response.status_code == 200 and count_exist(count_response.json()):
                    maximum = max_capability(capability_response.json())
                    pages = total_pages(count_response.json(), maximum)

                    for page in range(0, pages):
                        payload = search_payload(page, maximum)
                        search_response = requests.request(method="POST",
                                                           url=f"{url(tourniquet.ip)}{person_search_path}",
                                                           data=payload,
                                                           headers=headers,
                                                           auth=HTTPDigestAuth(tourniquet.username,
                                                                               tourniquet.password), verify=False)
                        if search_response.status_code == 200:
                            tourniquet_employees.extend(employees(search_response.json()))
                        else:
                            raise HikBaseException(search_response.json(), search_response.status_code)

                    data = tourniquet_data(tourniquet_employees, tourniquet)
                    synchronize_response = requests.request(method="POST", url=SYNCHRONIZE_URL,
                                                            data=json.dumps(data, indent=4),
                                                            auth=HTTPBasicAuth(username, password), headers=headers)

                    if synchronize_response.json():
                        response = requests.request(method="PUT",
                                                    url=f"{url(tourniquet.ip)}{person_delete_path}",
                                                    data=json.dumps(delete_person(synchronize_response), indent=4),
                                                    headers=headers,
                                                    auth=HTTPDigestAuth(tourniquet.username,
                                                                        tourniquet.password))
                        print(response.status_code)
                else:
                    raise HikBaseException(count_response.json(), count_response.status_code)

            else:
                raise HikBaseException(capability_response.json(), capability_response.status_code)

    else:
        raise HikBaseException(tourniquet_response.json(), tourniquet_response.status_code)

    return ""


def add_employees(employee_data, tourniquet, event_list):
    add_response = requests.request(method="POST", url=f"{url(tourniquet.ip)}{person_add_path}",
                                    data=json.dumps(person(employee_data.data), indent=4),
                                    headers=headers,
                                    auth=HTTPDigestAuth(tourniquet.username, tourniquet.password))

    try:
        if add_response.status_code == 200 or employee_exists(add_response.json()):
            add_face(employee_data, tourniquet, event_list)
        else:
            event_list.append(add_event(employee_data.eventId, False))
    except Exception as e:
        event_list.append(add_event(employee_data.eventId, False, str(e)))


def add_face(employee_data, tourniquet, event_list):
    payload = {
        'FaceDataRecord': '{"faceLibType":"blackFD","FDID":"1","FPID":"' + str(employee_data.data.employeeId) + '"}'}
    face_add_response = requests.request(method="POST", url=f"{url(tourniquet.ip)}{face_add_path}",
                                         data=payload,
                                         files=files(employee_data.data),
                                         headers={},
                                         auth=HTTPDigestAuth(tourniquet.username, tourniquet.password))
    try:
        if face_add_response.status_code == 200 or employee_face_exists(face_add_response.json()):
            event_list.append(add_event(employee_data.eventId, True))
        else:
            event_list.append(add_event(employee_data.eventId, False, str(face_add_response.content)))
    except Exception as e:
        event_list.append(add_event(employee_data.eventId, False, str(e)))


def delete_employees(employee_data, tourniquet, event_list):
    delete_response = requests.request(method="PUT",
                                       url=f"{url(tourniquet.ip)}{person_delete_path}",
                                       data=json.dumps(person_delete(employee_data.data), indent=1),
                                       headers=headers,
                                       auth=HTTPDigestAuth(tourniquet.username,
                                                           tourniquet.password))
    try:
        if delete_response.status_code == 200:
            event_list.append(add_event(employee_data.eventId, True))
        else:
            event_list.append(add_event(employee_data.eventId, False, str(delete_response.content)))
    except Exception as e:
        event_list.append(add_event(employee_data.eventId, False, str(e)))


def update_employees(employee_data, tourniquet, event_list):
    update_response = requests.request(method="PUT",
                                       url=f"{url(tourniquet.ip)}{person_update_path}",
                                       data=json.dumps(person(employee_data.data), indent=4),
                                       headers=headers,
                                       auth=HTTPDigestAuth(tourniquet.username,
                                                           tourniquet.password))
    try:
        if update_response.status_code == 200:
            update_face(employee_data, tourniquet, event_list)
        else:
            event_list.append(add_event(employee_data.eventId, False, str(update_response.content)))
    except Exception as e:
        event_list.append(add_event(employee_data.eventId, False, str(e)))


def update_face(employee_data, tourniquet, event_list):
    payload = {'FaceDataRecord': '{"faceLibType":"blackFD","FDID":"1","FPID":"' +
                                 str(employee_data.data.employeeId) + '"}'}

    face_update = requests.request(method="PUT",
                                   url=f"{url(tourniquet.ip)}{face_update_path}",
                                   data=payload,
                                   files=files(employee_data.data),
                                   headers={},
                                   timeout=10,
                                   auth=HTTPDigestAuth(tourniquet.username,
                                                       tourniquet.password))
    if face_update.status_code == 200:
        event_list.append(add_event(employee_data.eventId, True))
    else:
        event_list.append(add_event(employee_data.eventId, False, str(face_update.content)))


def employee_exists(employee_add_json):
    return 'subStatusCode' in employee_add_json and employee_add_json['subStatusCode'] == 'employeeNoAlreadyExist'


def employee_face_exists(face_add_json):
    return 'subStatusCode' in face_add_json and face_add_json['subStatusCode'] == 'deviceUserAlreadyExistFace'


def max_capability_exist(capability_json):
    return 'UserInfo' in capability_json and 'UserInfoSearchCond' in capability_json['UserInfo'] and 'maxResults' in \
        capability_json['UserInfo']['UserInfoSearchCond'] and '@max' in \
        capability_json['UserInfo']['UserInfoSearchCond']['maxResults']


def max_capability(capability_json):
    return int(capability_json['UserInfo']['UserInfoSearchCond']['maxResults']['@max'])


def count_exist(count_json):
    return 'UserInfoCount' in count_json and 'userNumber' in count_json['UserInfoCount']


def person_count(count_json):
    return int(count_json['UserInfoCount']['userNumber'])


def total_pages(count_json, maximum):
    total_elements = person_count(count_json)
    pages = total_elements // maximum
    if total_elements % maximum > 0:
        pages += 1
    return pages


def check_tourniquets(tourniquet_collection):
    for tourniquet in tourniquet_collection:
        check(url(tourniquet.ip), tourniquet.username, tourniquet.password)


def employees(search_json):
    user_info_list = search_json.get("UserInfoSearch", {}).get("UserInfo", [])
    employee_list = [{"id": int(info.get('employeeNo')), "name": str(info.get('name'))} for info in user_info_list]
    return employee_list


def tourniquet_list(tourniquet_response):
    tourniquets_data = tourniquet_response.json()
    return [TourniquetDto.from_json(item) for item in tourniquets_data]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2222)
