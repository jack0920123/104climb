import requests
import bs4
import json
import csv
import random,time
import re
import datetime

today = datetime.date.today()
search = input('請輸入要找的資料:')
link_page = int(input('請輸入要找幾頁:'))
file_name = input('請輸入想建立檔案名:')
url_A =f'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={search}&order=15&asc=0&page='
url_B = '&mode=s&jobsource=2018indexpoc'

all_job_datas=[]
for page in range(1,link_page+1):
    url = url_A+str(page)+url_B
    print(url)
    htmlFile = requests.get(url)
    ObjSoup=bs4.BeautifulSoup(htmlFile.text,'html.parser')
    jobs = ObjSoup.find_all('article',class_='js-job-item')#搜尋所有職缺

    for job in jobs:
        job_name = job.find('a', class_="js-job-link").text  # 職缺內容
        job_company = job.get('data-cust-name')  # 公司名稱
        job_loc = job.find('ul', class_='job-list-intro').find('li').text  # 地址
        job_pay = job.find('span', class_='b-tag--default').text  # 薪資
        job_url = job.find('a').get('href')  # 網址

        material = job.find('a').get('href').split('/')[4].split('?')[0]#擷取不同網頁的代號
    #######################################################################
        url = f'https://www.104.com.tw/job/ajax/content/{material}'
        res = requests.get(url, headers={
            "Referer": f"https://www.104.com.tw/job/{material}?jobsource=hotjob_chr"

        })

        # print(res.text)

        jsonData = res.json()

        custName = jsonData["data"]["header"]["custName"]
        jobname = jsonData["data"]["header"]["jobName"]
        edu = jsonData["data"]["condition"]["edu"]
        salary = jsonData["data"]["jobDetail"]["salary"]
        vacation = jsonData["data"]["jobDetail"]["vacationPolicy"]
        workexp = jsonData["data"]["condition"]["workExp"]
        others = jsonData["data"]["condition"]["other"]
        other =re.sub(r"\s+", "", others)
        describe=re.sub(r"\s+", "", jsonData["data"]["jobDetail"]["jobDescription"])
        skill = []
        for i in jsonData["data"]["condition"]["specialty"]:
             skill.append(i['description'])
            # print(i['description'])                    #所需技巧
        # print(jsonData["data"]["header"]["custName"])  #公司名稱
        # print(jsonData["data"]["header"]["jobName"])   #工作名稱
        # print(jsonData["data"]["jobDetail"]["salary"]) #薪水
        # print(jsonData["data"]["jobDetail"]["vacationPolicy"]) #休假
        # print('=' * 70)

        job_data = {'職缺內容': job_name,
                    '公司名稱': job_company,
                    '地址': job_loc,
                    '薪資': job_pay,
                    '網址': job_url,
                    '教育程度': edu,
                    '所需技能': skill,
                    '工作經驗': workexp,
                    '工作描述': describe,
                    '其他描述': other,
                    '休假模式':vacation}
        all_job_datas.append(job_data)
    time.sleep(random.randint(1, 3))

####################################################################
fn=f'{today}-104人力銀行職缺內容_{file_name}.csv'                                             #取CSV檔名
columns_name=['職缺內容','公司名稱','地址','薪資','網址','教育程度','所需技能','工作經驗','工作描述','其他描述','休假模式']                     #第一欄的名稱
with open(fn,'w',newline='',encoding='utf_8_sig') as csvFile:               #定義CSV的寫入檔,並且每次寫入完會換下一行
    dictWriter = csv.DictWriter(csvFile,fieldnames=columns_name)            #定義寫入器
    dictWriter.writeheader()
    for data in all_job_datas:
        dictWriter.writerow(data)
