
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI, LlamaCpp

# 外部LLM（ChatGPT API）
openai_llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

# ローカルLLM（Llama.cpp）
local_llm = LlamaCpp(model_path="./models/local_model.gguf")

def route_query(user_input):
    company_keywords = ["御社", "あなたの会社", "会社概要", "社内情報"]
    if any(kw in user_input for kw in company_keywords):
        llm = local_llm
    else:
        llm = openai_llm

    chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template("Q: {question}\nA:")
    )
    return chain.run({"question": user_input})
