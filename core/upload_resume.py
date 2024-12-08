import json
import boto3


def handler(event, context):
	body = json.loads(event["body"])

	username = body["username"]
	resume = body["resume"]
	job = body["job"]
	jobId = body["jobId"]

	sqs_message = {
		"username": username,
		"resume": resume,
		"job": job,
		"jobId": jobId,
	}
	sqs_client = boto3.client('sqs')
	sqs_client.send_message(
		QueueUrl="https://sqs.us-east-1.amazonaws.com/147997152608/rank-my-resume-sqs-upload",
		MessageBody=json.dumps(sqs_message)
	)

	return {
		"statusCode": 200,
		"body": json.dumps({
			"message": "SQS message sent successfully",
		})
	}
