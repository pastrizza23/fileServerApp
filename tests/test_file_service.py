"""Test with pytest for file services"""
from src.file_service import FileService as fs


def test_create_file(tmpdir):
    """Test file creation capability"""
    file = tmpdir.join("test.txt")
    fs.create_file(file.strpath)
    assert file.read()


def test_delete_no_existing_file():
    """Test deleting files capability on no existing file"""
    assert fs.delete_file("I`m not exist") is False, "Can`t delete non existing file"


def test_delete_file(tmpdir):
    """Test deleting files capability"""
    file = tmpdir.mkdir("mydir").join("myfile")
    file.write_text("content", "utf-8")
    assert fs.delete_file(file.strpath)


def test_read_file(tmpdir):
    """Test reading file in utf-8 encoding"""
    file = tmpdir.mkdir("mydir").join("myfile")
    file.write_text("content", "utf-8")
    assert fs.read_file(file.strpath) == "content"


def test_get_metadata(tmpdir):
    """Test gathering metadata"""
    file = tmpdir.mkdir("mydir").join("myfile")
    file.write_text("content", "utf-8")
    assert fs.get_metadata(file.strpath) != {}
