import requests
import json
import socket
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

URL = "https://192.168.0.160:8339/beta"
HOSTNAME = socket.gethostname()


class Api:

    # noinspection PyMethodMayBeStatic
    def get(self, url):
        url = URL + url
        res = requests.get(url,
                           auth=("admin", "fren1212"),
                           verify=False)
        return res.json()

    # noinspection PyMethodMayBeStatic
    def getSchedules(self, url):
        print(url)
        res = requests.get(url,
                           auth=("admin", "fren1212"),
                           verify=False)
        print(res)
        print(res.text)
        print(res.json())

        return res.json()

    # noinspection PyMethodMayBeStatic
    def post(self, url, params):
        params = json.dumps(params)
        url = URL + url
        res = requests.post(url,
                            auth=("admin", "fren1212"),
                            verify=False,
                            data=params,
                            headers={'Content-type': 'application/json'})

    # noinspection PyMethodMayBeStatic
    def postWithoutParams(self, url):
        print(url)
        res = requests.post(url,
                            auth=("admin", "fren1212"),
                            verify=False,
                            headers={'Content-type': 'application/json'})
        print(res.text)


    # noinspection PyMethodMayBeStatic
    def cancelScheduledByTargetId(self):
        print("cancel Scheduled By TargetId has been called")
        jSon = self.getSchedules(URL+"/schedules?scheduled=true&limit=100000")

        for i in range(len(jSon)):
            for target in jSon[i]['targets']:
                if target['name'] == HOSTNAME:
                    print(jSon[i]['id'])
                    self.cancelSchedule(jSon[i]['id'])

        print("cancel Scheduled By TargetId has been finished")


    def cancelSchedule(self, schedule_id):
        url = URL + "/schedules/" + schedule_id + "/cancel"
        self.postWithoutParams(url)


scanStartFormat = {
    "label": "ER_PC Client Test",
    "targets": "",
    "profiles": [
        "1",
        "10",
        "13"
    ],
    "start": "2022-04-23 19:20",
    "timezone": "Default",
    "repeat_days": 0,
    "repeat_months": 0,
    "cpu": "low",
    "throughput": 0,
    "memory": 0,
    "capture": "true",
    "trace": "true",
}
mark = b'\xe2\x80\x99'.decode("utf8")


def set_targets(paths):
    api = Api()
    hostname = socket.gethostname()
    result = api.get("/groups/all")

    for i in range(len(result)):
        for target in result[i]['targets']:
            if target['name'] == hostname:
                for j in range(len(target['locations'])):
                    if target['locations'][j]['description'] == "All local files":
                        target_id = target['id']
                        location_id = target['locations'][j]['id']
                        break
                break
    tJson = json.loads(json.dumps(scanStartFormat))

    for i in range(len(paths)):
        paths[i] = {'id': location_id, 'subpath': paths[i]}

    tJson['targets'] = {'id': target_id, 'locations': paths}
    tJson["label"] = hostname + " " + datetime.datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))
    tJson["start"] = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M')

    print(tJson)
    return tJson


def er_api(paths):
    api = Api()

    # 스케줄 실행
    # if paths:
    #     api.post("/schedules", set_targets(paths))

    # 스케줄 삭제
    api.cancelScheduledByTargetId()