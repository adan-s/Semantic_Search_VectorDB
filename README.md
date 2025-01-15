# Article Search with Chroma and LangChain

This project demonstrates how to create a document search service using LangChain, OpenAI embeddings, and Chroma as a vector store. The service allows users to query for information on predefined topics and returns the most relevant articles based on similarity search.

---

## Features

- **Persistent Vector Store**: Uses Chroma for storing embeddings and documents.
- **OpenAI Embeddings**: Employs the `text-embedding-ada-002` model for vectorizing text.
- **Predefined Topics**: Limits user queries to a set of predefined topics for better control and relevance.
- **Duplicate Filtering**: Ensures the results do not include duplicate articles.
- **Interactive Querying**: Allows users to interactively search for articles until they choose to quit.

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   
2. **Install Dependencies**


    Ensure **Python 3.8+** is installed, then run the following command to install the required libraries:
   ```bash
   pip install langchain chromadb python-dotenv
   
3. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
 
4. **Set Up Environment Variables**

   Create a .env file in the root of the project and add your OpenAI API key:

   ```bash
   OPENAI_API_KEY=your_openai_api_key

---

## Running the Script

Run the script using the following command:
```bash
python main.py
```



---

## How to Use
1. Run the script, and you'll be prompted to enter a query.
2. Type a question or topic (e.g., "Tell me about AI").
3. If your query matches one of the predefined topics, the service will return the most relevant articles.
4. To exit the program, type quit.
 

---

## Acknowledgments

- **[LangChain](https://www.langchain.com/)**: For providing a modular framework to build with LLMs.
- **[Chroma](https://www.trychroma.com/)**: For enabling efficient and persistent vector storage.
- **[OpenAI](https://www.openai.com/)**: For their embedding models and APIs.

