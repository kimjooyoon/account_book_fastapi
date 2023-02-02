from core.api.user.models import User


def test_verify():
    m = User()
    m.email = "test@test.test"
    m.password = "testaaaaa"
    assert True is m.verify()[0]
    m.email = "a@b.c"
    assert '이메일은 최소 6자 부터 30자 입니다.' in m.verify()
    m.email = "abcd"
    assert '이메일 형식이 올바르지 않습니다.' in m.verify()
    m.email = ""
    assert '이메일 형식이 올바르지 않습니다.' in m.verify()
    m.email = "test@test."
    assert '이메일 형식이 올바르지 않습니다.' in m.verify()
    m.email = "t@test.abcdddsdddddddddddddddddddddfdfdfd"
    assert "이메일은 최소 6자 부터 30자 입니다." in m.verify()
    m.email = "test@test.test"
    m.password = ""
    assert '비밀번호는 최소 6자 부터 30자 입니다.' in m.verify()
    m.password = "abc"
    assert "비밀번호는 최소 6자 부터 30자 입니다." in m.verify()
    m.password = "abcaskdjaskdjaksdjaskdjaskdjaskdjaskdjaskdjaskdjasdkjasdk"
    assert "비밀번호는 최소 6자 부터 30자 입니다." in m.verify()
    m.password = "test1234"
    assert True is m.verify()[0]
