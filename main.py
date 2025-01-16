from langchain.agents import initialize_agent, Tool
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from uuid import uuid4
from langchain_core.documents import Document

from database.db import get_all_sessions, retrieve_memory, store_memory, initialize_database

# Load environment variables
load_dotenv()

# Use the correct embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Initialize the vector store with persistence
vector_store = Chroma(
    collection_name="Articles",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

# Define documents with article-like content
document_1 = Document(
    page_content="In recent years, the popularity of plant-based diets has surged, with many people opting for vegetarian or vegan lifestyles. This shift is often motivated by health concerns, ethical considerations regarding animal welfare, and environmental impact. Studies suggest that plant-based diets can lower the risk of chronic diseases such as heart disease, diabetes, and certain cancers.",
    metadata={"source": "health_article"},
    id=1,
)

document_2 = Document(
    page_content="The global economic outlook for 2023 remains uncertain, as geopolitical tensions and inflationary pressures continue to affect markets worldwide. Economists predict slow growth, particularly in emerging markets, with several regions facing high levels of unemployment and rising costs of living. Analysts urge governments to implement policies that focus on sustainable economic recovery.",
    metadata={"source": "economic_article"},
    id=2,
)

document_3 = Document(
    page_content="Artificial Intelligence (AI) and Machine Learning (ML) have become integral components of modern technology, transforming industries from healthcare to finance. While AI promises greater efficiencies and enhanced capabilities, there are also concerns about its ethical implications and the potential for job displacement. The key challenge moving forward will be balancing innovation with responsible governance.",
    metadata={"source": "technology_article"},
    id=3,
)

document_4 = Document(
    page_content="The rise of renewable energy sources such as wind and solar power has been one of the most significant developments in the fight against climate change. Governments and private companies are investing heavily in clean energy infrastructure, hoping to reduce reliance on fossil fuels and lower greenhouse gas emissions. However, challenges remain, particularly in energy storage and grid integration.",
    metadata={"source": "environmental_article"},
    id=4,
)

document_5 = Document(
    page_content="The entertainment industry has undergone a major transformation in the past decade, driven by the rise of streaming platforms. With companies like Netflix, Disney+, and Amazon Prime Video dominating the market, traditional TV networks are struggling to maintain their relevance. As the demand for on-demand content continues to grow, the future of broadcasting remains uncertain.",
    metadata={"source": "entertainment_article"},
    id=5,
)

document_6 = Document(
    page_content="As the world becomes increasingly interconnected, cybersecurity has become a critical issue for both individuals and organizations. Cyberattacks, ranging from data breaches to ransomware, are on the rise, highlighting the need for robust security measures. Experts emphasize the importance of adopting a proactive approach to cybersecurity, including regular software updates and employee training.",
    metadata={"source": "cybersecurity_article"},
    id=6,
)

document_7 = Document(
    page_content="In the world of finance, cryptocurrency has emerged as both a disruptive innovation and a speculative investment. While digital currencies like Bitcoin and Ethereum have the potential to revolutionize the financial industry, their volatility and lack of regulation raise concerns. Financial experts advise caution and recommend diversifying investments to mitigate risk.",
    metadata={"source": "finance_article"},
    id=7,
)

document_8 = Document(
    page_content="The field of genetic engineering has made significant advances in recent years, with CRISPR technology offering new possibilities for gene editing. While this technology holds great promise for curing genetic diseases, it also raises ethical questions about the potential for genetic modifications in humans. As research progresses, the debate over the moral implications of gene editing continues to intensify.",
    metadata={"source": "science_article"},
    id=8,
)

document_9 = Document(
    page_content="The world of sports continues to captivate millions, with soccer, basketball, and tennis among the most popular. Recent developments, such as the expansion of major leagues and the growing prominence of esports, have changed the landscape of competitive sports. As new sports technologies emerge, fans and players alike are experiencing a shift in how the game is played and consumed.",
    metadata={"source": "sports_article"},
    id=9,
)

document_10 = Document(
    page_content="The influence of social media on politics cannot be overstated. Platforms like Twitter, Facebook, and Instagram have become central to political discourse, with leaders using these platforms to communicate directly with their constituents. However, the role of social media in spreading misinformation and influencing elections remains a topic of debate among policymakers and experts.",
    metadata={"source": "politics_article"},
    id=10,
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
]

# Predefined list of valid categories or topics
valid_topics = [
    'plant-based diets', 'economic outlook', 'AI', 'ML', 'renewable energy', 'economy',
    'entertainment', 'cybersecurity', 'cryptocurrency', 'genetic engineering', 'crypto', 'plants',
    'sports', 'social media', 'politics'
]

# Initialize vector store and add documents
vector_store.add_documents(documents=documents, ids=[str(uuid4()) for _ in range(len(documents))])

# Define the search tool
def search_tool_function(query):
    query_lower = query.lower()

    # Validate topics
    valid_topics_lower = [topic.lower() for topic in valid_topics]
    if not any(topic in query_lower for topic in valid_topics_lower):
        return f"We don't have information on that topic right now. Valid topics include: {', '.join(valid_topics)}"

    # Perform similarity search
    results = vector_store.similarity_search(query, k=3)
    filtered_results = [
        res for res in results if any(topic in res.page_content.lower() for topic in valid_topics_lower)
    ]

    # Remove duplicates
    seen = set()
    unique_results = []
    for res in filtered_results:
        if res.page_content not in seen:
            seen.add(res.page_content)
            unique_results.append(res)

    if not unique_results:
        return "No matching articles found. Try a different topic."
    else:
        response = "Here are some relevant articles for your query:\n"
        for res in unique_results:
            response += f"\n* {res.page_content}\n  Source: {res.metadata.get('source', 'Unknown Source')}\n"
        return response

# Convert the search function into a tool
search_tool = Tool(
    name="Semantic Search",
    func=search_tool_function,
    description="Use this tool to search for articles related to specific topics or queries."
)


# Initialize the ChatGPT model for the agent
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Create the agent with the tool
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
)

