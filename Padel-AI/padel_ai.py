import os
from flask import Flask, jsonify, request
import asyncio
import warnings
from langchain_huggingface import HuggingFaceEmbeddings,HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
warnings.filterwarnings("ignore", category=FutureWarning)


load_dotenv(find_dotenv())
app = Flask(__name__)
DB_FAISS_PATH =r"vectorstore/db_faiss"

#load vectore store
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vectorstore = FAISS.load_local(DB_FAISS_PATH,embedding_model,allow_dangerous_deserialization=True)

CUSTOM_PROMPT_TEMPLATE ="""
Use the pieces of information provided in the context to answer user's question.
If you don’t know the answer, just say that you don’t know, don’t try to make up an answer.
Don’t provide anything out of the given context.

Context: {context}
Question: {question}

Start the answer directly. No small talk please."""

def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE,input_variables=['context','questions'])

def load_llm():
    HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
    HF_TOKEN = os.environ.get("HF_TOKEN")

    return HuggingFaceEndpoint(
        repo_id = HUGGINGFACE_REPO_ID,
        task = "test-generation",
        temperature = 0.5,
        model_kwargs={
            "token":HF_TOKEN,
            "max_length":"512"
        }
    )

qa_chain = RetrievalQA.from_chain_type(
    llm=load_llm(),
    chain_type = "stuff",
    retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
    return_source_documents = True,
    chain_type_kwargs = {'prompt': set_custom_prompt()}
)

@app.route('/ask',methods=['post'])
def ask_questions():
    try:
        data = request.json
        query = data.get('question', '')

        if not query:
            return jsonify({'error': 'No question provided'}), 400

        asyncio.set_event_loop(asyncio.new_event_loop())
        response = qa_chain.invoke({'query': query})
        return jsonify({'answer': response['result']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7005,debug=True)