from click.testing import CliRunner
from nomenclature import cli
from nomenclature.testing import assert_valid_yaml, assert_valid_structure
import pytest
import pydantic

from conftest import TEST_DATA_DIR

runner = CliRunner()


def test_cli_valid_yaml_path():
    """Check that CLI throws an error when the `path` is incorrect"""
    result_valid = runner.invoke(
        cli, ["validate-yaml", str(TEST_DATA_DIR / "incorrect_path")]
    )
    assert result_valid.exit_code == 2


def test_cli_valid_yaml():
    """Check that CLI runs through, when all yaml files in `path`
    can be parsed without errors"""
    result_valid = runner.invoke(
        cli, ["validate-yaml", str(TEST_DATA_DIR / "duplicate_code_raises")]
    )
    assert result_valid.exit_code == 0


def test_cli_valid_yaml_fails():
    """Check that CLI raises expected error when parsing an invalid yaml"""
    result_invalid = runner.invoke(
        cli, ["validate-yaml", str(TEST_DATA_DIR / "invalid_yaml")]
    )
    assert result_invalid.exit_code == 1
    match = "Parsing the yaml files failed. Please check the log for details."
    with pytest.raises(AssertionError, match=match):
        assert_valid_yaml(TEST_DATA_DIR / "invalid_yaml")


def test_cli_valid_project_path():
    """Check that CLI throws an error when the `path` is incorrect"""
    path = str(TEST_DATA_DIR / "incorrect_path")
    result_valid = runner.invoke(cli, ["validate-project", path])
    assert result_valid.exit_code == 2


def test_cli_valid_project():
    """Check that CLI runs through with existing "definitions" and "mappings"
    directory"""
    result_valid = runner.invoke(
        cli, ["validate-project", str(TEST_DATA_DIR / "structure_validation")]
    )
    assert result_valid.exit_code == 0


def test_cli_invalid_region():
    """Test that errors are correctly propagated"""
    obs = runner.invoke(
        cli, ["validate-project", str(TEST_DATA_DIR / "structure_validation_fails")]
    )
    assert obs.exit_code == 1
    assert isinstance(obs.exception, pydantic.ValidationError)
    assert "region_a" in obs.exception.errors()[0]["msg"]


def test_cli_valid_project_fails():
    """Check that CLI expected error when "definitions" directory doesn't exist"""
    path = TEST_DATA_DIR / "invalid_yaml" / "definitions"
    result_invalid = runner.invoke(
        cli, ["validate-project", str(TEST_DATA_DIR / "invalid_yaml")]
    )
    assert result_invalid.exit_code == 1

    def print_helper(_path):
        print(f"Definitions directory not found: {_path}")

    with pytest.raises(NotADirectoryError, match=print_helper(path)):
        assert_valid_structure(
            TEST_DATA_DIR / "invalid_yaml", "mappings", "definitions"
        )


def test_cli_non_default_folders():
    """Check that CLI runs through with non-default but existing "definitions" and
    "mappings" directory when the correct names are given"""
    result_valid = runner.invoke(
        cli,
        [
            "validate-project",
            str(TEST_DATA_DIR / "non-default_folders"),
            "--definitions",
            "def",
            "--mappings",
            "map",
        ],
    )
    assert result_valid.exit_code == 0


def test_cli_non_default_folders_fails():
    """Check that CLI raises expected error when non-default "definitions" and
    "mappings" directory names are not given"""
    result_valid = runner.invoke(
        cli, ["validate-project", str(TEST_DATA_DIR / "non-default_folders")]
    )
    assert result_valid.exit_code == 1


def test_cli_wrong_definitions_name():
    """Check that CLI raises expected error when a non-existing non-default directory
    is given"""
    result_valid = runner.invoke(
        cli,
        [
            "validate-project",
            str(TEST_DATA_DIR / "structure_validation"),
            "--definitions",
            "def",
        ],
    )
    assert result_valid.exit_code == 1


def test_cli_custom_dimensions():
    """Check that CLI runs through with a non-default dimension"""

    result_valid = runner.invoke(
        cli,
        [
            "validate-project",
            str(TEST_DATA_DIR / "non-default_dimensions_passing"),
            "--dimensions",
            "['variable', 'region', 'scenario']",
        ],
    )
    assert result_valid.exit_code == 0


def test_cli_custom_dimensions_empty():
    """Check that CLI raises an error when specifying an empty directory ('empty')"""

    result_valid = runner.invoke(
        cli,
        [
            "validate-project",
            str(TEST_DATA_DIR / "non-default_dimensions_failing"),
            "--dimensions",
            "['variable', 'region', 'empty']",
        ],
    )
    assert result_valid.exit_code == 1


def test_cli_custom_dimensions_fails():
    """Check that CLI raises an error when specifying a non-existent
    directory ('foo')"""

    result_valid = runner.invoke(
        cli,
        [
            "validate-project",
            str(TEST_DATA_DIR / "non-default_dimensions_passing"),
            "--dimensions",
            "['variable', 'region', 'foo']",
        ],
    )
    assert result_valid.exit_code == 1
