from django.shortcuts import render
import requests, re, datetime, json

def search(request):
    status = "200"
    if request.method == "GET":
        log_name = request.GET.get("log_name",None)
        phone_num = request.GET.get("Phone",None)
        if phone_num:
            phone_num = "0" + phone_num
            status = search_jz(log_name,phone_num)

    return render(request,"search.html",{"status":status})

def search_jz(log_name,phone_num):
    start_time = (datetime.datetime.now()+datetime.timedelta(days=-60)).strftime("%Y-%m-%d")
    session_request = requests.session()
    login_url = 'http://134.200.26.196/api/oauth/token'
    result = session_request.post(
        login_url,
        data={
            'client_id': 'app_client',
            'client_secret': 'hollycrm_app_client',
            'username': '%s' %log_name,
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
    req = requests.get(
        "http://134.200.26.196/api/callRecord/showRecordList?handleUser=&handleResult=&startTimeBegin=%s+00:00:00&startTimeEnd=&endTimeBegin=&endTimeEnd=&isConn=&qualityResult=&productId=&projectName=&called=%s&userCode=&mobileNo=&city=&qualityCondition=&deptName=&parentDeptName=&page=1&rows=10" %(start_time,phone_num),
        headers=headers)
    return json.loads(req.text)['content']['rows']
    # call = ''.join(re.findall('"totalRows":(.*?),', req.content.decode('utf-8')))


# Create your views here.
