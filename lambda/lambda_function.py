import json
import os
import requests
from comm_github import *
from comm_tele import *

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

if TELEGRAM_TOKEN is None or GITHUB_TOKEN is None:
    raise ValueError("Required token is not set in environment variables")

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    if 'message' in body:
        chat_id = body['message']['chat']['id']
        command = body['message'].get('text', '')
        if command == '/ec2':
            send_ec2_keyboard(TELEGRAM_TOKEN, chat_id)
        elif command == '/ec2list':
            send_message(TELEGRAM_TOKEN, chat_id, "Please wait ...")
            list_ec2_servers(TELEGRAM_TOKEN, chat_id)

    elif 'callback_query' in body:
        query_data = body['callback_query']['data']
        chat_id = body['callback_query']['message']['chat']['id']
        if "class" in query_data:
            send_instance_details(TELEGRAM_TOKEN, chat_id, query_data.replace("class_", ""))
        elif "type" in query_data:
            if "ond" in query_data:
                send_message(TELEGRAM_TOKEN, chat_id, "Please wait ...\nCreating EC2 On-Demand")
                create_ond_server(GITHUB_TOKEN, chat_id, query_data.replace("type_ond_", ""))
            elif "spot" in query_data:
                send_message(TELEGRAM_TOKEN, chat_id, "Please wait ...\nCreating EC2 Spot")
                create_spot_server(GITHUB_TOKEN, chat_id, query_data.replace("type_spot_", ""))
    return { 'statusCode': 200, 'body': json.dumps('OK') }