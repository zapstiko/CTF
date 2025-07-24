# Read space-separated coefficients a0...an
coefficients = list(map(int, input().split()))
# Read the value x to evaluate at
x = int(input())

# Evaluate using Horner's method
result = 0
for coeff in reversed(coefficients):
    result = result * x + coeff

# Output the final value—the flag
print(result)
