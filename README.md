# Telegram Bot to Provision EC2
This Telegram bot allows users to provision Amazon EC2, leveraging both on-demand and spot instances. It's designed to simplify the process of managing cloud infrastructure directly from Telegram app.

## Features
- Provision EC2 instances using on-demand or spot pricing.
- View the status of running instances.

## Requirements
- Python 3.7 or higher
- AWS SDK for Python (Boto3), requests
- An AWS account with permissions to manage EC2 instances

## Installation

<b>Fork the Repository and change the url in the lambda function to github. Add necessary key (Telegram, GitHub, and AWS Access Key) to AWS Lambda and GitHub Secret Environment. Then, set webhook telegram to lambda function.</b>

<b>Install requests to lambda folder </b>
```
pip3 install requests -t lambda
```

<b>Zip & Upload zip to AWS Lambda</b>
```
zip -r lambda.zip lambda
```

## Usage
<b>List all EC2 Instances</b>
```
/ec2list
```
<b>Create EC2 Server (On-Demand or Spot)</b>
```
/ec2
```
