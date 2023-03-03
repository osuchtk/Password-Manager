# Password-Manager

Simple password manager using Pyhon with Kivy framework.

## How does it work?
When user creates an account his username and password (which is hashed using [bcrypt](https://pypi.org/project/bcrypt/)) are saved to a file. During registration process user gets unique key and generator used to encode and decode all credentials stored - I use [cryptography](https://pypi.org/project/cryptography/) package to achieve it. 
Every saved credentials can be deleted or modyfied. Temporarily all saved data and master password are stored in one file, but in future I'm plannig to store all data in database.

Login window: 

![obraz](https://user-images.githubusercontent.com/56642926/222717926-4d616056-ac8a-44b5-baef-23ceaf59524e.png)


Main window:

![obraz](https://user-images.githubusercontent.com/56642926/222717971-adfaf2c8-b9ac-487c-84e4-697c2804d97f.png)
