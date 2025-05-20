# Import the base Tool class from smolagents
from smolagents import Tool

# BM25Retriever is a keyword-based retriever for searching documents
from langchain_community.retrievers import BM25Retriever

# Document class represents text data in LangChain-compatible format
from langchain.docstore.document import Document

# Datasets module for loading Hugging Face datasets
import datasets


# ----------------------------------------
# Guest Info Retrieval Tool Definition
# ----------------------------------------

class GuestInfoRetrieverTool(Tool):
    """
    A custom tool that retrieves guest information from a dataset using BM25-based keyword search.
    """

    # Tool metadata
    name = "guest_info_retriever"
    description = "Retrieves detailed information about gala guests based on their name or relation."

    # Define the input format
    inputs = {
        "query": {
            "type": "string",
            "description": "The name or relation of the guest you want information about."
        }
    }

    # Define the output format
    output_type = "string"

    def __init__(self, docs):
        """
        Initialize the tool with a list of Document objects.
        Uses BM25Retriever to perform keyword matching over these documents.
        """
        self.is_initialized = False  # Unused, can be used later to check status
        self.retriever = BM25Retriever.from_documents(docs)  # Create a retriever using the documents

    def forward(self, query: str):
        """
        Execute the retrieval logic for a given query.
        Returns top 3 matching documents' contents or a fallback message if nothing is found.
        """
        results = self.retriever.get_relevant_documents(query)

        if results:
            # Join and return content from top 3 results
            return "\n\n".join([doc.page_content for doc in results[:3]])
        else:
            return "No matching guest information found."


# ----------------------------------------
# Utility Function to Load Guest Dataset
# ----------------------------------------

def load_guest_dataset():
    """
    Loads the invitee dataset from Hugging Face and formats it into Document objects.
    Each document includes name, relation, description, and email.
    Returns an initialized GuestInfoRetrieverTool.
    """

    # Load the dataset from Hugging Face (agents-course/unit3-invitees)
    guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

    # Format each row in the dataset into a LangChain Document
    docs = [
        Document(
            page_content="\n".join([
                f"Name: {guest['name']}",
                f"Relation: {guest['relation']}",
                f"Description: {guest['description']}",
                f"Email: {guest['email']}"
            ]),
            metadata={"name": guest["name"]}  # Optional metadata for additional filtering
        )
        for guest in guest_dataset
    ]

    # Return an instance of the custom retrieval tool initialized with the documents
    return GuestInfoRetrieverTool(docs)