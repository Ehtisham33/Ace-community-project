from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import DirectoryLoader
# step 1: load raw pdfs

DATA_PATH =r'data'
def load_pdf_file(data):
    loader = DirectoryLoader(
        path=data,
        glob='*.pdf',
        loader_cls=UnstructuredPDFLoader,
        loader_kwargs={'strategy': 'auto'}
    )
    documents = loader.load()
    return documents 

documents = load_pdf_file(data=DATA_PATH)
print(f'The Total No of Pages : {len(documents)}')

# step 2: create chunks

def create_chunks(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,
                                                 chunk_overlap=50)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks=create_chunks(extracted_data=documents)
print("Length of Text Chunks: ", len(text_chunks))

# step 3: create vector embeddings

def get_embedding_model():
    print(f"Embedding Model Processing Begin!!...")
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

embedding_model=get_embedding_model()

# step 4: store embedding in FAISS

DB_FAISS_PATH="vectorstore/db_faiss"
print(f"Creating & Storing Database Processing Begin!!...")
db=FAISS.from_documents(text_chunks, embedding_model)
db.save_local(DB_FAISS_PATH)