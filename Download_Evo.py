import requests
from selenium import webdriver
from seleniumwire import webdriver
import json
import os
import time

def out_log(text):
    outF = open("Log_Download.txt", "a")
    text = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()) + ": " + text
    outF.write(text)
    outF.write("\n")
    outF.close()

out_log("Start script")
USERNAME = '@gmail.com'
PASSWORD = ''

driver = webdriver.Chrome()
driver.get('https://sektaschool.ru')
cred = {'email':USERNAME, 'password':PASSWORD}
resp = requests.post('https://backend.sektaschool.ru/api/v2/auth/login', cred)
newcookie = {'name': 'api_token', 'value': resp.json()['data']['token']}
driver.add_cookie(newcookie)

sektaevo = {'url':'https://sektaschool.ru/courses/sektaevo-new/','weeks':10,'days':7}
runner = {'url':'https://sektaschool.ru/courses/kurs-na-press-dlya-begunov-new/','weeks':3,'days':7}
course = {'basename':'sektamama','url':'https://sektaschool.ru/courses/sektamama/','weeks':10,'days':7}
curcourse = course

for week in range(1,mychoice['weeks']+1):
    for day in range(1,mychoice['days']+1):
        coursename = mychoice['url'].rsplit('/', 2)[-2] #example: sektamama
        URL = mychoice['url'] + str(week) + "/" + str(day)
        driver.get(URL)
        time.sleep(2)
        links = []
        for request in driver.requests:
            if request.response:
                if request.url.endswith('m3u8'):
                    links.append(request.url)
        for link in links:
            filename = link[link.find('/'):]
            filename = filename[:filename.find('/',4)]
            filename = filename.replace('/','_') + '_day' + str(day) + ".mp4"
            fullpath = '/users/new/Desktop/Sekta/runner/Week' + str(week) + '/' + filename
            if os.path.isfile(fullpath):
                out_log(fullpath + ' already exist')
            elif os.path.isfile(fullpath + ".part"):
                out_log(fullpath + ' now downloading')
            else:
                out_log("start download " + link)
                os.system('youtube-dl ' + link + ' -o' + fullpath)
                out_log("complete download" + link)
            del driver.requests
driver.close()
out_log("end script")
