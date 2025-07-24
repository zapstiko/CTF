# Function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Take input as a string of space-separated numbers
n = input()

# Convert the input into a list of integers
numbers = list(map(int, n.split()))

# Find prime numbers in the list
prime_numbers = [num for num in numbers if is_prime(num)]

# If exactly two prime numbers are found, calculate their product
if len(prime_numbers) == 2:
    product = prime_numbers[0] * prime_numbers[1]
    print(product)
else:
    print("Not enough prime numbers in the list.")
