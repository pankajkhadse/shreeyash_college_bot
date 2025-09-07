from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert assistant for Shreeyash College of Engineering.

Answer the question clearly and directly using ONLY the given context.
Do NOT mention documents, sources, titles, IDs, or any metadata.
Do NOT use phrases like "according to the document" or "based on the provided document".
If the answer is not found, simply reply: "Sorry, I don’t have that information."

Format the answer in clean, structured points or short sentences for readability.

Context:
{context}

Question: {question}

Answer:
"""



prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    # ✅ Extract only the text
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])

    
    result = chain.invoke({"context": context, "question": question})
    print(result)
