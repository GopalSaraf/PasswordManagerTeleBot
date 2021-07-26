import random

small_alphabets = "abcdefghijklmnopqrstuvwxyz"
cap_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
symbols = "!@#%&"

universal_set = list(small_alphabets) + list(cap_alphabets) + list(numbers) + list(symbols)

def pwdgen(length=8)
    password = ''
    for i in range(int(length)):
        x = random.choice(universal_set)
        password += x
        
    return password
