from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

questions = [
    {"question": "北京航空发展怎么样", "index": 1},
    {"question": "汽车由那几个部分组成", "index": 2}


]

def test_is_match_with_no_matching_question(index=1):
    # 根据index找到对应的测试用例
    test_case = next((item for item in questions if item["index"] == index), None)
    if not test_case:
        raise ValueError(f"No test case found with index: {index}")
    question = test_case["question"]
    response = client.get(f"/api/langchain_qa/match?question={question}")
    assert response.status_code == 200
    assert response.json() == {"match": False,"index": -1}


