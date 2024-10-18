import requests

def create_ond_server(gh_token, chat_id, ec2_class):
	url = "https://api.github.com/repos/febriantosurya/telegram-bot-aws/actions/workflows/create_server.yml/dispatches"
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

def list_ec2_servers(gh_token, chat_id):
	url = "https://api.github.com/repos/febriantosurya/telegram-bot-aws/actions/workflows/list_server.yml/dispatches"
	headers = {
			"Accept": "application/vnd.github+json",
			"Authorization": f"Bearer {gh_token}",
			"X-GitHub-Api-Version": "2022-11-28",
			"Content-Type": "application/json"
	}
	data = {
			"ref": "master",
			"inputs":{
					"chat_id": f"{chat_id}"
			}
	}
	requests.post(url, headers=headers, json=data)