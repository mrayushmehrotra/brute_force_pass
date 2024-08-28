import itertools
import string
import random
import sys
import time
import multiprocessing

def try_password_chunk(password, chars, min_len, max_len, queue):
    start_time = time.time()
    
    for i in range(min_len, max_len + 1):
        for guess in itertools.product(chars, repeat=i):
            guess = ''.join(guess)
            elapsed_time = time.time() - start_time
            sys.stdout.write(f"\rTrying password: {guess}")
            sys.stdout.flush()
            if guess == password:
                queue.put((guess, elapsed_time))  # Found the password with elapsed time
                return

def brute_force_crack(password, chars, min_len, max_len, num_workers=4):
    # Create a multiprocessing queue for communicating between processes
    queue = multiprocessing.Queue()

    # Determine the chunk size for each worker
    total_len = max_len - min_len + 1
    chunk_size = total_len // num_workers

    processes = []

    for i in range(num_workers):
        start_len = min_len + i * chunk_size
        end_len = start_len + chunk_size - 1
        if i == num_workers - 1:  # Ensure the last process covers the remaining range
            end_len = max_len

        p = multiprocessing.Process(target=try_password_chunk, args=(password, chars, start_len, end_len, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Check if the password was found
    if not queue.empty():
        found_password, elapsed_time = queue.get()
        print(f"\nPassword cracked: {found_password} | Time taken: {elapsed_time:.2f}s")
    else:
        print("\nPassword not found.")

if __name__ == "__main__":
    print("Welcome to the Python Brute Force Cracking App")
    
    # Get the actual password (for testing purposes, this is predefined)
    password = input("Enter the password (for testing purposes): ")

    # Get hints from the user
    hint_chars = input("Enter characters you think are in the password (e.g., 'abc123'): ")

    # Get the length range from the user
    min_len = int(input("Enter the minimum length of the password: "))
    max_len = int(input("Enter the maximum length of the password: "))

    # Generate a pool of characters to iterate through
    all_chars = (
        list(hint_chars) +                        # User-specified characters
        list(string.ascii_lowercase) +            # Lowercase letters
        list(string.ascii_uppercase) +            # Uppercase letters
        list(string.digits) +                     # Numbers
        list('#@*&^')                             # Special characters
    )

    # Shuffle the character set for randomness
    random.shuffle(all_chars)

    # Start brute force cracking with multiprocessing
    brute_force_crack(password, all_chars, min_len, max_len)
