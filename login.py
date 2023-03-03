import bcrypt
import kivy
from cryptography.fernet import Fernet
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

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
                              pos_hint={'x': 0., 'y': 0.37},
                              bold=True,
                              font_size=20,
                              underline=True))
        # username label and text field
        self.usernameLabel = Label(text="Login",
                                   pos_hint={'x': -0.26, 'y': 0.15})
        self.add_widget(self.usernameLabel)
        self.username = TextInput(multiline=False,
                                  size_hint=(None, None),
                                  pos_hint={'x': 0.45, 'y': 0.62},
                                  width=200,
                                  height=30,
                                  write_tab=False)
        self.add_widget(self.username)

        # password label and text field
        self.passwordLabel = Label(text="Password",
                                   pos_hint={'x': -0.26, 'y': -0.02})
        self.add_widget(self.passwordLabel)
        self.password = TextInput(multiline=False,
                                  password=True,
                                  size_hint=(None, None),
                                  pos_hint={'x': 0.45, 'y': 0.44},
                                  width=200,
                                  height=30,
                                  write_tab=False)
        self.add_widget(self.password)

        # login button
        self.loginButton = Button(text="Login",
                                  size_hint=(0.45, 0.1),
                                  background_color=(1, 0, 0, 1),
                                  pos_hint={'x': 0.265, 'y': 0.23})
        self.add_widget(self.loginButton)
        self.loginButton.bind(on_press=self.loginFunction)

        # register button
        self.registerButton = Button(text="Don't have account?",
                                     size_hint=(0.44, 0.08),
                                     background_normal='',
                                     background_color=(1, 0, 0, 1),
                                     pos_hint={'x': 0.27, 'y': 0.09})
        self.add_widget(self.registerButton)
        self.registerButton.bind(on_press=self.register)

    # method used to log in into application
    def loginFunction(self, obj):
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
            loginErrorLayout = FloatLayout()
            label = Label(text="Wrong username or password",
                          pos_hint={'x': 0., 'y': 0.25})
            closeButton = Button(text='Close',
                                 size_hint=(0.5, 0.3),
                                 pos_hint={'x': 0.25, 'y': 0.1})

            loginErrorLayout.add_widget(label)
            loginErrorLayout.add_widget(closeButton)

            information = Popup(title="Warning",
                                content=loginErrorLayout,
                                size_hint=(0.5, 0.5))
            closeButton.bind(on_press=information.dismiss)
            information.open()

    # metohd preparing view for registration
    def register(self, obj):
        # clearing view
        self.clear_widgets()
        self.username.text = ""
        self.password.text = ""
        self.add_widget(self.usernameLabel)
        self.add_widget(self.username)
        self.add_widget(self.passwordLabel)
        self.add_widget(self.password)

        welcomingLabel = Label(text="Welcome to Password Manager",
                               pos_hint={'x': 0., 'y': 0.33})
        self.add_widget(welcomingLabel)

        createAccount = Button(text="Create account!",
                               size_hint=(0.45, 0.1),
                               pos_hint={'x': 0.265, 'y': 0.23},
                               background_color=(1, 0, 0, 1))
        self.add_widget(createAccount)

        backButton = Button(text="Cancel",
                            size_hint=(0.44, 0.08),
                            pos_hint={'x': 0.27, 'y': 0.09},
                            background_normal='',
                            background_color=(1, 0, 0, 1))
        self.add_widget(backButton)

        createAccount.bind(on_press=self.createNewAccountWarning)
        backButton.bind(on_press=self.reloadMainView)

    # show warning when creating new account
    def createNewAccountWarning(self, obj):
        # empty username or password
        if len(self.username.text) == 0 or len(self.password.text) == 0:
            informationLayout = FloatLayout()
            textLabel = Label(text="Username or password\ncan not be empty!",
                              pos_hint={'x': 0., 'y': 0.2})
            continueButton = Button(text="Continue",
                                    size_hint=(0.5, 0.3),
                                    pos_hint={'x': 0.25, 'y': 0.03})
            informationLayout.add_widget(textLabel)
            informationLayout.add_widget(continueButton)
            information = Popup(title="Warning!",
                                content=informationLayout,
                                size_hint=(0.5, 0.5))
            information.open()

            continueButton.bind(on_press=information.dismiss)

        else:
            # register information
            informationLayout = FloatLayout()
            textLabel = Label(text="You are trying to create new account.If it is your first time\nlogging into "
                                   "application click Continue, otherwise click Cancel.\nCreating new account while "
                                   "having passwords wrote up\nin the memory will erase them!",
                              pos_hint={'x': 0., 'y': 0.25})
            continueButton = Button(text="Continue",
                                    size_hint=(0.3, 0.2),
                                    pos_hint={'x': 0.55, 'y': 0.1})
            cancelButton = Button(text="Cancel",
                                  size_hint=(0.3, 0.2),
                                  pos_hint={'x': 0.15, 'y': 0.1})

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
    def createNewAccount(self, obj):
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
        informationLayout = FloatLayout()
        textLabel = Label(text="Account created!",
                          pos_hint={'x': 0., 'y': 0.2})
        continueButton = Button(text="Continue",
                                size_hint=(0.5, 0.3),
                                pos_hint={'x': 0.25, 'y': 0.1})
        informationLayout.add_widget(textLabel)
        informationLayout.add_widget(continueButton)
        information = Popup(title="Success!",
                            content=informationLayout,
                            size_hint=(0.5, 0.5))
        information.open()

        continueButton.bind(on_press=information.dismiss)
        continueButton.bind(on_press=self.reloadMainView)

    def reloadMainView(self, obj):
        self.clear_widgets()
        self.add_widget(Login())
