# chains.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def run_chain(text: str):
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=None)

    # Define prompt template
    prompt = PromptTemplate(
        input_variables=["text"],
        template=(
            "You are an expert analyst. For the following text:\n\n{text}\n\n"
            "1. Provide a short summary.\n"
            "2. Provide the sentiment (Positive, Neutral, Negative).\n"
            "3. Extract 3–5 main keywords.\n\n"
            "Respond in JSON format with fields: summary, sentiment, keywords."
        )
    )

    # Format prompt with text
    formatted_prompt = prompt.format(text=text)

    # Run LLM
    result = llm.invoke(formatted_prompt)
    return result
