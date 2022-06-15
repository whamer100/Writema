import pytest
from writema import Writema, WritemaFloatTypes, WritemaTypes
import io
from struct import pack, unpack


def test_Writema_BytesIO_check():
    assert type(Writema(io.BytesIO()).get_io()) == io.BytesIO


@pytest.mark.xfail
def test_Writema_path_string_invalidType():
    # to get rid of the warning, intentional exception
    # noinspection PyTypeChecker
    Writema(69)


def test_Writema_buffer_fulltest():
    w = Writema()
    w.write(1, 42)
    w.write(2, 2448)
    w.write(4, 694201337)
    w.write(8, 2396795999211369490)
    e_f64 = 2.718281828459045
    e_f32 = unpack(">f", pack(">f", e_f64))[0]  # convert to float32
    w.write("d", e_f64)
    w.write("f", e_f32)
    w.bytes(b"Hello, World!")
    with open("./tests/test.bin", "rb") as fp:
        data = fp.read()
    assert data == w.get_buffer()
    assert data == w.get_io().read()


def test_Writema_buffer_fulltest_names():
    w = Writema()
    w.write("byte",  42)
    w.write("short", 2448)
    w.write("int",   694201337)
    w.write("long",  2396795999211369490)
    e_f64 = 2.718281828459045
    e_f32 = unpack(">f", pack(">f", e_f64))[0]  # convert to float32
    w.write("double", e_f64)
    w.write("float", e_f32)
    w.bytes(b"Hello, World!")
    with open("./tests/test.bin", "rb") as fp:
        data = fp.read()
    assert data == w.get_buffer()
    assert data == w.get_io().read()


def test_Writema_buffer_fulltest_alt():
    w = Writema()
    w.write(WritemaTypes.byte,  42)
    w.write(WritemaTypes.short, 2448)
    w.write(WritemaTypes.int,   694201337)
    w.write(WritemaTypes.long,  2396795999211369490)
    e_f64 = 2.718281828459045
    e_f32 = unpack(">f", pack(">f", e_f64))[0]  # convert to float32
    w.write(WritemaFloatTypes.double, e_f64)
    w.write(WritemaFloatTypes.float, e_f32)
    w.bytes(b"Hello, World!")
    with open("./tests/test.bin", "rb") as fp:
        data = fp.read()
    assert data == w.get_buffer()
    assert data == w.get_io().read()


def test_Writema_writing_fulltest():
    w = Writema("./tests/writetest.bin")
    w.write(1, 42)
    w.write(2, 2448)
    w.write(4, 694201337)
    w.write(8, 2396795999211369490)
    e_f64 = 2.718281828459045
    e_f32 = unpack(">f", pack(">f", e_f64))[0]  # convert to float32
    w.write("d", e_f64)
    w.write("f", e_f32)
    w.bytes(b"Hello, World!")
    w.save()
    with open("./tests/test.bin", "rb") as fp:
        data = fp.read()
    with open("./tests/writetest.bin", "rb") as wp:
        wdata = wp.read()
    assert data == wdata


def test_Writema_endianness_check():
    w = Writema()
    w.write(4, 2018915346)
    w.set_endianness("big")
    w.write(4, 2018915346)
    w.set_endianness("little")
    w.write(4, 2018915346)
    assert w.get_buffer() == b"\x12\x34\x56\x78\x78\x56\x34\x12\x12\x34\x56\x78"
