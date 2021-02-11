import json
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import re
import boto3
from datetime import datetime, timedelta
import time
import http.client
import json


# 리전 참고표 (나중에 별도로 모듈로 분리)
region_dict = {
                "us-east-2": "미국 동부(오하이오)",
                "us-east-1": "미국 동부(버지니아 북부)",
                "us-west-1": "미국 서부(캘리포니아 북부 지역)",
                "us-west-2": "미국 서부(오레곤)",
                "ap-east-1": "아시아 태평양(홍콩)",
                "ap-south-1": "아시아 태평양(뭄바이)",
                "ap-northeast-3": "아시아 태평양(오사카-로컬)",
                "ap-northeast-2": "아시아 태평양(서울)",
                "ap-southeast-1": "아시아 태평양(싱가포르)",
                "ap-southeast-2": "아시아 태평양(시드니)",
                "ap-northeast-1": "아시아 태평양(도쿄)",
                "ca-central-1": "캐나다(중부)",
                "eu-central-1": "유럽(프랑크푸르트)",
                "eu-west-1": "유럽(아일랜드)",
                "eu-west-2": "유럽(런던)",
                "eu-west-3": "유럽(파리)",
                "eu-north-1": "유럽(스톡홀름)",
                "me-south-1": "중동(바레인)",
                "sa-east-1": "남아메리카(상파울루)",
                "global": "글로벌"
            }


