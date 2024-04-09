from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

questions = [
    {"question": "扬州航空产业发展如何", "index": 1},
    {"question": "飞机的组成部分", "index": 2},
    {"question": "扬州航空发展怎么样", "index": 3},
    {"question": "说一下扬州航空的发展", "index": 4},
    {"question": "扬州航空的如何", "index": 5},
    {"question": "扬州航空发展怎么样？", "index": 6},
    {"question": "扬州航空，发展怎么样", "index": 7},
    {"question": "你觉得扬州航空发展的怎么样？", "index": 8},
    {"question": "扬州航空发展？", "index": 9},
    {"question": "飞机由哪几个部分组成", "index": 10},
    {"question": "飞机的组成部分有那些", "index": 11},
    {"question": "飞机有什么部件", "index": 12},
    {"question": "飞机由哪几个部分组成？", "index": 13},
    {"question": "飞机上面，有那些部分？", "index": 14},
    {"question": "请问飞机上面会有那些部件", "index": 15},

]


def test_is_match_with_matching_question(index=3):
    # 根据index找到对应的测试用例
    test_case = next((item for item in questions if item["index"] == index), None)
    if not test_case:
        raise ValueError(f"No test case found with index: {index}")

    question = test_case["question"]
    print(question)
    response = client.get(f"/api/langchain_qa/match?question={question}")
    print(f"Status Code: {response.status_code}")
    # 打印响应体的字符串表示
    print(f"Response Text: {response.text}")
    assert response.status_code == 200
    assert response.json() == {"match": True, "index": 1}
