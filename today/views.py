from django.shortcuts import render
import requests, re, datetime


# Create your views here.
def search(request):
    citys = {"襄阳": "xy_xuzhufei@hb", "荆门": "jm_houqingyang@hb", "宜昌": "yc_xuzhufei@hb", "江汉": "jh_xuzhufei@hb",
             "荆门_本地": "jm_xuzhufei@hb", "江汉_本地": "jh_xuzhufei02@hb", "襄阳_本地": "xy_xuzhufei01@hb",
             "宜昌_本地": "yc_xuzhufei02@hb"}
    if request.method == "GET":
        team = request.GET.get("team", None)
        if team == '0':
            status = []
            now_date = datetime.datetime.now().strftime("%Y-%m-%d")
            for city in citys:
                status.append(doit(city, now_date))
            return render(request,"today_team1.html",{"status":status})
        if team == '2':
            now_date = datetime.datetime.now().strftime("%Y-%m-%d")
            status = doit_team2(now_date)
            return render(request, "today_team2.html", {"status": status})
        else:
            return render(request, "today.html")
    return render(request, "today.html")
def doit(city,now_date):
    citys = {"襄阳": "xy_xuzhufei@hb", "荆门": "jm_houqingyang@hb", "宜昌": "yc_xuzhufei@hb", "江汉": "jh_xuzhufei@hb",
             "荆门_本地": "jm_xuzhufei@hb", "江汉_本地": "jh_xuzhufei02@hb", "襄阳_本地": "xy_xuzhufei01@hb",
             "宜昌_本地": "yc_xuzhufei02@hb"}
    session_request = requests.session()
    login_url='http://134.200.26.196/api/oauth/token'
    result=session_request.post(
                login_url,
                data={
                    'client_id':'app_client',
                    'client_secret':'hollycrm_app_client',
                    'username':'%s'%citys["%s"%city],
                    'password':'Jzyx@0606',
                    'grant_type':'password',
                    'scope':'read write',
                    'errorCnt':'0',
                    'captcha_uid':'',
                    'captcha':'',
                    'deviceId':'',
                    'loginType':''
                },
            headers = dict(referer=login_url)
            )
    body_message=result.content.decode('utf-8')
    access_token=''.join(re.findall('"access_token":"(.*?)",',body_message))
    JSESSIONID = result.cookies.get_dict()['JSESSIONID']

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'access_token': '%s' % access_token,
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=%s' % JSESSIONID,
        'Host': '134.200.26.196',
        'Referer': 'http://134.200.26.196/callrecord/callrecordNew',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 Edg/80.0.361.50'
    }
    req = requests.get(
        "http://134.200.26.196/api/callRecord/showRecordList?handleUser=&handleResult=&startTimeBegin=%s+00:00:00&startTimeEnd=%s+23:00:00&endTimeBegin=&endTimeEnd=&isConn=&qualityResult=&productId=&projectName=&called=&userCode=&mobileNo=&city=&qualityCondition=&deptName=&parentDeptName=&page=1&rows=10"%(now_date,now_date),
        headers=headers)
    call = int(''.join(re.findall('"totalRows":(.*?),', req.content.decode('utf-8'))))
    req = requests.get(
        "http://134.200.26.196/api/callRecord/showRecordList?handleUser=&handleResult=&startTimeBegin=%s+00:00:00&startTimeEnd=%s+23:00:00&endTimeBegin=&endTimeEnd=&isConn=1&qualityResult=&productId=&projectName=&called=&userCode=&mobileNo=&city=&qualityCondition=&deptName=&parentDeptName=&page=1&rows=10" % (
        now_date, now_date),
        headers=headers)
    called = int(''.join(re.findall('"totalRows":(.*?),', req.content.decode('utf-8'))))
    req = requests.get(
        "http://134.200.26.196/api/callRecord/showRecordList?handleUser=&handleResult=agree&startTimeBegin=%s+00:00:00&startTimeEnd=%s+23:00:00&endTimeBegin=&endTimeEnd=&isConn=&qualityResult=&productId=&projectName=&called=&userCode=&mobileNo=&city=&qualityCondition=&deptName=&parentDeptName=&page=1&rows=10" % (
        now_date, now_date),
        headers=headers)
    call_ok = int(''.join(re.findall('"totalRows":(.*?),', req.content.decode('utf-8'))))
    req = {}
    req['city'] = city
    req['call'] = call
    req['called'] = called
    req['ok'] = call_ok
    if call != 0:
        req['jtl'] = str(round((called/call)*100,2)) + "%"
    else:
        req['jtl'] = "0%"
    if call_ok != 0:
        req['cgl'] = str(round((call_ok/called)*100,2)) + "%"
    else:
        req['cgl'] = "0%"
    return req

