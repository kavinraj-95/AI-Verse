from tools.reddit_scraper import get_reddit_threads
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

def market_analyst_agent(user_profile: dict) -> list:
    """
    Searches for job opportunities that match the user's profile and ranks them by relevance.

    Args:
        user_profile: A dictionary containing the user's profile information.

    Returns:
        A list of job opportunities, ranked by relevance.
    """
    keywords = user_profile.get("skills", []) + user_profile.get("implied_interests", [])
    
    threads = get_reddit_threads(keywords)
    
    # Using gemini-2.5-flash to avoid model not found errors and improve rate limit.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    prompt = PromptTemplate.from_template(
        """
        Given the user's profile and a list of job opportunities, rank the opportunities by relevance.
        Return a valid JSON list of the opportunities with an added "relevance_score" key (from 0 to 1).
        
        Do not include any other text, explanations, or markdown formatting. Only return the raw JSON list.

        User profile:
        {user_profile}

        Job opportunities:
        {threads}
        """
    )
    
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    
    try:
        response = chain.invoke({"user_profile": user_profile, "threads": threads})
        return response
    except Exception as e:
        return [{"error": f"Failed to parse LLM response as JSON: {e}"}]

