import time
from datetime import datetime
import random
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#project id对应项目，需自己获取，默认位miYoSummer 2nd的id
project_id='68575'

def get_bili_status():

    url=f'https://show.bilibili.com/api/ticket/project/get?version=134&id=68575&project_id={project_id}'
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer':'https://show.bilibili.com/platform/detail.html?id=68575&from=pc_search',
        'Accept-Encoding' : "gzip, deflate, br"
    }

    try:
        responce=requests.get(url,headers=header)
        responce=responce.json()
        return responce
    except Exception as e:
        print("接口请求错误")
        print(e)
        return 'error'

def mail_sender(text,subject):
    sender = '@qq.com'  # 发件人邮箱
    #receiver = '903238891@qq.com'  # 收件人邮箱 单收件人
    receiver = ['1111@qq.com', '11111@qq.com'] #收件人邮箱，多收件人
    sender1='@qq.com'  #发件人邮箱
    mail_pass = ''  # 邮箱授权码

    # text为邮件正文内容，plain为文本格式，'utf-8'为编码格式
    #text = '还不快去抢'
    message = MIMEText(text, 'plain', 'utf-8')

    # 添加Header信息，From，To，Subject分别为发送者信息，接收者消息和邮件主题
    message['From'] = Header(sender1)
    #message['To'] = Header(receiver, 'utf-8')
    message['To'] = ','.join(receiver)
    #subject = '有票啦！！！！'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        # smtp.xxx.com为邮箱服务类型，25为STMP的端口
        #smtpObj = smtplib.SMTP('smtp.qq.com', 25)  # smtp.xxx.com为邮箱服务类型，25为STMP
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com'.encode(), '465')

        smtpObj.login(sender, mail_pass)  # 登录
        smtpObj.sendmail(sender, receiver, message.as_string())  # 发送
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("邮件发送失败")

error_times=0


while(True):

    status=get_bili_status()
    if status == 'error' :
        mail_sender('接口出问题啦','接口出问题啦')
        error_times=error_times+1
        sleep_time=error_times * 1200
        time.sleep(sleep_time)

    now = datetime.now()
    current_hour=now.strftime("%H")
    current_time = now.strftime("%H:%M:%S")
    error_times=0

    try:
        if status['data']['sale_flag'] != '不可售' :  #每个项目不一样，具体可能需要根据状态更换
            print('---------------------------------------------')
            print('状态变啦！！！！！！！')
            print('---------------------------------------------')
            mail_sender('有票啦！！！！！','还不快去抢！')
            time.sleep(120)
    except Exception as e:
        print(e)

    #进入规定时间高频模式
    if current_hour == '17' or current_hour == '18' or current_hour == '19' :
        sleep_time_high=random.randint(0,10)
        print('当前时间：', current_time, '场次为：',status['data']['screen_list'][1]['name'],"场次状态",status['data']['screen_list'][1]['ticket_list'][0]['clickable'],'状态为：', status['data']['sale_flag'],'休息：',sleep_time_high,'s   ', '高频模式')
        time.sleep(sleep_time_high)
        continue

    #其他时间进入低频模式
    sleep_time_low=random.randint(0, 60)
    print('当前时间：', current_time, '场次为：',status['data']['screen_list'][1]['name'],"场次状态",status['data']['screen_list'][1]['ticket_list'][0]['clickable'],'状态为：',status['data']['sale_flag'], '休息：', sleep_time_low, 's   ',
          '低频模式')

    #设置低频时间段睡眠30s内，防止IP被封
    time.sleep(sleep_time_low)

