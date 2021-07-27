import random
from main import chat_id
import datetime

small_alphabets = "abcdefghijklmnopqrstuvwxyz"
cap_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
symbols = "!@#%&"

universal_set = list(small_alphabets) + list(cap_alphabets) + list(numbers) + list(symbols)

def pwdgen(length=8,set=universal_set):
    password = ''
    for i in range(int(length)):
        x = random.choice(set)
        password += x
        
    return password

saved_pwds = f"{chat_id}.txt"

def savepwd(pwd,info):
    datetime = datetime.datetime()
    pwd_line = f"Password: {pwd}\nPassword info: {info}\nPassword saved at {datetime}\n\n"
    
    with open(saved_pwds, 'r+') as file:
        content = file.read()
        file.seek(0, 0)
        file.write(pwd_line.rstrip('\r\n') + '\n' + content)
        file.close()    
