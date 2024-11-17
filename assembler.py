import csv


class Assembler:
    def __init__(self, path_to_code, path_to_log=None):
        self.path_to_log = path_to_log
        self.logs = []
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
                number = None
                bits = None
                match name:
                    case 'CONST':
                        number = 5
                        bits = Assembler.load_constant(*body)
                    case 'READ':
                        number = 2
                        bits = Assembler.read_memory(*body)
                    case 'WRITE':
                        number = 6
                        bits = Assembler.write_memory(*body)
                    case 'ABS':
                        number = 10
                        bits = Assembler.abs(*body)
                file.write(bits)
                self.logs.append([number, body, bits])
        self.make_log()

    def make_log(self):
        with open(self.path_to_log, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(('Тест', 'Команда'))
            for log in self.logs:
                key = []
                for name, param in zip('ABCD', [log[0], *log[1]]):
                    key.append(f'{name}={param}')
                writer.writerow(('   '.join(key), ' '.join(hex(i) for i in log[-1])))

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
