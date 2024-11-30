# Rank-My-Resume

## Overview
An intelligent applicant tracking system that leverages AWS serverless technologies to process, analyze, and rank job candidate resumes.

## Core Architecture
- **Text Extraction**: PyPDF for resume parsing
- **Entity Recognition**: AWS Comprehend for skill extraction
- **Scoring Engine**: Multi-stage computational pipeline
- **Infrastructure**: AWS Lambda, SNS/SQS fan-out architecture

## Key Processing Steps
1. Resume Text Extraction
2. Skill Entity Recognition
3. Keyword Matching
4. Semantic Similarity Analysis
5. Hard Requirement Validation
6. Aggregate Scoring (0-100 scale)

## Technical Components
- **Compute**: AWS Lambda
- **Messaging**: SNS/SQS for scalable event processing
- **Machine Learning**: Optional SageMaker for advanced scoring models
- **Ranking**: Dynamic leaderboard generation

## Scalability Features
- Parallel Lambda processing
- Event-driven architecture
- Low-latency design
- Elastic infrastructure

## Potential Enhancements
- Advanced NLP models
- Machine learning scoring refinement
- Multi-language support
