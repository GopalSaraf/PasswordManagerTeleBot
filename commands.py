# commands

start_command = ["start"]
help_command = ["help"]
gen_random_pwd_command = ["randpwd"]
gen_spec_pwd_command = ["specpwd"]
my_pwd_command = ["mypwds"]


# messages

start_msg = "Hii {}!\nI am **password manager bot!**\nPress /help for more info."

help_msg = """Save your passwords safely here..

Here you can generate strong passwords and save them for future use.

**You can generate password by two ways in here:**
1| Generating password by random characters
2| Generating password by your specific characters

**Commands:** 
- /randpwd <<code>len</code>> <<code>info</code>>: For generating password by random characters.
- /specpwd <<code>len</code>> <<code>char</code>> <<code>info</code>>: For generating password by your specific characters. (<<code>char</code>> means characters you want to use in your password.)
- /mypwds: For getting saved passwords.

👆here in commands..
<<code>info</code>> means length of password required.
and..
<<code>info</code>> means for what you are generating password. This will be helpful to you for future use.

Thank you!
"""

gen_random_pwd_msg = "Here is your password:\n<code>{}</code>"
