# End-To-End Example: Password Program

Password Program:

- 5 attempts for the password
- On correct password, print: “Access Granted”, then end the program 
- On incorrect password “Invalid Password Attempt #” and give the user another try
- After 5 attempts, print “You are locked out”. Then end the program.



```python
secret = "rhubarb"
attempts = 0
while True:
    password = input("Enter Password: ")
    attempts= attempts + 1
    if password == secret:
        print("Access Granted!")
        break 
    print("Invalid password attempt #",attempts)
    if attempts == 5:
        print("You are locked out")
        break
```

    Enter Password: sd
    Invalid password attempt # 1
    Enter Password: fds
    Invalid password attempt # 2
    Enter Password: sd
    Invalid password attempt # 3
    Enter Password: d
    Invalid password attempt # 4
    Enter Password: d
    Invalid password attempt # 5
    You are locked out



```python

```
