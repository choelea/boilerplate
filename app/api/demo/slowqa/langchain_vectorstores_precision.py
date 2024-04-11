from pymilvus import connections, Collection
from langchain_openai.embeddings import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
def query_all_matches_precision(question,content):
    '''
    【严格模式下】接收一个问题和内容集合作为输入，并返回与问题相匹配的所有内容元素。
    '''
    # 设置连接Milvus数据库的参数
    connection_args = {"host": "10.3.70.15", "port": "19530"}
    collection_name = "test"

    # 初始化Azure OpenAI嵌入向量生成器
    embedder = AzureOpenAIEmbeddings(
        azure_endpoint="https://coe0118.openai.azure.com/",
        openai_api_key=os.getenv('AZURE_OPENAI_API_KEY')
    )
    # 使用Azure OpenAI嵌入向量生成器将问题文本转换为向量
    question_vector = embedder.embed_query(question)
    # 连接到Milvus数据库
    connections.connect(**connection_args)
    # 连接到Milvus数据库
    #欧式，内积20
    collection = Collection(name=collection_name)
    search_params = {"metric_type": "L2", "params": {"nprobe": 20}}
    #返回一个
    limit_number = 1
    results = collection.search([question_vector], "vector", search_params, limit=limit_number)

    # 用于存储所有匹配的文本元素
    all_text_elements = []

    # 如果搜索结果不为空  代码与发散类似，分开出来【严格模式】参数在其中调整
    if results:
        distances = results[0].distances
        matched_ids = results[0].ids
        # 精度小于【发散模式】
        relevant_ids = [matched_ids[i] for i, distance in enumerate(distances) if distance < 0.2]

        if relevant_ids:
            pk_list_str = ", ".join(str(pk) for pk in relevant_ids)
            expr = f"pk in [{pk_list_str}]"

            documents = collection.query(expr=expr, output_fields=["*"])

            for doc in documents:
                text_element = doc.get("text", None)
                if text_element:
                    all_text_elements.append(text_element)
    # 如果找到了匹配的文本元素，则返回它们；否则返回 "没有数据"
    return all_text_elements if all_text_elements else "没有数据"

