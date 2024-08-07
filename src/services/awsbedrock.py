import os
import boto3
from dotenv import load_dotenv

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

#TODO: test the functioning of the service
def converse_stream_bedrock(model_id, 
                            query, 
                            search_results):
    response = client.converse(
        modelId=model_id,
        messages=[
            {'role': 'user', 'content': [
                                {'text': f"""You are an AI assistant, given the task to understand the user\'s query, and the provided search results with their content and the links.\
                                        Give the user a detailed answer in json format. Do not include any ```json``` and unnecessary words.
                                        user query: {query};

                                        search_results: {search_results};
                                        """,
                                }
                            ]
            },
        ],
        system=[
            {
                'text': """You are an AI assistant, given the task to understand the user\'s query, and the provided search results with their content and the links.\
                            Give the user a detailed answer in json format. Do not include any ```json``` and unnecessary words.""",
            },
        ]
    )

    return response["output"]["message"].content["text"]
