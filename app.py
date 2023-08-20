# Import necessary libraries and modules
import os
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = '-'

# Initialize OpenAI LLM and embeddings with adjusted parameters for broader answers
llm = OpenAI(temperature=0.2, verbose=True, max_tokens=500)
embeddings = OpenAIEmbeddings()

# Directory containing PDFs
pdf_directory = '/Users/angad/DFG/data'

# Get all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Dictionary to store Chroma vectorstores for each PDF
stores = {}

for pdf_file in pdf_files:
    loader = PyPDFLoader(os.path.join(pdf_directory, pdf_file))
    pages = loader.load_and_split()
    store_name = pdf_file.replace('.pdf', '')
    stores[store_name] = Chroma.from_documents(pages, embeddings, collection_name=store_name)

# Create a default VectorStoreInfo object
default_vectorstore_info = VectorStoreInfo(
    name="default_store",
    description="Default store for multiple PDFs",
    vectorstore=next(iter(stores.values()))  # Use the first vectorstore as a placeholder
)

# Create the agent executor for the LLM using the default VectorStoreInfo
toolkit = VectorStoreToolkit(vectorstore_info=default_vectorstore_info)
agent_executor = create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

# Streamlit interface
st.title('Decentralised Fisheries Governance')
prompt = st.text_input('Input your prompt here')

# When user provides input
if prompt:
    max_similarity = -float('inf')
    most_relevant_content = None
    most_relevant_store_name = None

    # Search across all vectorstores to find the most relevant document
    for store_name, store in stores.items():
        search = store.similarity_search_with_score(prompt)
        if search and search[0][1] > max_similarity:
            max_similarity = search[0][1]
            most_relevant_content = search[0][0].page_content
            most_relevant_store_name = store_name

    # Get answer from LLM
    response = agent_executor.run(prompt)
    st.write(response)

    # Display most relevant content from the most relevant PDF
    with st.expander(f'Document Similarity Search from {most_relevant_store_name}.pdf'):
        st.write(most_relevant_content)