# 서비스 참고표 (나중에 별도로 모듈로 분리)
product_dict = {
                "apigateway": "Amazon API Gateway",
                "appstream2": "Amazon AppStream 2.0",
                "athena": "Amazon Athena",
                "chime": "Amazon Chime",
                "clouddirectory": "Amazon Cloud Directory",
                "cloudfront": "Amazon CloudFront",
                "cloudsearch": "Amazon CloudSearch",
                "cloudwatch": "Amazon CloudWatch",
                "cognito": "Amazon Cognito",
                "comprehend": "Amazon Comprehend",
                "connect": "Amazon Connect",
                "dlm": "Amazon Data Lifecycle Manager",
                "detective": "Amazon Detective",
                "docdb": "Amazon DocumentDB",
                "dynamodb": "Amazon DynamoDB",
                "ec2": "Amazon Elastic Compute Cloud",
                "ecr": "Amazon Elastic Container Registry",
                "ecs": "Amazon Elastic Container Service",
                "elasticfilesystem": "Amazon Elastic File System",
                "eks": "Amazon Elastic Kubernetes Service",
                "elb": "Amazon Elastic Load Balancing",
                "emr": "Amazon Elastic MapReduce",
                "elastictranscoder": "Amazon Elastic Transcoder",
                "elasticache": "Amazon ElastiCache",
                "elasticsearch": "Amazon Elasticsearch Service",
                "events": "Amazon EventBridge",
                "amazonforecast": "Amazon Forecast",
                "freertos": "Amazon FreeRTOS",
                "fsx": "Amazon FSx",
                "gamelift": "Amazon GameLift",
                "glacier": "Amazon Glacier",
                "guardduty": "Amazon GuardDuty",
                "inspector": "Amazon Inspector",
                "kinesis": "Amazon Kinesis Data Streams",
                "firehose": "Amazon Kinesis Firehose",
                "acuity": "Amazon Kinesis Video Streams",
                "lex": "Amazon Lex",
                "lightsail": "Amazon Lightsail",
                "cassandra": "Amazon Managed Apache Cassandra Service",
                "kafka": "Amazon Managed Streaming for Apache Kafka",
                "mq": "Amazon MQ",
                "neptune": "Amazon Neptune",
                "personalize": "Amazon Personalize",
                "pinpoint": "Amazon Pinpoint",
                "polly": "Amazon Polly",
                "qldb": "Amazon Quantum Ledger Database",
                "redshift": "Amazon Redshift",
                "rekognition": "Amazon Rekognition",
                "rds": "Amazon Relational Database Service",
                "route53": "Amazon Route 53",
                "route53domainregistration": "Amazon Route 53 Domain Registration",
                "route53resolver": "Amazon Route 53 Resolver",
                "sagemaker": "Amazon SageMaker",
                "ses": "Amazon Simple Email Service",
                "sns": "Amazon Simple Notification Service",
                "sqs": "Amazon Simple Queue Service",
                "s3": "Amazon Simple Storage Service",
                "swf": "Amazon Simple Workflow Service",
                "simpledb": "Amazon SimpleDB",
                "sumerian": "Amazon Sumerian",
                "transcribe": "Amazon Transcribe",
                "vpc": "Amazon Virtual Private Cloud",
                "workdocs": "Amazon WorkDocs",
                "workspaces": "Amazon WorkSpaces",
                "autoscaling": "Auto Scaling",
                "amplify": "AWS Amplify",
                "appmesh": "AWS App Mesh",
                "applicationdiscoveryservice": "AWS Application Discovery Service",
                "appsync": "AWS AppSync",
                "backup": "AWS Backup",
                "batch": "AWS Batch",
                "billingconsole": "AWS Billing Console",
                "certificatemanager": "AWS Certificate Manager",
                "clientvpn": "AWS Client VPN",
                "servicediscovery": "AWS Cloud Map",
                "cloud9": "AWS Cloud9",
                "cloudformation": "AWS CloudFormation",
                "cloudhsm": "AWS CloudHSM",
                "cloudtrail": "AWS CloudTrail",
                "codebuild": "AWS CodeBuild",
                "codecommit": "AWS CodeCommit",
                "codedeploy": "AWS CodeDeploy",
                "codepipeline": "AWS CodePipeline",
                "codestar": "AWS CodeStar",
                "config": "AWS Config",
                "dataexchange": "AWS Data Exchange",
                "datapipeline": "AWS Data Pipeline",
                "dms": "AWS Database Migration Service",
                "datasync": "AWS DataSync",
                "directconnect": "AWS Direct Connect",
                "directoryservice": "AWS Directory Service",
                "elasticbeanstalk": "AWS Elastic Beanstalk",
                "mediaconnect": "AWS Elemental MediaConnect",
                "mediaconvert": "AWS Elemental MediaConvert",
                "elementalmedialive": "AWS Elemental MediaLive",
                "elementalmediapackage": "AWS Elemental MediaPackage",
                "elementalmediastore": "AWS Elemental MediaStore",
                "mediatailor": "AWS Elemental MediaTailor",
                "fms": "AWS Firewall Manager",
                "globalaccelerator": "AWS Global Accelerator",
                "glue": "AWS Glue",
                "awsgreengrass": "AWS Greengrass",
                "iam": "AWS Identity and Access Management",
                "import-export": "AWS Import/Export",
                "internetconnectivity": "AWS Internet Connectivity",
                "iot1click": "AWS IoT 1-Click",
                "iotanalytics": "AWS IoT Analytics",
                "awsiot": "AWS IoT Core",
                "iotdevicedefender": "AWS IoT Device Defender",
                "awsiotdevicemanagement": "AWS IoT Device Management",
                "iotevents": "AWS IoT Events",
                "thingsgraph": "AWS IoT Things Graph",
                "kms": "AWS Key Management Service",
                "lambda": "AWS Lambda",
                "licensemanager": "AWS License Manager",
                "management-console": "AWS Management Console",
                "marketplace": "AWS Marketplace",
                "migrationhub": "AWS Migration Hub",
                "natgateway": "AWS NAT Gateway",
                "opsworkschef": "AWS OpsWorks for Chef Automate",
                "opsworkspuppet": "AWS OpsWorks for Puppet Enterprise",
                "opsworks": "AWS OpsWorks Stacks",
                "organizations": "AWS Organizations",
                "quicksight": "AWS QuickSight",
                "ram": "AWS Resource Access Manager",
                "resourcegroups": "AWS Resource Groups",
                "resourcegroupstaggingapi": "AWS Resource Groups Tagging API",
                "scretmanager": "AWS Secrets Manager",
                "hub": "AWS Security Hub",
                "serverlessrepo": "AWS Serverless Application Repository",
                "servicecatalog": "AWS Service Catalog",
                "sso": "AWS Single Sign-On",
                "state": "AWS Step Functions",
                "storagegateway": "AWS Storage Gateway",
                "ec2systemsmanager": "AWS Systems Manager",
                "transfer": "AWS Transfer for SFTP",
                "transitgateway": "AWS Transit Gateway",
                "privatelink": "AWS VPCE PrivateLink",
                "awswaf": "AWS WAF",
                "xray": "AWS X-Ray",
                "imagebuilder": "EC2 Image Builder",
            }


# AWS Product 리스트 조회 함수
# 37라인의 product_dict를 대체하려고 하였으나 조회되는 서비스 리스트가 112개밖에 안보임 (지워도 됨)
def service_list():
    svclist = {}
    client = boto3.client('service-quotas')
    results_for_call=50
    response = client.list_services(MaxResults=results_for_call)
    for svc in response['Services']:
        svclist[svc['ServiceCode']] = svc['ServiceName']
    while True:
        # NextToken이 없을때까지 Looping
        if 'NextToken' in response:
            response = client.list_services(MaxResults=results_for_call,NextToken=response['NextToken'])
            for svc in response['Services']:
                svclist[svc['ServiceCode']] = svc['ServiceName']
        else:
            response = client.list_services(MaxResults=results_for_call)
            for svc in response['Services']:
                svclist[svc['ServiceCode']] = svc['ServiceName']
        # NextToken이 더이상 없을 시 Break
        if 'NextToken' not in response:
            break
    return svclist


