from typing import List


class AOCDays:
    _instance = None
    days = None

    def __init__(self):
        self.days = {i+1: [] for i in range(25)}

    def add_day(self, number: int, cls: 'days.AOCDay') -> None:
        self.days[number].append(cls)

    def get_day(self, number: int) -> 'List[days.AOCDay]':
        return self.days[number]

    @classmethod
    def get_instance(cls) -> 'AOCDays':
        if not cls._instance:
            cls._instance = AOCDays()
        return cls._instance

