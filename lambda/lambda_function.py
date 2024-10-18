import json
import os
import urllib3
import requests
from instance_type import EC2_INSTANCE_TYPES


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

if TELEGRAM_TOKEN is None:
    raise ValueError("Telegram bot token is not set in environment variables")

http = urllib3.PoolManager()

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    if 'message' in body:
        chat_id = body['message']['chat']['id']
        command = body['message'].get('text', '')
        if command == '/ec2':
            send_ec2_keyboard(chat_id)
        elif command == '/ec2list':
            send_message(chat_id, "Please wait ...")
            url = "https://api.github.com/repos/febriantosurya/telegram-bot-aws/actions/workflows/list_server.yml/dispatches"
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json"
            }
            data = {
                "ref": "master",
                "inputs":{
                    "chat_id": f"{chat_id}"
                }
            }
            res = requests.post(url, headers=headers, json=data)

    elif 'callback_query' in body:
        # Handle the callback query
        callback_query = body['callback_query']
        chat_id = callback_query['message']['chat']['id']
        instance_type = callback_query['data']
        send_instance_details(chat_id, instance_type)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }


def send_ec2_keyboard(chat_id):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "t2.micro", "callback_data": "t2.micro"},
                {"text": "t2.small", "callback_data": "t2.small"},
                {"text": "t2.medium", "callback_data": "t2.medium"}
            ]
        ]
    }

    # Send the message with the inline keyboard
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': "Choose an EC2 instance type to view details:",
        'reply_markup': json.dumps(keyboard)
    }
    requests.post(url, json=data)
    # encoded_data = json.dumps(data).encode('utf-8')
    # http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})


def send_instance_details(chat_id, instance_type):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Create On-Demand", "callback_data": "ond_t2.micro"},
                {"text": "Create Spot", "callback_data": "spot_t2.micro"},
            ]
        ]
    }
    if instance_type in EC2_INSTANCE_TYPES:
        instance_info = EC2_INSTANCE_TYPES[instance_type]
        response_text = f"**{instance_type}**\n"
        response_text += f"Memory: {instance_info['memory']}\n"
        response_text += f"Storage: {instance_info['storage']}\n"
        response_text += "Pricing:\n"
        for pricing_type, price in instance_info['pricing'].items():
            response_text += f"- {pricing_type}: {price}\n"
        
        # send_message(chat_id, response_text)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': response_text,
            'reply_markup': json.dumps(keyboard),
            'parse_mode': 'Markdown'
        }
        encoded_data = json.dumps(data).encode('utf-8')
        http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})
    else:
        # send_message(chat_id, "Invalid option selected.")
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': "Invalid option selected.",
            'parse_mode': 'Markdown'  # To enable formatting
        }
        encoded_data = json.dumps(data).encode('utf-8')
        http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'  # To enable formatting
    }
    encoded_data = json.dumps(data).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})