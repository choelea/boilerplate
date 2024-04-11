from pymilvus import connections, Collection
from langchain_openai.embeddings import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

def query_all_matches(question,content):
    '''
    【发散模式下】接收一个问题和内容集合作为输入，并返回与问题相匹配的所有内容元素。
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

    # 获取 对应库
    collection = Collection(name=collection_name)
    # L2 （欧氏距离）：计算两个点之间的直线距离 内积：反映了两个向量的方向一致性和大小，常用于推荐系统等。
    search_params = {"metric_type": "L2", "params": {"nprobe": 100}}
    #输出一个相关的向量结果
    limit_number = 1
    #结果
    results = collection.search([question_vector], "vector", search_params, limit=limit_number)

    # 用于存储所有匹配的文本元素
    all_text_elements = []

    # 如果搜索结果不为空
    if results:
        # 获取搜索结果的距离
        distances = results[0].distances
        # 获取匹配的ID
        matched_ids = results[0].ids
        # 筛选出距离小于【参数可以调。越小越精准】的结果，认为是相关的
        relevant_ids = [matched_ids[i] for i, distance in enumerate(distances) if distance < 0.4]

        # 如果有相关的结果
        if relevant_ids:
            pk_list_str = ", ".join(str(pk) for pk in relevant_ids)
            expr = f"pk in [{pk_list_str}]"

            documents = collection.query(expr=expr, output_fields=["*"])
            # 从查询结果中提取文本内容
            for doc in documents:
                text_element = doc.get("text", None)
                if text_element:
                    all_text_elements.append(text_element)
    # 如果找到了匹配的文本元素，则返回它们；否则返回 "没有数据"
    return all_text_elements if all_text_elements else "没有数据"


