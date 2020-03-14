from django.shortcuts import render
import pymysql, datetime

# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def set(request):
    if request.method == "GET" and request.GET.get("f5",None) == "1":
        f = open('static/data', 'r')  # 打开文件
        req = f.read()  # 读取文件内容
        for i in range(-7,0):
            date = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            if date not in req:
                reload_data(date)
        req = req.replace("None", "0")
        req = req.split("\n")
        status = req
        f.close()
    else:
        status = "None"
    return render(request, "set.html",{"status":status})

def reload_data(date):
    conn = pymysql.connect(host='123.207.121.89', port=3306, user='fei', passwd='ddd123', db='hd', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    # 执行SQL，并返回收影响行数
    cursor.execute("""SELECT 
COUNT(IF(`用户意向`='成功',TRUE,NULL)) as '成功',
CONCAT(ROUND(COUNT(IF(`用户意向`='成功',TRUE,NULL))/COUNT(IF(`接通状态`='已接通',TRUE,NULL)) * 100 ,1),'%%') as '成功率'
FROM `%d月外呼记录`
WHERE `通话时间` LIKE '%s%%'
AND `任务` <> "" """ %(int(date.split("-")[1]), date))
    # 获取所有记录列表
    results = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    with open('static/data', 'a') as ff:
        ff.write((date + "," + str(results[0][0]) + "," + str(results[0][1]) + "\n"))
        ff.close()