from bitarray import bitarray


class Assembler:
    def __init__(self, path_to_code, path_to_log=None):
        self.path_to_log = path_to_log
        self.commands = []
        try:
            with open(path_to_code, 'rt') as file:
                self.commands = file.readlines()
        except FileNotFoundError:
            print('Файл не найден')

    def make_bin(self, path_to_bin):
        with open(path_to_bin, 'wb') as file:
            for command in self.commands:
                name, body = command.split(' ', 1)
                body = tuple(map(int, body.split()))
                match name:
                    case 'CONST':
                        file.write(Assembler.load_constant(*body))
                    case 'READ':
                        file.write(Assembler.read_memory(*body))
                    case 'WRITE':
                        file.write(Assembler.write_memory(*body))
                    case 'ABS':
                        file.write(Assembler.abs(*body))

    @staticmethod
    def load_constant(b, c):
        bits = (c << 32) | (b << 4) | 5
        return bits.to_bytes(7, byteorder='little', signed=True)

    @staticmethod
    def read_memory(b, c, d):
        bits = (d << 41) | (c << 32) | (b << 4) | 2
        return bits.to_bytes(9, byteorder='little', signed=True)

    @staticmethod
    def write_memory(b, c):
        bits = (c << 32) | (b << 4) | 6
        return bits.to_bytes(8, byteorder='little', signed=True)

    @staticmethod
    def abs(b, c, d):
        bits = (d << 41) | (c << 13) | (b << 4) | 10
        return bits.to_bytes(9, byteorder='little', signed=True)