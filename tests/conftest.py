from pathlib import Path
import pytest
import pandas as pd
from pyam import IamDataFrame, IAMC_IDX
from nomenclature import DataStructureDefinition


here = Path(__file__).parent
TEST_DATA_DIR = here / "data"


TEST_DF = pd.DataFrame(
    [
        ["model_a", "scen_a", "World", "Primary Energy", "EJ/yr", 1, 6.0],
        ["model_a", "scen_a", "World", "Primary Energy|Coal", "EJ/yr", 0.5, 3],
        ["model_a", "scen_b", "World", "Primary Energy", "EJ/yr", 2, 7],
    ],
    columns=IAMC_IDX + [2005, 2010],
)


@pytest.fixture(scope="session")
def simple_definition():
    yield DataStructureDefinition(TEST_DATA_DIR / "validation_nc")


@pytest.fixture(scope="session")
def extras_definition():
    yield DataStructureDefinition(TEST_DATA_DIR / "extras_nc")


@pytest.fixture(scope="function")
def simple_df():
    df = IamDataFrame(TEST_DF)
    add_meta(df)
    yield df


def add_meta(df):
    """Add simple meta indicators"""
    if len(df.index) == 1:
        df.set_meta([1.0], "number")
        df.set_meta(["foo"], "string")
    if len(df.index) == 2:
        df.set_meta([1.0, 2.0], "number")
        df.set_meta(["foo", "bar"], "string")
