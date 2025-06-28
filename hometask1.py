

from typing import Callable

def caching_fibonacci()-> Callable[[int], int]:
    """
    Returns a function that computes Fibonacci numbers with caching.
    This function uses a dictionary to cache previously computed Fibonacci numbers
    """ 
    # Initialize a cache to store previously computed Fibonacci numbers
    # value cache is passed by reference, so it is not required nonlocal in pcocedure fibonacci
    cache ={}    
    def fibonacci(n: int) -> int:   
        """
        Computes the nth Fibonacci number using recursion and caching

        Args: 
            n (int): The index of the Fibonacci number to compute.
        Returns:
            int: The nth Fibonacci number.
        """ 
       
        if n <=0 :
            return 0   
        elif n == 1:
            return 1  
        elif n in cache:
            # Return the cached Fibonacci number if it exists   
            return cache[n]
        else:
            # Store the computed Fibonacci number in the cache  
            cache[n] = fibonacci(n-1) + fibonacci(n-2)
            return cache[n] 
    return fibonacci    

fib = caching_fibonacci()
print(fib(10))  
print(fib(15))  
