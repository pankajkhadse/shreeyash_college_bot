from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering questions about Shreeyash College of Engineering.

Here are some relevant documents: {reviews}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    reviews = retriever.invoke(query.question)
    result = chain.invoke({"reviews": reviews, "question": query.question})
    return {"answer": result}
