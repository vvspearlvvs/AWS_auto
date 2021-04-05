import json
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    response = ec2_client.describe_instances(
        Filters=[
            {   'Name' : 'tag:AutoStartStop',
                'Values' : ['True']
            },
            {   'Name' : 'instance-state-name',
                'Values' : ['stopped']
            }
        ]
    )

    if not response['Reservations']:
        logger.info("필터로 찾은 인스턴스가 없습니다 ")

    InstanceList = []

    for items_list in response['Reservations']:
        items_list_instances = items_list['Instances'][0]
        items_instanceId = items_list_instances['InstanceId']

        InstanceList.append(items_instanceId)

    logger.info("start instatnce 대상")
    logger.info(InstanceList)

    try:
        ec2_client.start_instances(
            InstanceIds = InstanceList
        )

    except:
        logger.info("Auto stop 할 수 없는 인스턴스의 상태입니다 ")
