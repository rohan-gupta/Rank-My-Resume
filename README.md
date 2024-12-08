# Rank-My-Resume

## Overview
An intelligent applicant tracking system that leverages AWS serverless technologies to process, analyze, and rank job candidate resumes.

## Core Architecture
- **Text Extraction**: PyPDF for resume parsing
- **Entity Recognition**: AWS Bedrock for skill extraction
- **Scoring Engine**: Multi-stage computational pipeline
- **Leaderboard**: Sort the score list
- **Infrastructure**: AWS Lambda, SQS fan-out architecture, Serverless Framework (Infra as Code)

## Key Processing Steps
1. Resume Text Extraction
2. Hard Requirements Recognition
3. Keyword Matching
4. Semantic Similarity Analysis
5. Aggregate Scoring
6. Compose Leadeboard

## Technical Components
- **Compute**: AWS Lambda
- **Messaging**: SQS for scalable event processing
- **Cosine Similarity**: Bedrock for vectorizing text
- **Gen AI**: Bedrock for hard requirements

## Scalability Features
- Parallel Lambda processing
- Event-driven architecture
- Low-latency design

# How To Use
- `cd Rank-My-Resume`
- `cd core`
- `npm install serverless`
- `npm install serverless-python-requirements`
- `serverless deploy`
- update the endpoints shown after serverless deploy in the html/js file (line 119 in index and line 42 in leaderboard)
- access the html to use the app
