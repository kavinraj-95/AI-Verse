from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from datetime import datetime

def executive_agent(user_profile: dict, opportunity: dict) -> str:
    """
    Drafts a tailored outreach message for a job opportunity and logs the application.

    Args:
        user_profile: A dictionary containing the user's profile information.
        opportunity: A dictionary representing the job opportunity.

    Returns:
        A string representing the drafted outreach message.
    """
    # Using gemini-2.5-flash to avoid model not found errors and improve rate limit.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    prompt = PromptTemplate.from_template(
        """
        Draft a tailored outreach message for the following job opportunity.
        The message should be professional, concise, and highlight the user's relevant skills.

        User profile:
        {user_profile}

        Job opportunity:
        {opportunity}
        """
    )

    chain = prompt | llm | StrOutputParser()

    draft_message = chain.invoke({"user_profile": user_profile, "opportunity": opportunity})

    # Log the application
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "opportunity": opportunity,
        "draft_message": draft_message,
    }

    with open("application_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return draft_message
