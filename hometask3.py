import sys, pathlib
from itertools import zip_longest
from collections import Counter
from  datetime import datetime

RED   = "\033[31m"
RESET = "\033[0m"

def validation_string(data: dict) -> str:
    """
    Validates the log line format.
    
    Args:
        data (dict): A dictionary containing log data.
    
    Returns:
        str: A validation string indicating the result of the validation.
            If the log line is valid, returns an empty string.
    """
    if not data.get('date') or not data.get('time') or not data.get('level') or not data.get('message'):
        return "Invalid log line format"
    
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
        datetime.strptime(data['time'], '%H:%M:%S')
    except ValueError:
        return "Invalid date or time format"
    
    if data['level'].upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        return f"Invalid log level: {data['level']}"
    
    return ""
    

def parse_log_line(line: str) -> dict:
    """
    Parses a single line of log data into a dictionary.

    Args:
        line (str): A single line of log data.
    Returns:
        dict: A dictionary with keys 'date', 'time', 'level', and 'message'.
              Returns None if the line is empty or invalid.
    """
    if not line.strip():
        return None
    
    keys = ['date', 'time', 'level', 'message']
    # TODO: validation string
    parts = line.split(maxsplit=3)
    # deleting system-specific line endings
    parts = [part.rstrip('\r\n') for part in parts]
    return dict(zip_longest(keys, parts, fillvalue=None))

def load_logs(file_path: str) -> list:
    """
    Loads logs from a file and parses each line into a dictionary.

    Args:
        file_path (str): The path to the log file.
    Returns:
        list: A list of dictionaries, each representing a log entry.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        logs = []
        line_number = 0
        for line in file:
            line_number += 1
            log_dic = parse_log_line(line)
            if log_dic:
                error = validation_string(log_dic)
                if error:
                    raise ValueError(f"Invalid log line at {line_number}: {error}  - {line.strip()}")
                # Append the log dictionary to the list if it is valid
                logs.append(log_dic)
        return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Filters logs by a specific log level.

    Args:
        logs (list): A list of log dictionaries.
        level (str): The log level to filter by (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
    Returns:
        list: A list of log dictionaries that match the specified log level.
    """
    return list(
            filter(
            lambda log: log.get('level').upper() == level.upper(),logs)
            )

def count_logs_by_level(logs: list) -> dict:
     """
     Counts the number of logs for each log level.

     Args:
            logs (list): A list of log dictionaries.
    Returns:
            dict: A dictionary with log levels as keys and their counts as values.

     """
     return Counter(log.get('level').upper() for log in logs)

def display_log_counts(counts: dict):
    """
    Displays the counts of logs by their levels in a formatted table.
    This function prints the log levels and their corresponding counts in a table format.

    Args:
        counts (dict): A dictionary with log levels as keys and their counts as values.
    Returns:
        None: This function prints the output directly to the console.
    """
    if not counts:
        print("Файл порожній, не містить логів.")
        return
    
    col1, col2 = "Рівень логування", "Кількість"
    # calculating the maximum width for each column
    w1 = max(len(col1), *(len(level) for level in counts))
    w2 = max(len(col2), *(len(str(cnt)) for cnt in counts.values()))
    
    # printing header
    print(f"{col1:<{w1}} | {col2:>{w2}}")
    print(f"{'-'*w1} | {'-'*w2}")
    
    # printing each level and its count
    for level, cnt in counts.items():
        line = f"{level:<{w1}} | {cnt:>{w2}}"
        if level.upper() == "ERROR":
            line = f"{RED}{level:<{w1}}{RESET} | {cnt:>{w2}}"
        else:
             line = f"{level:<{w1}} | {cnt:>{w2}}"
        print(line)
    return

def main():
    """
    The main function for processing arguments and running the script.

    Arguments:
        path_file (str): The path to the log file.    
        level_arg (str): The log level to filter logs by (optional).
    """
    # Clear the console screen
    print("\033[2J\033[H", end='')
    # Check if the user provided a file path as a command line argument
    if len(sys.argv) == 1:
        print("Please provide a file path as a command line argument.")
        sys.exit(1) 
    # Check if the provided path exists
    path_file= sys.argv[1]
    if not pathlib.Path(path_file).exists():
        print(f"Error: The provided path '{path_file}' does not exist.")
        sys.exit(2)
    # Check if the provided path is a file  
    if not pathlib.Path(path_file).is_file():
        print(f"The provided path is not a file: {path_file}")
        sys.exit(2)
    try:
        # Load logs from the file
        list_logs = load_logs(path_file)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(3)
    except Exception as e:
        print(f"An unexpected error occurred while reading file {path_file}: {e}")
        sys.exit(4)

    # Displaying the total level of logs
    display_log_counts(count_logs_by_level(list_logs))

    # Displaying the logs details for a specific level if provided
    if len(sys.argv) > 2:
        level_arg = sys.argv[2].upper()
        filter_list= filter_logs_by_level(list_logs, level_arg)
        if filter_list:
            print(f"\nДеталі логів для рівня '{level_arg}':")
            for log in filter_list:
                print(f"{log['date']} {log['time']} {log['level']} {log['message']}")
        else:
            print(f"\nНемає логів для рівня '{level_arg}'.")


if __name__ == "__main__":
   main()


