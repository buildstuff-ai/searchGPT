from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services import optimize_query,get_query_results,converse_stream_bedrock
app = FastAPI()

class Query(BaseModel):
    text: str

@app.get("/query")
async def handle_query(query: Query):
    print(query)
    optimized_query = optimize_query(query.text)
    serpapi_response = await get_query_results(optimized_query)
    optimized_result = converse_stream_bedrock(optimized_query,serpapi_response)
    return {"query": query.text, "response": optimized_result}

def process_query(text: str) -> str:
    return text

def get_brave_response(processed_text: str) -> str:
    return "Sample response from Brave API"

def summarize_response(response: str) -> str:
    return "Summarized: " + response
