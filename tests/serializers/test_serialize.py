import tempfile
from pathlib import Path

import pytest
from yaml import serialize

from openpecha.serializers import EditorSerializer, EpubSerializer, HFMLSerializer


# For testing read_base_layer, add_chars and apply_layer
@pytest.fixture(scope="module")
def opf_path():
    return Path("./tests/data/serialize/tsadra/P000100.opf")


# Test HFML Serializer
# hfml_opf_path = Path("tests/data/serialize_test/hfml/hfml.opf")


@pytest.mark.skip(reason="not important")
def test_hfml_serializer():
    opf_path = "./tests/data/serialize/hfml/P000002.opf/"
    serializer = HFMLSerializer(opf_path)
    serializer.apply_layers()
    hfml_results = serializer.get_result()
    expected_hfml_paths = list(Path('./tests/data/serialize/hfml/P000002/').iterdir())
    expected_hfml_paths.sort()
    expected_hfmls = [expected_hfml for expected_hfml in expected_hfml_paths]
    for hfml_result, expected_hfml in zip(hfml_results.values(), expected_hfmls):
        assert hfml_result == expected_hfml


def test_hfml_2_tsadra_serializer(opf_path):
    with tempfile.TemporaryDirectory() as tmpdirname:
        serializer = EpubSerializer(opf_path)
        out_fn = serializer.serialize(output_path=tmpdirname)
        assert Path(out_fn).name == "P000100.epub"


def test_editor_serializer():
    opf_path = "./tests/data/serialize/tsadra/P000801/P000801.opf"
    expected_output = Path(
        "./tests/data/serialize/tsadra/editor_serializer_output.html"
    ).read_text(encoding="utf-8")
    serializer = EditorSerializer(opf_path)
    for base_name, result in serializer.serialize():
        assert base_name
        assert result == expected_output