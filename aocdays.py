class AOCDays:
    _instance = None
    days = None

    def __init__(self):
        self.days = {i+1: None for i in range(25)}

    def add_day(self, number: int, cls: 'days.AOCDay') -> None:
        self.days[number] = cls

    def get_day(self, number: int) -> 'days.AOCDay':
        return self.days[number]

    @classmethod
    def get_instance(cls) -> 'AOCDays':
        if not cls._instance:
            cls._instance = AOCDays()
        return cls._instance