# Agent interaction loop with session management
def start_agent():
    initialize_database()  # Ensure tables are created
    print("Welcome to the Semantic Search Application!")

    # Get available sessions
    available_sessions = get_all_sessions()

    # Ask the user whether to continue or start a new session
    if available_sessions:
        print("\nAvailable sessions:")
        for i, session in enumerate(available_sessions, start=1):
            print(f"{i}. {session}")

        choice = input("\nDo you want to continue a previous session or start a new one? (Type 'new' or the session number): ")

        if choice.lower() == "new":
            session_id = f"session_{len(available_sessions) + 1}"  # Generate a new session ID
            print("\nStarting a new session...")
        else:
            try:
                session_id = available_sessions[int(choice) - 1]
                print(f"\nContinuing session: {session_id}")

                # Retrieve memory for the current session
                past_memory = retrieve_memory(session_id)
                if past_memory:
                    print("\nPrevious Interactions:")
                    for item in past_memory:
                        print(f"User: {item['query']}")
                        print(f"Agent: {item['response']}")

            except (IndexError, ValueError):
                print("\nInvalid choice. Starting a new session.")
                session_id = f"session_{len(available_sessions) + 1}"
    else:
        session_id = "session_1"  # Default for the first session
        print("\nNo previous sessions found. Starting a new session...")

    while True:
        user_query = input("\nEnter the content to Search or type 'quit' to exit: ")
        if user_query.lower() == "quit":
            print("\nThank you for using the search agent. Goodbye!")
            break
        else:
            # Get agent response
            response = agent.invoke(user_query)

            # Store memory for the current session
            store_memory(session_id, user_query, response["output"])

            # Print agent response
            print(f"\n{response['output']}")

# Run the agent
if __name__ == "__main__":
    start_agent()