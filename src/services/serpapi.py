import httpx
from dotenv import load_dotenv
import os
load_dotenv()
from serpapi import GoogleSearch
async def get_query_results(query: str):
    api_key = os.getenv("SERP_API_KEY")
    params = {
        "q": query,
        # "location": "Austin, Texas, United States",
        "hl": "en",
        # "gl": "us",
        "google_domain": "google.com",
        "api_key": api_key
      }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results
