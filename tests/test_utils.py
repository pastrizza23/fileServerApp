""""Test with pytest for utils"""
import utils.utils as utils
import src.file_service as fs
from utils.config_parser import config


def test_generate_data():
    """Test if generated data eq configured len"""
    assert len(utils.generate_data()) == config()["base"]["data_length"]


def test_get_metadata(tmpdir):
    """Test get_metadata method"""
    file = tmpdir.mkdir("mydir").join("myfile")
    file.write_text("content", "utf-8")
    try:
        utils.metadata_str(fs.get_metadata(file.strpath))
    except Exception as exc:
        assert False


