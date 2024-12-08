import re
import json
import boto3
import math

from collections import Counter


def count_words(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words (case-insensitive)
    return Counter(words)


def get_bedrock_embedding(text, model_id, region="us-east-1"):
    bedrock_client = boto3.client("bedrock-runtime", region_name=region)
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json"
    )
    return json.loads(response["body"].read())["embedding"]


def calculate_cosine_similarity(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vector1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vector2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def compare_keywords(resume, job):
    resume_word_counts = count_words(resume)
    description_word_counts = count_words(job)

    matches = {word: min(resume_word_counts[word], description_word_counts[word])
               for word in resume_word_counts if word in description_word_counts}

    return sum(matches.values()) / sum(resume_word_counts.values())


def compare_embeddings(resume, job):
    model_id = "amazon.titan-embed-text-v1"
    region = "us-east-1"

    resume_embedding = get_bedrock_embedding(resume, model_id, region)
    jd_embedding = get_bedrock_embedding(job, model_id, region)

    similarity = calculate_cosine_similarity(resume_embedding, jd_embedding)
    return similarity


def compare_hard_requirements(resume, job):
    prompt = f"""
        Here is the resume:
        {resume}

        Here is the job description:
        {job}

        Does the basic requirement match? True or False?
    """

    bedrock_client = boto3.client(service_name='bedrock-runtime')

    # Inference configuration
    inference_config = {
        "temperature": 0,
        "maxTokens": 100,
        "topP": 1,
    }

    # Prepare the message payload
    messages = [{
        "role": "user",
        "content": [{"text": prompt}]
    }]

    # Invoke the model
    response = bedrock_client.converse(
        modelId="amazon.titan-tg1-large",
        messages=messages,
        inferenceConfig=inference_config,
    )

    # Extract and return the generated text
    return 1 if "True" in response['output']['message']['content'][0]['text'] else 0


def handler(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    s3_client = boto3.client("s3")
    file = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file = json.loads(file["Body"].read().decode("utf-8"))

    resume = file['resume']
    job = file['job']

    score1 = compare_keywords(resume, job)
    score2 = compare_embeddings(resume, job)
    score3 = compare_hard_requirements(resume, job)
    score = (score1 + score2 + score3) / 3

    open(f"/tmp/score.txt", "w").write(str(score))

    filename = object_key.split(".")[0] + ".txt"
    s3_client.upload_file(f"/tmp/score.txt", "rank-my-resume-s3", filename)
