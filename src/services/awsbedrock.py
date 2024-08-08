import os
import boto3
from dotenv import load_dotenv
from typing import List, Dict, Optional
import json
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
def converse_stream_bedrock(
                            query: str,
                            search_results: Optional[str]):
    response = client.converse(
        modelId=os.getenv("MODEL_ID"),
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

def optimize_query(user_query: str) -> str:
    system_message = {
   'text': """You are an AI assistant tasked with optimizing user queries for better search results on the Serper API. 
    Please enhance the following query to make it more specific and effective for searching. 
    Your response should be formatted in JSON with the key "optimized_query" and the value being the enhanced query. 
    Ensure the JSON response is clean and free from any additional text or formatting. 
    Here is the query to be optimized: {user_query}.
    
    Example of the expected response format:
    {
        "optimized_query": "enhanced version of the input query"
    }"""
    }

    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'text': user_query
                }
            ]
        }
    ]

    response = client.converse(
        modelId=os.getenv("MODEL_ID"),  # Ensure you have the correct model ID
        messages=messages,
        system=[system_message]
    )

    optimized_query = response["output"]["message"]["content"][0]["text"]
    response_json = json.loads(optimized_query)
    optimized_query = response_json.get("optimized_query", "No optimized query found")
    return optimized_query

if __name__ == '__main__':
    model_id = os.getenv("MODEL_ID")
    # query = "what is the meaning of life?"

    # response = converse_stream_bedrock(model_id=model_id, query=query, search_results=search_results)
    # response = optimize_query("Web development course for the beginners and intermdiate and advanced")
    # print(response)





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

"""

"""