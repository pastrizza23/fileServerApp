"""Test with pytest for file services"""
from src.crypto_file_service import CryptoFileService as fs


def test_verify_true(tmpdir):
    file = tmpdir.join("test.txt")
    fs.create_file(file.strpath)
    fs.sign_file(fs(), file.strpath)
    assert fs.verify_signature(fs(), file.strpath)


def test_verify_false(tmpdir):
    file = tmpdir.join("test.txt")
    fs.create_file(file.strpath)
    fs.sign_file(fs(), file.strpath)
    with open(file.strpath, "wb") as f:
        f.write(b"dummy")

    assert fs.verify_signature(fs(), file.strpath) is False
