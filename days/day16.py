import re
from collections import defaultdict
from typing import List, Tuple, Dict, Set

from days import AOCDay, day

BEFORE_REGEX = r"Before:\s+\[(?P<r1>[0-9]+),\s+(?P<r2>[0-9]+),\s+(?P<r3>[0-9]+),\s+(?P<r4>[0-9]+)\]"
OPCODE_REGEX = r"(?P<opcode>[0-9]+)\s+(?P<a>[0-9]+)\s+(?P<b>[0-9]+)\s+(?P<c>[0-3]+)"
AFTER_REGEX = r"After:\s+\[(?P<r1>[0-9]+),\s+(?P<r2>[0-9]+),\s+(?P<r3>[0-9]+),\s+(?P<r4>[0-9]+)\]"

@day(16)
class DayTemplate(AOCDay):

    test_input = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]""".split("\n")

    instructions: List[Tuple[List[int], List[int], List[int]]]
    instruction_set = {}
    program: List[List[int]] = []

    def common(self, input_data):
        # input_data = self.test_input
        self.instructions = []
        self.instruction_set = {}
        self.program = []
        i = 0
        first_section = True
        while i < len(input_data):
            entry = []
            if input_data[i] == "":
                first_section = False
                i += 2

            if first_section:
                before = re.match(BEFORE_REGEX, input_data[i]).groupdict()
                entry.append(list(map(int, [before['r1'], before['r2'], before['r3'], before['r4']])))
                i += 1
                instruction = re.match(OPCODE_REGEX, input_data[i]).groupdict()
                entry.append(list(map(int, [instruction['opcode'], instruction['a'], instruction['b'], instruction['c']])))
                i += 1
                after = re.match(AFTER_REGEX, input_data[i]).groupdict()
                entry.append(list(map(int, [after['r1'], after['r2'], after['r3'], after['r4']])))
                i += 2
                self.instructions.append(entry)
            else:
                instruction = re.match(OPCODE_REGEX, input_data[i]).groupdict()
                self.program.append(list(map(int, [instruction['opcode'], instruction['a'], instruction['b'], instruction['c']])))
                i += 1

    def part1(self, input_data):
        above_three_count = 0
        for instruction in self.instructions:
            instr_id, count, instrs = self.identify_instruction(*instruction)
            if count >= 3:
                above_three_count += 1
        yield "{} samples behave like three or more opcodes.".format(above_three_count)

    def part2(self, input_data):
        # Find all possible instructions for the given samples
        possibilities: Dict[int, Set[str]] = defaultdict(set)
        for instruction in self.instructions:
            instr_id, count, instrs = self.identify_instruction(*instruction)
            possibilities[instr_id].update(instrs)

        # Identify instructions
        while possibilities:
            for op, options in possibilities.items():
                if len(options) == 1:
                    opcode, instruction = op, options.pop()
                    yield "Identified {} as {}".format(opcode, instruction)
                    break
            else:
                yield "Done?"
                return

            del possibilities[opcode]
            for op in possibilities.keys():
                try:
                    possibilities[op].remove(instruction)
                except KeyError:
                    pass
            self.instruction_set[opcode] = instruction

        yield "All instructions identified; running program..."

        # Execute program
        registers = [0, 0, 0, 0]
        for instr in self.program:
            registers = self.execute_instruction(registers, instr)

        yield "Register 0 has value {}".format(registers[0])

    def identify_instruction(self, input_registers: List[int], instruction: List[int], output_registers: List[int]) -> Tuple[int, int, List[str]]:
        count = 0
        ops = []
        for code, func in opcodes.items():
            output: List[int] = func(regs=input_registers[:], a=instruction[1], b=instruction[2], c=instruction[3])
            if output == output_registers:
                count += 1
                ops.append(code)
        return instruction[0], count, ops

    def execute_instruction(self, input_registers: List[int], instruction: List[int]) -> List[int]:
        return opcodes[self.instruction_set[instruction[0]]](
            regs=input_registers[:], a=instruction[1], b=instruction[2], c=instruction[3]
        )


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
