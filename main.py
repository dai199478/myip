import os
import requests
import re


def get_ip_by_ip138():
    response = requests.get("http://2018.ip138.com/ic.asp")
    ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response.content.decode(errors='ignore')).group(0)
    return ip


if __name__ == '__main__':
    ip = get_ip_by_ip138()
    print("本机的ip地址为:", ip)
    open('ip.txt', 'w').write(ip)
    os.chdir(os.getcwd())
    os.system('git push')

