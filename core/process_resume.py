import io
import json
import base64
import boto3
from pypdf import PdfReader


def handler(event, context):
	body = json.loads(event["Records"][0]["body"])

	username = body["username"]
	resume = base64.b64decode(body["resume"])
	job = base64.b64decode(body["job"]).decode('utf-8')
	jobId = body["jobId"]
	jobOrg = body["jobOrg"]

	resume = io.BytesIO(resume)
	resume = PdfReader(resume)
	page_count = len(resume.pages)
	extracted_text = ""

	for i in range(page_count):
		page = resume.pages[i]
		extracted_text += page.extract_text()

	resume = {
		"resume": extracted_text,
		"job": job,
	}
	json.dump(resume, open("/tmp/resume.json", "w"), indent=4)

	s3_client = boto3.client('s3')
	s3_client.upload_file("/tmp/resume.json", "rank-my-resume-s3", f"{username}-{jobOrg}-{jobId}.json")
