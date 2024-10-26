import requests

def create_ond_server(gh_token, chat_id, ec2_class):
	url = "https://api.github.com/repos/febriantosurya/telegram-bot-aws/actions/workflows/create_ond_server.yml/dispatches"
	headers = {
		"Accept": "application/vnd.github+json",
		"Authorization": f"Bearer {gh_token}",
		"X-GitHub-Api-Version": "2022-11-28",
		"Content-Type": "application/json"
	}
	data = {
		"ref": "master",
		"inputs":{
			"chat_id": f"{chat_id}",
			"class": f"{ec2_class}"
		}
	}
	requests.post(url, headers=headers, json=data)

def create_spot_server(gh_token, chat_id, ec2_class):
	url = "https://api.github.com/repos/febriantosurya/telegram-bot-aws/actions/workflows/create_spot_server.yml/dispatches"
	headers = {
		"Accept": "application/vnd.github+json",
		"Authorization": f"Bearer {gh_token}",
		"X-GitHub-Api-Version": "2022-11-28",
		"Content-Type": "application/json"
	}
	data = {
		"ref": "master",
		"inputs":{
			"chat_id": f"{chat_id}",
			"class": f"{ec2_class}"
		}
	}
	requests.post(url, headers=headers, json=data)