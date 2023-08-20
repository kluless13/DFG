# Import necessary libraries and modules
import os
import re
from os import listdir
from os.path import isfile, join
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
os.environ['OPENAI_API_KEY'] = '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'

# Initialize OpenAI LLM and embeddings
llm = OpenAI(temperature=0.1, verbose=True)
embeddings = OpenAIEmbeddings()

# Directory containing PDFs
pdf_directory = '/Users/angad/DFG/data'

# Get all PDF files in the directory
all_files = [f for f in listdir(pdf_directory) if isfile(join(pdf_directory, f))]
pdf_files = [f for f in all_files if f.endswith('.pdf')]

# Dictionary to store Chroma vectorstores for each PDF
stores = {}

# Load and process each PDF, storing pages in separate vector databases
for pdf_file in pdf_files:
    loader = PyPDFLoader(join(pdf_directory, pdf_file))
    pages = loader.load_and_split()
    store_name = pdf_file.replace('.pdf', '')
    stores[store_name] = Chroma.from_documents(pages, embeddings, collection_name=store_name)

# Create vectorstore info object and toolkit
vectorstore_info = VectorStoreInfo(
    name=store_name,
    description=f"{store_name} as a PDF",
    vectorstore=stores[store_name]
)
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

# Create the agent executor after defining the toolkit
agent_executor = create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

# Streamlit interface
st.title('🦜🔗 GPT Investment Banker')
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
