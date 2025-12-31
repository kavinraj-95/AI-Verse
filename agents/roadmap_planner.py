from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def roadmap_planner_agent(user_profile: dict, opportunities: list) -> str:
    """
    Performs a gap analysis and generates a learning roadmap.

    Args:
        user_profile: A dictionary containing the user's profile information.
        opportunities: A list of job opportunities.

    Returns:
        A markdown string representing the learning roadmap.
    """
    # Using gemini-2.5-flash to avoid model not found errors and improve rate limit.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    prompt = PromptTemplate.from_template(
        """
        Analyze the user's profile and the top job opportunity to identify skill gaps.
        Generate a 3-step learning roadmap (Short, Medium, and Long term) in Markdown format.
        Focus on the skills required for the job that are missing from the user's profile.

        User profile:
        {user_profile}

        Top job opportunity:
        {top_opportunity}
        """
    )

    chain = prompt | llm | StrOutputParser()

    # For simplicity, we'll use the first opportunity as the top opportunity
    top_opportunity = opportunities[0] if opportunities else {}

    response = chain.invoke({"user_profile": user_profile, "top_opportunity": top_opportunity})
    
    return response
