# commands

start_command = ["start"]
help_command = ["help"]
gen_random_pwd_command = ["randpwd"]
gen_spec_pwd_command = ["specpwd"]
my_pwds_command = ["mypwds"]
search_pwd_command = ["search"]


# messages

start_msg = "Hii {}!\nI am **password manager bot!**\nI can create **strong** passwords for you and also I can save them for you!\nPress /help for more info."

help_msg = """Save your passwords safely here..

Here you can generate strong passwords and save them for future use.

**You can generate password by two ways in here:**
1| Generating password by random characters
2| Generating password by your specific characters

**Commands:** 
- /randpwd **<**<code>len</code>**> <**<code>info</code>**>**: For generating password by random characters.
- /specpwd **<**<code>char</code>**> <**<code>len</code>**> <**<code>info</code>**>**: For generating password by your specific characters.
- /search **<**<code>info</code>**>**: This command will search for specific passwords with info provided.
- /mypwds: To get all saved passwords.

👆here in commands..
**<**<code>len</code>**>** means length of password required.
and..
**<**<code>info</code>**>** means for what you are generating password. This will be helpful to you for future use.
**<**<code>char</code>**>** means characters you want to use in your password.

Thank you!
"""

pwd_msg = """**Your password is generated successfully!**

**Here is your password:**
<code>{0}</code>

**Password info:**
<code>{1}</code>

Your password is saved successfully😊!
"""
