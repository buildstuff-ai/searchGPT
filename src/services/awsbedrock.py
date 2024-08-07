import os
import boto3
from dotenv import load_dotenv
from typing import List, Dict, Optional
load_dotenv()


aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')


client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
                )

#TODO: fix the latency
def converse_stream_bedrock(model_id: str,
                            query: str,
                            search_results: Optional[str]):
    response = client.converse(
        modelId=model_id,
        messages=[
            {
                'role': 'user',
                'content': [
                    {   #TODO: update the system message and the below content as per the request and the response required.
                        'text': f"""You are an AI assistant, given the task to understand the user's query, and the provided search results with their content and the links.
                                    Give the user a detailed answer in json format. Do not include any ```json``` and unnecessary words.
                                    user query: {query};

                                    search_results: {search_results};
                                    """
                    }
                ]
            }
        ],
        system=[
            {
                'text': """You are an AI assistant, given the task to understand the user's query, and the provided search results with their content and the links.
                           Give the user a detailed answer in json format. Do not include any ```json``` and unnecessary words."""
            }
        ]
    )

    return response["output"]["message"]


if __name__ == '__main__':
    model_id = os.getenv("MODEL_ID")
    query = "what is the meaning of life?"
    search_results = """
    The meaning of life can be defined in many ways, including as the quality that distinguishes a living being from a dead body, or as the capacity for growth, metabolism, and reproduction. It can also be defined as the process of acting, reacting, evaluating, and evolving through growth. 

    Merriam-Webster(link)
    Life Definition & Meaning - Merriam-Webster
    6 days ago — a. : the quality that distinguishes a vital and functional being from a dead bod...

    Philosophy Now(link)
    What Is Life? | Issue 101 - Philosophy Now
    Life is the aspect of existence that processes, acts, reacts, evaluates, and evolves throu...
    Some say that the meaning of life is something that we actively create and define through our actions and experiences. Others say that the meaning of life can be found by recognizing your own gifts and using them to contribute to the world. This could be by helping friends, playing music, or bringing joy to others. 
    Here are some ways to find meaning in life:
    Learn about happiness
    Let your talents lead you to new opportunities
    Make connections with people who share your interests
    Set challenging but clear goals
    Follow your internal compass when making decisions
    Help others when you can 
"""
    response = converse_stream_bedrock(model_id=model_id, query=query, search_results=search_results)

    print(response)

    """
{
  "ResponseMetadata": {
    "RequestId": "3c949448-5aa2-1bc1c2ed0873",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "date": "Wed, 07 Aug 2024 18:58:54 GMT",
      "content-type": "application/json",
      "content-length": "1784",
      "connection": "keep-alive",
      "x-amzn-requestid": "3c949448-5aa2-1bc1c2ed0873"
    },
    "RetryAttempts": 0
  },
  "output": {
    "message": {
      "role": "assistant",
      "content": [
        {
          "text": 
                "{\n  \"answer\": \"The meaning of life is a profound philosophical and existential question that has been contemplated throughout human history.  \
                      1. Self-discovery and self-actualization: Discovering and fulfilling one's potential, talents, and purpose by pursuing personal growth, creativity, and contributing positively to the world.}"
        }
      ]
    }
  },
  "stopReason": "end_turn",
  "usage": {
    "inputTokens": 456,
    "outputTokens": 309,
    "totalTokens": 765
  },
  "metrics": {
    "latencyMs": 17537
  }
}
"""