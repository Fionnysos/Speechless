import pytest
import backend.auth
import backend.exceptions

@pytest.mark.parametrize("password", ["Diamond12312", "testPassword12:;"])
class TestHashPassword:

    def test_is_not_plain_password(self, password):
        result = backend.auth.hash_password(password)
        assert result != password

    def test_output_is_string(self, password):
        result = backend.auth.hash_password(password)
        assert isinstance(result, str)

@pytest.mark.parametrize("password, expected", [("", backend.exceptions.EmptyPasswordError)])
def test_empty_string(password, expected):
    with pytest.raises(expected):
        backend.auth.hash_password(password)

@pytest.mark.parametrize("password, hashed_password", [("test12345678", "$2b$12$LwCTz/h8D1GCFWLRRzcwbOnTSR88vi1A6fVz8tFxEuKuHX1eBcpE2")])
def test_output_is_bool(password, hashed_password):
    result = backend.auth.verify_password(password, hashed_password)
    assert isinstance(result, bool)

@pytest.mark.parametrize("wrong_password, hashed_password, expected",
                             [("test12348", "$2b$12$LwCTz/h8D1GCFWLRRzcwbOnTSR88vi1A6fVz8tFxEuKuHX1eBcpE2", backend.exceptions.WrongPasswordError)])
def test_wrong_password(wrong_password, hashed_password, expected):
    with pytest.raises(expected):
        backend.auth.verify_password(wrong_password, hashed_password)

@pytest.mark.parametrize("password, hashed_password",
                                 [("test12345678", "$2b$12$LwCTz/h8D1GCFWLRRzcwbOnTSR88vi1A6fVz8tFxEuKuHX1eBcpE2")])
def test_hash_password(password, hashed_password):
        result = backend.auth.verify_password(password, hashed_password)
        assert result == True

