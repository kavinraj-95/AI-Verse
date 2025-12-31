from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def critic_reflector_agent(rejection_feedback: str) -> str:
    """
    Parses rejection feedback and identifies the priority skill gap.

    Args:
        rejection_feedback: A string containing the rejection feedback.

    Returns:
        A string representing the priority skill gap.
    """
    # Using gemini-2.5-flash to avoid model not found errors and improve rate limit.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    prompt = PromptTemplate.from_template(
        """
        Analyze the following rejection feedback and identify the main reason for rejection.
        Return a short phrase or keyword representing the priority skill gap.

        Rejection feedback:
        {rejection_feedback}
        """
    )

    chain = prompt | llm | StrOutputParser()

    priority_gap = chain.invoke({"rejection_feedback": rejection_feedback})

    return priority_gap
