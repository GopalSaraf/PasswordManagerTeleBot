import random

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


def savepwd(pwd,info):
    import datetime
    dt = datetime.datetime.now()
    pwd_line = f"Password: {pwd}\nPassword info: {info}\nPassword saved at {dt}\n\n"
    
    f = open("SavedPasswords.txt","w+")
    f.close()
    with open("SavedPasswords.txt", 'r+') as file:
        content = file.read()
        file.seek(0, 0)
        file.write(pwd_line.rstrip('\r\n') + '\n' + content)
        file.close()    
