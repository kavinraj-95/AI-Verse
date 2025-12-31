from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from tools.resume_parser import resume_parser
from typing import IO
import json

def profiler_agent(file: IO[bytes]) -> dict:
    """
    Analyzes a resume file and extracts the user's skills, experience, and interests.

    Args:
        file: A file-like object representing the resume file.

    Returns:
        A dictionary containing the user's profile information.
    """
    resume_text = resume_parser(file)
    
    # Using gemini-2.5-flash to avoid model not found errors and improve rate limit.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    prompt = PromptTemplate.from_template(
        """
        Analyze the following resume text and extract the user's skills, experience, and implied interests.
        Return the information in a valid JSON format with the following keys: "skills", "experience", and "implied_interests".
        
        Do not include any other text, explanations, or markdown formatting. Only return the raw JSON object.

        Resume text:
        {resume_text}
        """
    )

    parser = JsonOutputParser()
    chain = prompt | llm | parser
    
    try:
        response = chain.invoke({"resume_text": resume_text})
        return response
    except Exception as e:
        return {"error": f"Failed to parse LLM response as JSON: {e}"}

