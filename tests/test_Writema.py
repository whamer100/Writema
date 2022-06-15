import pytest
from src.writema.writema import Writema, WritemaTypes
import io
from math import isclose
from struct import pack, unpack


def test_Writema_BytesIO_check():
    assert type(Writema(io.BytesIO()).get_io()) == io.BytesIO


@pytest.mark.xfail
def test_Writema_path_string_invalidType():
    # to get rid of the warning, intentional exception
    # noinspection PyTypeChecker
    Writema(69)
