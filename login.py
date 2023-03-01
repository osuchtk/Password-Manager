import bcrypt
import kivy
from cryptography.fernet import Fernet
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

from manager import MainScreen

kivy.require('2.1.0')


# abcd
# 1234


class Login(FloatLayout):
    # constructor preparing view showed when application is launched
    def __init__(self):
        super(Login, self).__init__()
        # declaring elements
        self.fernetGenerator = None
        self.key = None

        # label text
        self.add_widget(Label(text="Password Manager",
                              size_hint=(1, 1),
                              pos=(0, 120),
                              bold=True,
                              font_size=20,
                              underline=True))
        # username label and text field
        self.add_widget(Label(text="Login",
                              size_hint=(1, 1),
                              pos=(-130, 50)))
        self.username = TextInput(multiline=False,
                                  size_hint=(None, None),
                                  pos=(200, 200),
                                  width=200,
                                  height=30,
                                  write_tab=False)
        self.add_widget(self.username)

        # password label and text field
        self.add_widget(Label(text="Password",
                              size_hint=(1, 1),
                              pos=(-130, -10)))
        self.password = TextInput(multiline=False,
                                  password=True,
                                  size_hint=(None, None),
                                  pos=(200, 140),
                                  width=200,
                                  height=30,
                                  write_tab=False)
        self.add_widget(self.password)

        # login button
        self.login = Button(text="Login",
                            size_hint=(None, None),
                            width=200,
                            height=30,
                            background_color=(1, 0, 0, 1),
                            pos=(120, 75))
        self.add_widget(self.login)
        self.login.bind(on_press=self.loginFunction)

        # register button
        self.login = Button(text="Register",
                            size_hint=(None, None),
                            width=200,
                            height=30,
                            background_normal='',
                            background_color=(1, 0, 0, 1),
                            pos=(120, 25))
        self.add_widget(self.login)
        self.login.bind(on_press=self.register)

    # method used to log in into application
    def loginFunction(self, object):
        # reading credentials from file
        file = open("./credentials.txt", "rb")
        usernameFile = str(file.readline()).split("'")[1].split('\\')[0]
        passwordFile = file.readline().split(b'\n')[0]
        passwordEntered = bytes(self.password.text, 'ASCII')
        self.fernetGenerator = file.readline()
        self.key = file.readline()
        file.close()

        # checking if credentials used to log in are correct
        if (usernameFile == self.username.text and bcrypt.checkpw(passwordEntered, passwordFile)) and \
                len(self.password.text) > 0 and len(self.username.text) > 0:
            self.clear_widgets()
            self.add_widget(MainScreen(self.fernetGenerator, self.key))
        else:
            closeButton = Button(text='Close',
                                 size_hint=(None, None),
                                 width=100,
                                 height=30,
                                 pos=(0, 50))
            information = Popup(title="Wrong username or password",
                                auto_dismiss=False,
                                content=closeButton,
                                size_hint=(None, None),
                                width=230,
                                height=100)
            closeButton.bind(on_press=information.dismiss)
            information.open()

    # metohd preparing view for registration
    def register(self, object):
        # empty username or password
        if len(self.username.text) == 0 or len(self.password.text) == 0:
            informationLayout = GridLayout(rows=3, padding=5)
            textLabel = Label(text="Username or password can not be empty!")
            continueButton = Button(text="Continue")
            informationLayout.add_widget(textLabel)
            informationLayout.add_widget(continueButton)
            information = Popup(title="Warning!",
                                content=informationLayout)
            information.open()

            continueButton.bind(on_press=information.dismiss)

        else:
            # register information
            informationLayout = GridLayout(rows=4, padding=5)
            textLabel = Label(text="You are trying to create new account.If it is your first time\nlogging into "
                                   "application click Continue, otherwise click Cancel.\nCreating new account while "
                                   "having passwords wrote up\nin the memory will erase them!",
                              size_hint=(1, 1),
                              pos=(500, 120))
            continueButton = Button(text="Continue")
            cancelButton = Button(text="Cancel")

            informationLayout.add_widget(textLabel)
            informationLayout.add_widget(continueButton)
            informationLayout.add_widget(cancelButton)

            information = Popup(title="Warning!",
                                content=informationLayout)
            information.open()

            cancelButton.bind(on_press=information.dismiss)
            continueButton.bind(on_press=information.dismiss)
            continueButton.bind(on_press=self.createNewAccount)

    # method saving new account into file
    def createNewAccount(self, object):
        # writing credentials to file
        # but first some password hashing and preparing encoding
        salt = bcrypt.gensalt()
        self.fernetGenerator = Fernet.generate_key()
        self.key = Fernet(self.fernetGenerator)
        password = bytes(self.password.text, 'ASCII')
        file = open("./credentials.txt", "wb")
        file.write(bytes(self.username.text, 'ASCII'))
        file.write(bytes("\n", 'ASCII'))
        file.write(bcrypt.hashpw(password, salt))
        file.write(bytes("\n", 'ASCII'))
        file.write(bytes(self.fernetGenerator))
        file.write(bytes("\n", 'ASCII'))
        file.write(bytes(self.key.encryption_key))
        file.close()

        # showing popup when account created
        informationLayout = GridLayout(rows=3, padding=5)
        textLabel = Label(text="Account created!")
        continueButton = Button(text="Continue")
        informationLayout.add_widget(textLabel)
        informationLayout.add_widget(continueButton)
        information = Popup(title="Success!",
                            content=informationLayout)
        information.open()

        continueButton.bind(on_press=information.dismiss)
