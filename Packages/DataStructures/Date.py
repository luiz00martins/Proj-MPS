
class Date():
    def __init__(self, day : int, month : int, year : int):
        if day < 1 or day > 31:
            raise ValueError(f'Day {day} is outside of range [0,31]')
        if month < 1 or month > 12:
            raise ValueError(f'Month {month} is outside of range [1,12]')

        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return f"{self.day:02d}/{self.month:02d}/{self.year:04d}"

    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            if self.month == other.month:
                if self.day < other.day:
                    return True

        return False

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day

    def __gt__(self, other):
        return other < self

    def __ne__(self, other):
        not self == other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other



