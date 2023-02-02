from core.api.user.models import User


def test_verify():
    m = User()
    m.email = "test@test.test"
    m.password = "test"
    assert True, m.verify()
    m.email = "a@b.c"
    assert True, m.verify()
    m.email = "abcd"
    assert (False, '이메일 형식이 올바르지 않습니다.'), m.verify()
    m.email = ""
    assert (False, '이메일 형식이 올바르지 않습니다.'), m.verify()
    m.email = "test@test."
    assert (False, '이메일 형식이 올바르지 않습니다.'), m.verify()
    m.email = "t@test.abcdddsdddddddddddddddddddddfdfdfd"
    assert (False, '이메일은 최소 4자 부터 30자 입니다.'), m.verify()

    m.email = "test@test.test"
    m.password = ""
    assert (False, '비밀번호는 최소 4자 부터 30자 입니다.'), m.verify()
    m.password = "abc"
    assert (False, '비밀번호는 최소 4자 부터 30자 입니다.'), m.verify()
    m.password = "abcaskdjaskdjaksdjaskdjaskdjaskdjaskdjaskdjaskdjasdkjasdk"
    assert (False, '비밀번호는 최소 4자 부터 30자 입니다.'), m.verify()

    m.password = "test"
    assert True, m.verify()

