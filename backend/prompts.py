import os
import json
from langchain import OpenAI, LLMChain, PromptTemplate

llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

summary_template = PromptTemplate(
    input_variables=["text"],
    template=(
        "You are an expert summarizer. Given the user text delimited by triple backticks, provide a concise summary in at most 50 words.\n\n"
        "Text:\n```{text}```\n\nSummary:"
    )
)
summary_chain = LLMChain(llm=llm, prompt=summary_template)

sentiment_template = PromptTemplate(
    input_variables=["text"],
    template=(
        "You are an expert sentiment analyst. Given the text delimited by triple backticks, answer in JSON with keys: polarity (one of positive/neutral/negative) and score (0-1 confidence). Do not add extra commentary.\n\n"
        "Text:\n```{text}```\n\nResult:"
    )
)
sentiment_chain = LLMChain(llm=llm, prompt=sentiment_template)

keywords_template = PromptTemplate(
    input_variables=["text"],
    template=(
        "You are an expert that extracts the 5 most important keywords or short phrases from the text inside triple backticks. Return a JSON array of keywords ordered by importance.\n\n"
        "Text:\n```{text}```\n\nKeywords:"
    )
)
keywords_chain = LLMChain(llm=llm, prompt=keywords_template)
