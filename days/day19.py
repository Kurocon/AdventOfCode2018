import re
from collections import defaultdict
from typing import List, Tuple, Dict, Set

from days import AOCDay, day


@day(19)
class DayTemplate(AOCDay):

    test_input = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".split("\n")

    program: List[Tuple[str, int, int, int]] = []
    pc_register: int = -1
    pc = 0

    def common(self, input_data):
        # input_data = self.test_input
        self.program = []
        self.pc = 0

        self.pc_register = int(re.findall(r'\d+', input_data[0])[0]) if "#ip" in input_data[0] else -1

        for line in input_data[1:]:
            parts = line.split(" ")
            self.program.append((
                parts[0],
                int(parts[1]),
                int(parts[2]),
                int(parts[3]),
            ))

    def part1(self, input_data):
        # Execute program
        registers = [0, 0, 0, 0, 0, 0]

        try:
            while True:
                instr = self.program[self.pc]
                registers = self.execute_instruction(registers, instr)
        except IndexError:
            yield "Terminated."

        yield "Register 0 has value {}".format(registers[0])

    def part2(self, input_data):
        # Execute program
        registers = [1, 0, 0, 0, 0, 0]

        try:
            while True:
                # Optimization after reverse engineering assembly
                if self.pc == 2 and registers[5] != 0:
                    if registers[3] % registers[5] == 0:
                        registers[0] += registers[5]
                    registers[4] = 0
                    registers[2] = registers[3]
                    self.pc = 12
                    continue

                instr = self.program[self.pc]
                registers = self.execute_instruction(registers, instr)
        except IndexError:
            yield "Terminated."

        yield "Register 0 has value {}".format(registers[0])

    def execute_instruction(self, input_registers: List[int], instruction: Tuple[str, int, int, int]) -> List[int]:
        if self.pc_register >= 0:
            input_registers[self.pc_register] = self.pc

        res = opcodes[instruction[0]](
            regs=input_registers[:], a=instruction[1], b=instruction[2], c=instruction[3]
        )

        # print("ip={} {} {} {}".format(self.pc, input_registers, instruction, res))

        if self.pc_register >= 0:
            self.pc = res[self.pc_register]
        self.pc += 1
        return res


def get_r(registers: List[int], reg: int):
    return registers[reg]


def set_r(registers: List[int], reg: int, val: int) -> List[int]:
    registers[reg] = val
    return registers


def addr(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) + get_r(regs, b))


def addi(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) + b)


def mulr(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) * get_r(regs, b))


def muli(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) * b)


def banr(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) & get_r(regs, b))


def bani(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) & b)


def borr(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) | get_r(regs, b))


def bori(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a) | b)


def setr(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, get_r(regs, a))


def seti(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, a)


def gtir(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, 1 if a > get_r(regs, b) else 0)


def gtri(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, 1 if get_r(regs, a) > b else 0)


def gtrr(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, 1 if get_r(regs, a) > get_r(regs, b) else 0)


def eqir(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, 1 if a == get_r(regs, b) else 0)


def eqri(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, 1 if get_r(regs, a) == b else 0)


def eqrr(regs: List[int], a: int, b: int, c: int) -> List[int]:
    return set_r(regs, c, 1 if get_r(regs, a) == get_r(regs, b) else 0)


opcodes = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}
