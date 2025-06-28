import re
from typing import Iterator, Callable

def generator_numbers(text: str)-> Iterator[float]:
    """
    Extracts all numbers from the given text and yields them as floats. 
    This function uses a regular expression to find numbers in the text
    and yields each number as a float.

    Args:
        text (str): The input text containing numbers.
    Yields: 
        float: Each number found in the text as a float.
    """
    pattern = re.compile(r"(?:\d*\.\d+|\d+\.\d*|\d+)")
    for match in re.finditer(pattern, text):
        yield float(match.group())

def sum_profit(text: str, func: Callable)-> float:
    """
    Calculates the sum of all numbers in the text using a generator function.
    
    Args:
        text (str): The input text containing numbers.
        func (Callable): A generator function that yields numbers from the text.
    Returns:
        float: The sum of all numbers found in the text.
    """
    return sum(func(text))
    


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід працівника: {total_income}")
