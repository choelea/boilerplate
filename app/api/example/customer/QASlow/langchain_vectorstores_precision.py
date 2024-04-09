from pymilvus import connections, Collection
from langchain_openai.embeddings import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
def query_all_matches_precision(question,content):
    connection_args = {"host": "10.3.70.15", "port": "19530"}
    collection_name = "test"

    embedder = AzureOpenAIEmbeddings(
        azure_endpoint="https://coe0118.openai.azure.com/",
        openai_api_key=os.getenv('AZURE_OPENAI_API_KEY')
    )

    question_vector = embedder.embed_query(question)

    connections.connect(**connection_args)

    collection = Collection(name=collection_name)
    search_params = {"metric_type": "L2", "params": {"nprobe": 20}}

    limit_number = 1
    results = collection.search([question_vector], "vector", search_params, limit=limit_number)

    all_text_elements = []

    if results:
        distances = results[0].distances
        matched_ids = results[0].ids
        relevant_ids = [matched_ids[i] for i, distance in enumerate(distances) if distance < 0.2]

        if relevant_ids:
            pk_list_str = ", ".join(str(pk) for pk in relevant_ids)
            expr = f"pk in [{pk_list_str}]"

            documents = collection.query(expr=expr, output_fields=["*"])

            for doc in documents:
                text_element = doc.get("text", None)
                if text_element:
                    all_text_elements.append(text_element)

    return all_text_elements if all_text_elements else "没有数据"

if __name__ == '__main__':
    # results = query_all_matches("扬州航空产业发展得怎么样?")
    results = query_all_matches_precision("今天星期几?")
    print(results)
