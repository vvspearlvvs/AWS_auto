#-*- coding: utf-8 -*-
import os
import os.path
import sys
import boto3
import json
import http.client, urllib.request, urllib.parse, urllib.error
import requests
import time
import datetime
import logging

print("lambda test log")

CUSTOMER = os.environ['CUSTOMER']
TOKEN = os.environ['TOKEN'] #bot token
UID = os.environ['UID'] #channel name


def Send_Slack(TOKEN, UID, MSG):
    params = {'token':TOKEN, 'channel': UID, 'text':MSG}
    params = urllib.parse.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = http.client.HTTPSConnection("slack.com")

    conn.request("POST", "/api/chat.postMessage", params, headers)

    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)

    conn.close()

def sendImage(TOKEN, UID, MSG, PATH):
    url = "https://slack.com/api/files.upload";

    slack_params = { "token":TOKEN, "channels":['#cw_slack_test'], "filename":"title.png" }

    r=requests.post(url, params=slack_params, files=PATH)

    print(r.status_code, r.reason, r.content)

def MakeGraph(Title, Namespace, RegionCode, MetricName, Statistic, Dimensions):
    cw = boto3.client('cloudwatch', region_name=RegionCode)

    metric = {
        "metrics": [
            [Namespace, MetricName,]

        ],
        "stat": Statistic,
        "title" : Title,
        "view": "timeSeries",
        "stacked": False,
        "period": 60,
        "width": 600,
        "height": 300,
        "start": "-PT3H",
        "end": "P0D",
        "timezone": "+0900"
    }

    for d in Dimensions: #{'value': 'targetgroup/web-ebl2/606ae8d6296dc31a', 'name': 'TargetGroup'}
        metric['metrics'][0].append(d['name'])
        metric['metrics'][0].append(d['value'])

    #stat = { "stat": Statistic }
    #metric['metrics'][0].append(stat)

    metric=json.dumps(metric)
    response = cw.get_metric_widget_image(MetricWidget=metric, OutputFormat='png')
    png = response['MetricWidgetImage']

    imgfile = {'file': png}
    return imgfile

def lambda_handler(event, context):

    print("########## TEST EVENT ######")
    print(event)
    EventSubscriptionArn = event['Records'][0]['EventSubscriptionArn']
    RegionCode = EventSubscriptionArn.split(":")[3]
    msg = event['Records'][0]['Sns']['Message']
    Message = event['Records'][0]['Sns']['Message']
    Message = json.loads(msg)

    AlarmName = Message['AlarmName']
    Description = Message['AlarmDescription']
    Region = Message['Region']
    NewStateReason = Message['NewStateReason']
    StateChangeTime = Message['StateChangeTime']
    StateChangeTime = time.mktime(datetime.datetime.strptime(str(StateChangeTime), "%Y-%m-%dT%H:%M:%S.%f+0000").timetuple())
    StateChangeTime = StateChangeTime+32400
    StateChangeTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(StateChangeTime))
    NewStateValue = Message['NewStateValue']

    if NewStateValue == "ALARM":
        NewStateEmoji = "🔴"
    elif NewStateValue == "OK":
        NewStateEmoji = "🔵"
    else:
        NewStateEmoji = "⚪️"
    OldStateValue = Message['OldStateValue']
    if OldStateValue == "ALARM":
        OldStateEmoji = "🔴"
    elif OldStateValue == "OK":
        OldStateEmoji = "🔵"
    else:
        OldStateEmoji = "⚪️"
    Trigger = Message['Trigger']

    if 'Metrics' in Trigger:
        MSG = "["+NewStateEmoji+" "+CUSTOMER+"]\n알람명: "+AlarmName+"\n변경상태: "+OldStateEmoji+" > "+NewStateEmoji+"\n상태변경 시간: "+StateChangeTime+" (한국시간\n리전: "+Region+"\n알람상세: "+NewStateReason
        message_id = Send_Telegram(TOKEN, UID, MSG)
        logger.info(message_id)
    else:
        Namespace = Trigger['Namespace']
        MetricName = Trigger['MetricName']
        Statistic = Trigger['Statistic'].title()
        Dimensions = Trigger['Dimensions']

        try:
            Target = Dimensions[-1]['name']+"="+Dimensions[-1]['value']
        except:
            Target = "None"

        MSG = "["+NewStateEmoji+" "+CUSTOMER+"]\n알람명: "+AlarmName+"\n변경상태: "+OldStateEmoji+" > "+NewStateEmoji+"\n상태변경 시간: "+StateChangeTime+" (한국시간)\n타겟: "+Target+"\n리전: "+Region+"\n알람상세: "+NewStateReason

        Send_Slack(TOKEN, UID, MSG)

        GRAPH = MakeGraph(AlarmName, Namespace, RegionCode, MetricName, Statistic, Dimensions)

        sendImage(TOKEN, UID, MSG, GRAPH)
