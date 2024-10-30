import json
import requests
import boto3
from instance_type import *

def send_ec2_keyboard(tele_token, chat_id):
	keyboard = {
		"inline_keyboard": [
			[
				{"text": "t2.micro", "callback_data": "class_t2.micro"},
				{"text": "t2.small", "callback_data": "class_t2.small"},
				{"text": "t2.medium", "callback_data": "class_t2.medium"}
			]
		]
	}

	url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
	data = {
		'chat_id': chat_id,
		'text': "Choose an EC2 instance type to view details:",
		'reply_markup': json.dumps(keyboard)
	}
	requests.post(url, json=data)

def send_instance_details(tele_token, chat_id, instance_type):
	keyboard = {
		"inline_keyboard": [
			[
				{"text": "Create On-Demand", "callback_data": "type_ond_t2.micro"},
				{"text": "Create Spot", "callback_data": "type_spot_t2.micro"},
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
		
		url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
		data = {
			'chat_id': chat_id,
			'text': response_text,
			'reply_markup': json.dumps(keyboard),
			'parse_mode': 'Markdown'
		}
		requests.post(url, json=data)
	else:
		send_message(tele_token, chat_id, "Invalid option selected.")

def send_message(tele_token, chat_id, text):
	url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
	data = {
		'chat_id': chat_id,
		'text': text,
		'parse_mode': 'Markdown'
	}
	requests.post(url, json=data)
	
def list_ec2_servers(tele_token, chat_id):
	instance_info = ""
	ec2 = boto3.client('ec2')
	response = ec2.describe_instances()
	count = 0
	for reservation in response['Reservations']:
		for instance in reservation['Instances']:
			count += 1
			public_ip = instance.get('PublicIpAddress', None)
			instance_name = (instance.get('Tags', [{}])[0].get('Value', 'Unnamed Instance'))
			spot_id = instance.get('SpotInstanceRequestId', None)
			instance_id = instance.get('InstanceId', None)
			if public_ip:
				if spot_id:
					instance_info += f"{count}. _(`{spot_id}`)_-{instance_name} ({public_ip}) > {instance['State']['Name']} \n"
				else:
					instance_info += f"{count}. _(`{instance_id}`)_-{instance_name} ({public_ip}) > {instance['State']['Name']} \n"
			else:
				if spot_id:
					instance_info += f"{count}. _(`{spot_id}`)_-{instance_name} (No Public IP) > {instance['State']['Name']} \n"
				else:
					instance_info += f"{count}. _(`{instance_id}`)_-{instance_name} (No Public IP) > {instance['State']['Name']} \n"

	url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
	if instance_info == "":
		instance_info = "No instance found"
	data = {
		'chat_id': chat_id,
		'text': instance_info,
		'parse_mode': 'Markdown'
	}
	requests.post(url, json=data)