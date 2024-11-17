import csv


class Interpreter:
    def __init__(self, path_to_bin, limit):
        self.registers = [0] * limit
        self.code = 0
        try:
            with open(path_to_bin, 'rb') as file:
                self.code = int.from_bytes(file.read(), byteorder='little', signed=True)
        except FileNotFoundError:
            print('Файл не найден')

    def interpret(self):
        while self.code != 0:
            a = self.code & ((1 << 4) - 1)
            match a:
                case 5:
                    self.load_constant()
                case 2:
                    self.read_memory()
                case 6:
                    self.write_memory()
                case 10:
                    self.abs()
                case _:
                    self.code >>= 1
        self.dump_result()

    def dump_result(self):
        with open('result.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(('Регистр', 'Значение'))
            for ind, val in enumerate(self.registers):
                writer.writerow((f'R{ind}', val))

    def load_constant(self):
        b = (self.code & ((1 << 32) - 1)) >> 4
        c = (self.code & ((1 << 51) - 1)) >> 32
        self.code >>= 56

        self.registers[b] = c

    def read_memory(self):
        b = (self.code & ((1 << 32) - 1)) >> 4
        c = (self.code & ((1 << 41) - 1)) >> 32
        d = (self.code & ((1 << 69) - 1)) >> 41
        self.code >>= 72

        self.registers[b] = self.registers[c + d]

    def write_memory(self):
        b = (self.code & ((1 << 32) - 1)) >> 4
        c = (self.code & ((1 << 60) - 1)) >> 32
        self.code >>= 64

        self.registers[b] = self.registers[b]

    def abs(self):
        b = (self.code & ((1 << 13) - 1)) >> 4
        c = (self.code & ((1 << 41) - 1)) >> 13
        d = (self.code & ((1 << 69) - 1)) >> 41
        self.code >>= 72

        self.registers[c] = abs(self.registers[b + d])
