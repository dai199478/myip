import os
import requests
import re
import sys
import time


def get_ip_by_ip138():
    try:
        response = requests.get("http://2018.ip138.com/ic.asp")
    except:
        print("异常1:", sys.exc_info()[0])
        return ""

    result = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response.content.decode(errors='ignore'))
    if result is None:
        return ""

    ip = result.group(0)
    return ip


def getHtml(ip, port):
    html = '''<!doctype html>
<html lang="en">
<script>
    window.location = "http://{}:{}";
</script>
<head>
    <title>Document</title>
</head>
<body>
</body>
</html>
'''.format(ip, port)

    return html


def genCommit(ip):
    html = getHtml(ip, '4567')
    lastHtml = open('index.html', 'r').read()
    print(lastHtml)
    if html == lastHtml:
        print('一样')
        return

    open('index.html', 'w').write(html)

    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log = '{}；当前ip变为：{}'.format(curtime, ip)
    open('log.log', 'a').write(log + '\n')
    print(log)

    os.chdir(os.getcwd())
    os.system('git add index.html')
    os.system('git commit -m "{}"'.format(log))
    os.system('git push')


if __name__ == '__main__':
    lastIp = ""
    count = 0
    sleepTime = 30
    while True:
        count += 1
        ip = get_ip_by_ip138()
        if ip == "" or ip == "192.168.1.5":
            print("异常2：%s" % ip)
            ip = lastIp
            sleepTime = 10

        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print("{}；查询第{}次:".format(curtime, count), ip)
        if lastIp == ip:
            time.sleep(sleepTime)
        else:
            genCommit(ip)
            sleepTime = 30

        lastIp = ip