def doit_team2(now_date):
    citys = {"襄阳": "xy_xuzhufei@hb", "荆门": "jm_houqingyang@hb", "宜昌": "yc_xuzhufei@hb", "江汉": "jh_xuzhufei@hb",
             "荆门_本地": "jm_xuzhufei@hb", "江汉_本地": "jh_xuzhufei02@hb", "襄阳_本地": "xy_xuzhufei01@hb",
             "宜昌_本地": "yc_xuzhufei02@hb"}
    ids = {'宜昌':{'倪礼鑫':'yc_wanghao', '黄曼':'yc_zangmiao'},'荆门':{'倪礼鑫':'jm_lixiaqing', '黄曼':'jm_sunjingyuan'}}
    req = []
    for city in ids:
        for name in ids[city]:
            log_id = ids[city][name]
            session_request = requests.session()
            login_url = 'http://134.200.26.196/api/oauth/token'
            result = session_request.post(
                login_url,
                data={
                    'client_id': 'app_client',
                    'client_secret': 'hollycrm_app_client',
                    'username': '%s' % citys[city],
                    'password': 'Jzyx@0606',
                    'grant_type': 'password',
                    'scope': 'read write',
                    'errorCnt': '0',
                    'captcha_uid': '',
                    'captcha': '',
                    'deviceId': '',
                    'loginType': ''
                },
                headers=dict(referer=login_url)
            )
            body_message = result.content.decode('utf-8')
            access_token = ''.join(re.findall('"access_token":"(.*?)",', body_message))
            JSESSIONID = result.cookies.get_dict()['JSESSIONID']

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'access_token': '%s' % access_token,
                'Connection': 'keep-alive',
                'Cookie': 'JSESSIONID=%s' % JSESSIONID,
                'Host': '134.200.26.196',
                'Referer': 'http://134.200.26.196/callrecord/callrecordNew',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 Edg/80.0.361.50'
            }
            r = requests.get(
                "http://134.200.26.196/api/callRecord/showRecordList?handleUser=&handleResult=&startTimeBegin=%s+00:00:00&startTimeEnd=%s+23:00:00&endTimeBegin=&endTimeEnd=&isConn=1&qualityResult=&productId=&projectName=&called=&userCode=%s&mobileNo=&city=&qualityCondition=&deptName=&parentDeptName=&page=1&rows=10" % (
                    now_date, now_date, log_id),
                headers=headers)
            called = int(''.join(re.findall('"totalRows":(.*?),', r.content.decode('utf-8'))))
            r = requests.get(
                "http://134.200.26.196/api/callRecord/showRecordList?handleUser=&handleResult=agree&startTimeBegin=%s+00:00:00&startTimeEnd=%s+23:00:00&endTimeBegin=&endTimeEnd=&isConn=&qualityResult=&productId=&projectName=&called=&userCode=%s&mobileNo=&city=&qualityCondition=&deptName=&parentDeptName=&page=1&rows=10" % (
                    now_date, now_date, log_id),
                headers=headers)
            call_ok = int(''.join(re.findall('"totalRows":(.*?),', r.content.decode('utf-8'))))
            req1 = []
            req1.append(city)
            req1.append(name)
            req1.append(called)
            req1.append(call_ok)
            if call_ok != 0:
                req1.append(str(round((call_ok / called) * 100, 2)) + "%")
            else:
                req1.append("0%")
            req.append(req1)
    return req

