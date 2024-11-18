import pytest
from interpreter import Interpreter
from assembler import Assembler


@pytest.fixture
def assembler():
    a = Assembler('code.asm', 'logs/logs.csv')
    return a


@pytest.fixture
def interpreter():
    i = Interpreter('test.bin', 15)
    return i


@pytest.mark.parametrize(
    'method, args, expected',
    [
        (Assembler.load_constant, (229, 979), b'U\x0e\x00\x00\xd3\x03\x00'),
        (Assembler.read_memory, (92, 4, 106), b'\xc2\x05\x00\x00\x04\xd4\x00\x00\x00'),
        (Assembler.write_memory, (970, 629), b'\xa6<\x00\x00u\x02\x00\x00'),
        (Assembler.abs, (226, 178, 487), b'*N\x16\x00\x00\xce\x03\x00\x00'),
    ]
)
def test_static_methods(method, args, expected):
    assert method(*args) == expected


def test_task(interpreter):
    interpreter.interpret()
    assert interpreter.registers == [5, 5, 6, 8, 0, 0, 5, 524283, 6, 524280, 0, 0, 6, 0, 0]