
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI, LlamaCpp
from rag.rag_qa import build_rag_chain

# 外部LLM（ChatGPT API）
openai_llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

# ローカルLLM（Llama.cpp）
local_llm = LlamaCpp(model_path="./models/local_model.gguf")

# RAGチェーン構築（会社データ）
rag_chain = build_rag_chain("./company_data/company_info.txt", "./models/local_model.gguf")

def route_query(user_input):
    company_keywords = ["御社", "あなたの会社", "会社概要", "社内情報", "製品", "事業内容"]
    if any(kw in user_input for kw in company_keywords):
        # RAG経由で会社情報回答
        return rag_chain.run(user_input)
    else:
        chain = LLMChain(
            llm=openai_llm,
            prompt=PromptTemplate.from_template("Q: {question}\nA:")
        )
        return chain.run({"question": user_input})
