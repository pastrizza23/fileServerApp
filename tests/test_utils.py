import utils.utils as utils
import src.file_service as fs
""""Test with pytest for utils"""


def test_generate_data():
    """Test if generated data eq 100"""
    assert len(utils.generate_data()) == 100


def test_get_metadata(tmpdir):
    """Test get_metadata method"""
    file = tmpdir.mkdir("mydir").join("myfile")
    file.write_text("content", "utf-8")
    try:
        utils.metadata_str(fs.get_metadata(file.strpath))
    except Exception as exc:
        assert False


