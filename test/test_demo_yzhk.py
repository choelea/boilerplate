from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

questions_1 = [
    "扬州航空产业发展如何",
    "扬州航空发展怎么样",
    "说一下扬州航空的发展",
    "扬州航空的如何",
    "扬州航空发展怎么样？",
    "扬州航空，发展怎么样",
    "你觉得扬州航空发展的怎么样？",
    "扬州航空发展？",

]

questions_2 = [
    "飞机的组成部分",
    "飞机由哪几个部分组成",
    "飞机的组成部分有那些",
    "飞机有什么部件",
    "飞机由哪几个部分组成？",
    "飞机上面，有那些部分？",
    "请问飞机上面会有那些部件",
    "飞机的组成"
]

questions_3 = [
    "写一首与扬州航空相关的诗句",
    "扬州航空相关的诗句",
]

questions_not_match = [
    "北京航空发展怎么样",
    "汽车由那几个部分组成",
    "系由哪几部分组成",
]


def test_matching_question_1():
    """
    循环questions_1列表，测试是否匹配
    """
    __matching_question(questions_1, 1)


def test_matching_question_2():
    """
    循环questions_2列表，测试是否匹配
    """
    __matching_question(questions_2, 2)


def test_matching_question_3():
    """
    循环questions_3列表，测试是否匹配
    """
    __matching_question(questions_3, 3)


def test_not_matching_question():
    """
    测试questions列表中的问题是否匹配
    """
    for question in questions_not_match:
        response = client.get(f"/demo/yzhk/match?question={question}")
        assert response.status_code == 200
        assert response.json() == {"match": False, "index": -1}, f"Question is: {question}"


def __matching_question(questions: list[str], index: int):
    """
    循环questions列表，测试是否匹配
    """
    for question in questions:
        response = client.get(f"/demo/yzhk/match?question={question}")
        # 打印响应体的字符串表示
        assert response.status_code == 200
        # 如果assert expression为False，则打印错误信息
        assert response.json() == {"match": True, "index": index}, f"Question is: {question}"



