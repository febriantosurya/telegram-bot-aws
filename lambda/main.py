import json
import os
import urllib3
from instance_type import EC2_INSTANCE_TYPES

TOKEN = os.environ.get('TOKEN_TELEGRAM')
if TOKEN is None:
    raise ValueError("Telegram bot token is not set in environment variables")

http = urllib3.PoolManager()

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))

    if 'message' in body:
        chat_id = body['message']['chat']['id']
        command = body['message'].get('text', '')

        if command == '/ec2':
            send_ec2_keyboard(chat_id)

    elif 'callback_query' in body:
        # Handle the callback query
        callback_query = body['callback_query']
        chat_id = callback_query['message']['chat']['id']
        instance_type = callback_query['data']  # The instance type selected
        
        send_instance_details(chat_id, instance_type)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }


def send_ec2_keyboard(chat_id):
    # Define the inline keyboard for EC2 instance types
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
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': "Choose an EC2 instance type to view details:",
        'reply_markup': json.dumps(keyboard)
    }
    
    encoded_data = json.dumps(data).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})


def send_instance_details(chat_id, instance_type):
    if instance_type in EC2_INSTANCE_TYPES:
        instance_info = EC2_INSTANCE_TYPES[instance_type]
        response_text = f"**{instance_type}**\n"
        response_text += f"Memory: {instance_info['memory']}\n"
        response_text += f"Storage: {instance_info['storage']}\n"
        response_text += "Pricing:\n"
        for pricing_type, price in instance_info['pricing'].items():
            response_text += f"- {pricing_type}: {price}\n"
        
        # Send the response back to the user
        send_message(chat_id, response_text)
    else:
        send_message(chat_id, "Invalid option selected.")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'  # To enable formatting
    }
    encoded_data = json.dumps(data).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})
