import os
import glob
from typing import Generator

import requests

from aocdays import AOCDays

modules = filter(lambda x: not x.startswith('_'), glob.glob(os.path.dirname(__file__) + "/*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules]


def day(day_number):
    def day_decorator(cls):
        if not str(cls.__module__).replace("days.", "").startswith("_"):
            AOCDays.get_instance().add_day(day_number, cls)
        return cls
    return day_decorator


class AOCDay:
    year = 2018
    day_number = 0
    session_token = ""
    input_filename = ""
    output_filename = ""
    input_data = None

    def __init__(self, year, day_number, session_token):
        self.year = year
        self.day_number = day_number
        self.session_token = session_token
        self.input_filename = os.path.join(os.path.dirname(__file__), "../inputs/day{}_{}".format(self.day_number, "input"))
        self.output_filename = os.path.join(os.path.dirname(__file__), "../outputs/day{}_{}".format(self.day_number, "output"))

    def download_input(self):
        if os.path.isfile(self.input_filename):
            return

        print("Could not find input data for day {}, please wait while I download it...".format(self.day_number))

        input_url = "https://adventofcode.com/{}/day/{}/input".format(self.year, self.day_number)
        result = requests.get(input_url, cookies={'session': self.session_token})
        if result.status_code == 200:
            self.input_data = result.text
            with open(self.input_filename, 'w') as f:
                f.write(result.text)
        else:
            raise ConnectionError("Could not connect to AoC website to download input data. "
                                  "Error code {}: {}".format(result.status_code, result.text))

    def load_input(self):
        if self.input_filename:
            with open(self.input_filename, 'r') as f:
                self.input_data = [int(x.strip()) for x in f.readlines()]

    def run(self):
        self.download_input()
        self.load_input()

        if os.path.isfile(self.output_filename):
            os.remove(self.output_filename)

        with open(self.output_filename, 'w') as output_file:
            def dprint(thing):
                print(thing, file=output_file)
                print(thing)
                
            common = self.common()
            if common:
                dprint("== Common ==")
                for x in common:
                    dprint(x)
                dprint("")
    
            dprint("== Part 1 ==")
            printed = False
            for x in self.part1():
                if not printed:
                    printed = True
                dprint(x)
            if not printed:
                dprint("(no output)")
            dprint("")
    
            common = self.common()
            if common:
                dprint("== Common ==")
                for x in common:
                    dprint(x)
                dprint("")
    
            dprint("== Part 2 ==")
            printed = False
            for x in self.part2():
                if not printed:
                    printed = True
                dprint(x)
            if not printed:
                dprint("(no output)")
            dprint("")

    def common(self) -> Generator:
        pass

    def part1(self) -> Generator:
        pass

    def part2(self) -> Generator:
        pass
