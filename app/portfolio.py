import os
import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path=None):
        # ✅ Always resolve to absolute path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Default location (inside app/resources/my_portfolio.csv)
        if file_path is None:
            file_path = os.path.join(current_dir, "resources", "my_portfolio.csv")

        # ✅ Ensure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Portfolio CSV not found at: {file_path}")

        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

        # ✅ Make vectorstore directory absolute (so works on Streamlit Cloud)
        vectorstore_path = os.path.join(current_dir, "vectorstore")
        os.makedirs(vectorstore_path, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(path=vectorstore_path)
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        """Load portfolio data into ChromaDB if empty."""
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        """Return most relevant project links based on given skills."""
        results = self.collection.query(query_texts=[skills], n_results=2)
        return results.get("metadatas", [])
