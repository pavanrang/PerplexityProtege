# search_engine.py
import json
import requests
from fastapi import HTTPException
from config import SERPER_API, SERPER_SEARCH_ENDPOINT, REFERENCE_COUNT, DEFAULT_SEARCH_ENGINE_TIMEOUT

def search_with_serper(query: str, subscription_key=SERPER_API, prints=False):
    """
    Search with serper and return the contexts.
    """
    payload = json.dumps({
        "q": query,
        "num": (
            REFERENCE_COUNT
            if REFERENCE_COUNT % 10 == 0
            else (REFERENCE_COUNT // 10 + 1) * 10
        ),
    })
    headers = {"X-API-KEY": subscription_key, "Content-Type": "application/json"}
    response = requests.post(
        SERPER_SEARCH_ENDPOINT,
        headers=headers,
        data=payload,
        timeout=DEFAULT_SEARCH_ENGINE_TIMEOUT,
    )
    if not response.ok:
        raise HTTPException(response.status_code, "Search engine error.")
    json_content = response.json()

    if prints:
        print(json_content)
        print("\n\n\n-------------------------------------------------------------------------------\n\n\n")

    try:
        # convert to the same format as bing/google
        contexts = []
        if json_content.get("knowledgeGraph"):
            url = json_content["knowledgeGraph"].get("descriptionUrl") or json_content["knowledgeGraph"].get("website")
            snippet = json_content["knowledgeGraph"].get("description")
            if url and snippet:
                contexts.append({
                    "name": json_content["knowledgeGraph"].get("title",""),
                    "url": url,
                    "snippet": snippet
                })
        if json_content.get("answerBox"):
            url = json_content["answerBox"].get("url")
            snippet = json_content["answerBox"].get("snippet") or json_content["answerBox"].get("answer")
            if url and snippet:
                contexts.append({
                    "name": json_content["answerBox"].get("title",""),
                    "url": url,
                    "snippet": snippet
                })
        contexts += [
            {"name": c["title"], "url": c["link"], "snippet": c.get("snippet","")}
            for c in json_content["organic"]
        ]

        if prints:
            print(contexts[:REFERENCE_COUNT])
        return contexts[:REFERENCE_COUNT]
    
    except KeyError:
        return []