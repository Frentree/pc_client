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

    # for path in paths:
    #     tmp.append({"id": locations, "subpath": path})

    # tJson['targets']['locations'].append({"id": "8987302884414283716", "subpath": "\\usr\\"})
    # print(tJson['targets']['locations'])


    # appointment1 = {'soccer': {
    #     'day': 20,
    #     'month': 'april'
    # }
    #
    # }
    # appointment2 = {
    #     'gym': {
    #         'day': 5,
    #         'month': 'may'
    #     }
    # }
    # appointment = {**appointment1, **appointment2}
    # print(appointment)


    # targets를 만들어 넣으면 locations가 덮어씌여 지기 때문에
    # locations를 만드는 것으로 접근
    # for path in paths:
    #     print(path)
    #     tmp = [{"targets": [{"id": target_id,
    #               "locations":
    #                   [{"id": locations, "subpath": path},]}]}]
    #     # update
    #     # tJson = {**tJson, **tmp}
    #     print(tmp)
    #     tJson.update(tmp)
    #     print(tJson)

    # locations 만들어서 targets에 넣는 방향
    # a = {}
    # d = defaultdict(lambda: defaultdict(list))
    # for path in paths:
    #     tmp = {"locations": [{"id": locations, "subpath": path},]}
    #     print(tmp)
    #     # a = {**a, **tmp}
    #     d['a'].append(tmp)
    #     print(a)

    # switches = {'s1': {'port1': [[0, 0, 0], [1, 1, 1]], 'port2': [2, 2, 2]}}
    # d = defaultdict(lambda: defaultdict(list))
    # d['s1']['port1'].append([{"id": locations, "subpath": "test"}])
    # d['s1']['port1'].append([{"id": locations, "subpath": "test2"}])
    # d['s1']['port2'].append([2, 2, 2])
    # print(d)
    # print(json.dumps(d))


    # print({**tmpJson, **tmp})

    # while paths:
    #     tmp.append(
    #         '{"id": ' +
    #         locations +
    #         "," +
    #         '"subpath": ' +
    #         paths.pop() +
    #         '},'
    #     )


    # print(paths)
    # print(tmp)
    # tmp = str(tmp).replace(",'", "").replace("'{", "{")
    # print(tmp)


    # tJson["targets"] = '[{' + ""'"' + 'id' + ""'"' + ": " + '"' + target_id + '"' + ',' \
    #                    + '"locations" :' \
    #                    + tmp \
    #                    + '}],'



    # print(tJson)
    print(tJson)
    return tJson


def er_api(paths):
    api = Api()

    # api.post("/schedules", tmpJson)

    # groups = api.get("/groups/all")

    # print(groups)
    # print(type(groups))

    # jsonGroups = json.dumps(groups)
    # print(jsonGroups)
    # print(type(jsonGroups))

    # test = ['{"id": 8987302884414283716,"subpath": C:\\\\Windows\\System32\\spp\\store\\2.0\\data.dat},', '{"id": 8987302884414283716,"subpath": C:\\\\Program Files\\AhnLab\\Safe Transaction\\MeD\\Definition\\mdp.asd},', '{"id": 8987302884414283716,"subpath": C:\\\\Users\\junhyun\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network Persistent State},']
    # print(test.pop())

    # api.cancelScheduledByTargetId()

    if paths:
        api.post("/schedules", set_targets(paths))
        # set_targets(hostname, start, paths)

"""
Json 수정 내용

label,
targets(target_id, location_id and subpath),
profiles(Django API 생성 후)
start
"""
