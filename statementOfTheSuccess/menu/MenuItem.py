from typing import Union, Callable, List


class MenuItem:
    count = 0

    def __init__(self, title, function, availability_check: Union[None, Callable, List[Callable]] = None):
        MenuItem.count += 1
        self.error_message = None
        self.number = MenuItem.count
        self.title = title
        self.function = function
        self.availability_check = availability_check

    def __str__(self):
        return f"[{self.number}] {self.title}"

    def get_availability(self):
        is_green = True
        if isinstance(self.availability_check, list):
            for func in self.availability_check:
                if not func():
                    is_green = False
                    break
        elif callable(self.availability_check):
            if not self.availability_check():
                is_green = False
        return is_green
