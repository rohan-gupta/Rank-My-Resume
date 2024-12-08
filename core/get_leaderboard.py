import json
import boto3


def handler(event, context):
	bucket_name = "rank-my-resume-s3"
	s3_client = boto3.client('s3')
	response = s3_client.list_objects_v2(Bucket=bucket_name)

	text_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.txt')]

	results = []

	for file_name in text_files:
		obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
		score = obj['Body'].read().decode('utf-8')

		username, jobOrg, jobid = file_name.split(".")[0].split("-")

		results.append({
			"username": username,
			"jobOrg": jobOrg,
			"jobId": jobid,
			"score": score,
		})

	sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)

	return {
		"statusCode": 200,
		"body": json.dumps(sorted_results)
	}