# AWS Translate 함수 (엑세스 키 사용)
def Translate(text):
    try:
        client = boto3.client('translate')
        response = client.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode='ko')
        res_text = "("+response['TranslatedText']+")"
    except:
        res_text = ''
    return res_text


# 슬랙 메시지 전송 함수
def Send_Slack(MSG):
    connection = http.client.HTTPSConnection('hooks.slack.com')
    headers = {'Content-type': 'application/json'}
    body = {'text': MSG}
    json_body = json.dumps(body)
    connection.request('POST', '/services/T0ADM364S/B011SDWATV5/GmRvZmqZPlCwIPpnuXuPFKED', json_body, headers)
    response = connection.getresponse()
    print(response.read().decode())


# 시간 변환 PDT(태평양시) -> KST (서울시간)으로 변경 함수
def timeConvert(pdt_time):
    try:
        date_time_obj = datetime.strptime(pdt_time, "%a, %d %b %Y %H:%M:%S PDT")
        time_gap = timedelta(hours=16)
        converted_time = str(date_time_obj + time_gap) + " KST"
    except:
        converted_time = pdt_time
    return converted_time


def put_DynamoDB(db_items,msg):
    dynamodb = boto3.resource('dynamodb')
    dbtable = dynamodb.Table('healthcheck')

    response = dbtable.get_item(
        Key={
            'title': db_items['title'],
            'pubDate' : db_items['pubDate']
        }
    )

    if 'Item' not in response.keys():
        dbtable.put_item(Item=db_items)
        Send_Slack(msg)
        #print("### send slack ## ")


def lambda_handler(event, context):
    # TODO implement
    #print("#### 1 minute event ### ")
    feed_url = urlopen('https://status.aws.amazon.com/rss/all.rss')
    tree = ET.parse(feed_url)
    root = tree.getroot()
    if tree.findall('channel/item'):
        for element in tree.findall('channel/item'):
            # 이벤트 제목(key1)
            title = element.findtext('title')
            # 이벤트 개시시간(key2)
            pubDate = element.findtext('pubDate')
    
            # 참고 링크
            guid = element.findtext('guid')
            # guid 값이 http://status.aws.amazon.com/#ec2-ap-northeast-1_1587391740 형식일 경우 정규식 패턴 매치
            if re.match(r"^http:\/\/status.aws.amazon.com\/\#(.*)-(ap|us|ca|eu|me|sa)-([a-z]*)-(\d{1})_(.*)", guid):
                match = re.search('^http:\/\/status.aws.amazon.com\/\#(.*)-(ap|us|ca|eu|me|sa)-([a-z]*)-(\d{1})_(.*)', guid)
                product = match.group(1)
                region = match.group(2)+"-"+match.group(3)+"-"+match.group(4)
            # guid 값이 http://status.aws.amazon.com/#cloudfront_1499437860 형식일 경우 정규식 패턴 매치
            elif re.match(r"^http:\/\/status.aws.amazon.com\/\#(.*)_(.*)", guid):
                match = re.search('^http:\/\/status.aws.amazon.com\/\#(.*)_(.*)', guid)
                product = match.group(1) #value
                region = "global" #value
            # 이도 저도 아닐 경우
            else:
                product = "Service"
                region = "Unknown"
            description = element.findtext('description')
    
            # 리전 코드가 리전 리스트에 있을 경우 리전 이름으로 반환
            if region in region_dict:
                region_name = region_dict[region]
            # 리전 코드가 리전 리스트에 없을 경우 리전코드 그대로 반환
            else:
                region_name = region
    
            # 프로덕트 코드가 리스트에 있을 경우 프로덕트 이름으로 반환
            if product in product_dict:
                product_name = product_dict[product]
            # 프로덕트 코드가 리스트에 있을 경우 프로덕트코드 그대로 반환
            else:
                product_name = product
    
            # PDT에서 KST로 시간 반환
            kst_time = timeConvert(pubDate)
    
    
            # Description에 들어갈 번역본 반환
            translated_description = Translate(description)
            msg = "["+product_name+"]\n리전: "+region+" / "+region_name+"\n내용: "+title+"\n시간: "+kst_time+"\n상세: "+description+" "+translated_description
            #print(msg)
            # 슬랙 메시지 보내기
            #Send_Slack(msg)
    
            #DB에 저장할 items
            db_items ={}
            db_items['title'] = title
            db_items['pubDate'] = pubDate
            db_items['guid'] = guid
            db_items['description'] = description
    
            #DB에 저장
            put_DynamoDB(db_items,msg)



