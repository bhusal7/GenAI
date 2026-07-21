import os
import tempfile
import shutil

import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

st.set_page_config(page_title="RAG Chat with your PDF", page_icon="📚", layout="wide")

PERSIST_DIR = "chroma_db"



@st.cache_resource(show_spinner=False)
def get_embedding_model():
    return HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatMistralAI(model="mistral-large-latest", temperature=0.9)


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
     You're a helpful AI Assistant.

Use only the provided context to answer the questions.

If the answer isn't present in the context,
say: "I can't find the answer in the document."
     """,
        ),
        (
            "human",
            """
     Context:{context}
     Question:{question}
     """,
        ),
    ]
)


def build_vector_store(pdf_path: str, persist_directory: str) -> Chroma:
    """Load a PDF, split it into chunks, embed it, and persist to Chroma."""
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embedding_model = get_embedding_model()


    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
    )
    return vector_store, len(chunks)


def get_retriever(vector_store: Chroma):
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5},
    )


def answer_question(retriever, llm, query: str):
    docs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in docs)
    final_prompt = PROMPT.invoke({"context": context, "question": query})
    response = llm.invoke(final_prompt)
    return response.content, docs




if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "book_name" not in st.session_state:
    st.session_state.book_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"/"assistant", "content": str}


with st.sidebar:
    st.header("📖 Upload your book")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    process_clicked = st.button("Process & Index", type="primary", use_container_width=True,
                                 disabled=uploaded_file is None)

    if process_clicked and uploaded_file is not None:
        with st.spinner("Reading, chunking and embedding your PDF... this can take a bit."):
            # Save the uploaded file to a temp path so PyPDFLoader can read it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name

            try:
                vector_store, num_chunks = build_vector_store(tmp_path, PERSIST_DIR)
                st.session_state.vector_store = vector_store
                st.session_state.book_name = uploaded_file.name
                st.session_state.messages = []  # reset chat for the new book
                st.success(f"Indexed **{uploaded_file.name}** into {num_chunks} chunks ✅")
            except Exception as e:
                st.error(f"Failed to process the PDF: {e}")
            finally:
                os.remove(tmp_path)

    st.divider()
    if st.session_state.book_name:
        st.caption(f"Currently loaded: **{st.session_state.book_name}**")
        if st.button("Clear document", use_container_width=True):
            if os.path.exists(PERSIST_DIR):
                shutil.rmtree(PERSIST_DIR)
            st.session_state.vector_store = None
            st.session_state.book_name = None
            st.session_state.messages = []
            st.rerun()
    else:
        st.caption("No document indexed yet.")


st.title("📚 Chat with your PDF")
st.caption("Upload a book/PDF from the sidebar, index it, then ask questions about it.")

if st.session_state.vector_store is None:
    st.info("👈 Upload a PDF and click **Process & Index** to get started.")
else:
    # Replay chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input("Ask something about your document...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    retriever = get_retriever(st.session_state.vector_store)
                    llm = get_llm()
                    answer, sources = answer_question(retriever, llm, query)
                    st.markdown(answer)

                    with st.expander("Show retrieved context"):
                        for i, doc in enumerate(sources, start=1):
                            page = doc.metadata.get("page", "N/A")
                            st.markdown(f"**Chunk {i} (page {page})**")
                            st.write(doc.page_content)
                except Exception as e:
                    answer = f"Something went wrong while answering: {e}"
                    st.error(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})