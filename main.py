import os
import requests
import re

import time


def get_ip_by_ip138():
    response = requests.get("http://2018.ip138.com/ic.asp")
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
<h1 style="color:red">Hello World.</h1>
</body>
</html>
'''.format(ip, port)

    return html

def genCommit(ip):
    html = getHtml(ip, '4567');
    open('index.html', 'w').write(html)

    curtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
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
    while True:
        count += 1
        ip = get_ip_by_ip138()
        if ip == "":
            ip = lastIp

        print("查询第%d本机的ip地址为:" % count, ip)
        if lastIp == ip:
            time.sleep(10)
        else:
            genCommit(ip)
        lastIp = ip
