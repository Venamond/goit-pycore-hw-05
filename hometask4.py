# decorator to handle input errors 
def input_error(func):
    """
     Decorator to handle input errors for functions that process user input.
     This decorator catches specific exceptions such as ValueError, KeyError, and IndexError,
     and returns user-friendly error messages instead of raising exceptions.
     
     Args:
         func (callable): The function to be decorated.
     Returns:
         callable: The decorated function that handles input errors.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid number of arguments. Please check your input."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return inner


@input_error
def parse_input(user_input: str)-> tuple[str, ...]:
    """
    Parses user input into a command and its arguments.
    This function splits the input string into a command and its arguments,
    ensuring that the command is in lowercase and stripped of leading/trailing whitespace.
    If the input is empty, it returns an empty tuple.

    Args:   
        user_input (str): The input string from the user.
    Returns:   
        tuple[str, ...]: A tuple containing the command and its arguments.
    """

    if not user_input.strip(): 
        return ("",)  # Return a tuple with an empty string if input is empty
    
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args:tuple[str, ...] , contacts: dict)-> str:  
    """
    Adds a new contact or updates an existing contact's phone number.
    If the contact already exists, it prompts the user to update the phone number.

    Args: 
        args (tuple[str, str]): A tuple containing the contact name and phone number.
        contacts (dict): A dictionary containing contact names as keys and phone numbers as values. 
    
    """
    # raise ValueError if the number of arguments is not equal to 2
    name, phone = args
    if name in contacts:
        user_result = input(f"Contact {name} already exists, phone: {contacts[name]}. Do you want to update the phone number? (y/n): ").strip().lower()   
        if user_result != 'y': 
            return "Contact not added."
        else:
            contacts[name] = phone
            return "Contact updated."
    else:
        contacts[name] = phone
        return "Contact added."

@input_error
def change_contact(args: tuple[str, ...], contacts: dict) -> str:   
    """
    Changes the phone number for an existing contact.
   
     Args: 
        args (tuple[str, str]): A tuple containing the contact name and the new phone number.
        contacts (dict): A dictionary containing contact names as keys and phone numbers as values.
    """

    # raise ValueError if the number of arguments is not equal to 2    
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        # raise KeyError if the contact does not exist
        raise KeyError
    
@input_error   
def show_phone(args: tuple[str, ...], contacts: dict) -> str:
    """
    Returns the phone number for a given contact name.
    
    Args: 
        name (str): The name of the contact.
        contacts (dict): A dictionary containing contact names as keys and phone numbers as values.
    """
    # raise index error if targs is empty
    name = args[0].strip()
    # raise KeyError if the contact does not exist
    return f"Phone number for {name} is {contacts[name]}."

@input_error
def show_all(contacts: dict) -> str:  
    """
    Returns a string representation of all contacts and their phone numbers. 
    
    Args: 
        contacts (dict): A dictionary containing contact names as keys and phone numbers as values.  
    """

    if not contacts: 
        return "No contacts available."
    result=""

    for name, phone in contacts.items():
        result += f"\n{name}: {phone}"
    return result

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))   
        elif command == "phone":
            print(show_phone(args, contacts))    
        elif command == "all":
            print(show_all(contacts))  
        else:
            print("Invalid command.")
    

if __name__ == "__main__":
    main()