from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings

class Embeddings:
    @staticmethod
    def get_embedding():
        return SpacyEmbeddings(model_name="en_core_web_sm")