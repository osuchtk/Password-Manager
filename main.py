from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '320')

import bcrypt
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

kivy.require('2.1.0')


class Login(FloatLayout):
    def __init__(self):
        super(Login, self).__init__()
        # label text
        self.add_widget(Label(text = "Password Manager",
                              size_hint = (1, 1),
                              pos = (0, 120),
                              bold = True,
                              font_size = 20,
                              underline = True))
        # username label and text field
        self.add_widget(Label(text = "Login",
                              size_hint = (1, 1),
                              pos = (-130, 50)))
        self.username = TextInput(multiline = False,
                                  size_hint = (1, 1),
                                  pos = (200, 200),
                                  size_hint_x = None,
                                  width = 200,
                                  size_hint_y = None,
                                  height = 30)
        self.add_widget(self.username)

        # password label and text field
        self.add_widget(Label(text = "Password",
                              size_hint = (1, 1),
                              pos = (-130, -10)))
        self.password = TextInput(multiline = False,
                                  password = True,
                                  size_hint =(1, 1),
                                  pos = (200, 140),
                                  size_hint_x = None,
                                  width = 200,
                                  size_hint_y = None,
                                  height = 30)
        self.add_widget(self.password)

        # login button
        self.login = Button(text = "Login",
                            size_hint_x = None,
                            width = 200,
                            size_hint_y = None,
                            height = 30,
                            background_normal = '',
                            background_color = (1, 0, 0, 1),
                            pos = (120, 75)
                            )
        self.add_widget(self.login)
        self.login.bind(on_press = self.loginFunction)

        # register button
        self.login = Button(text = "Register",
                            size_hint_x = None,
                            width = 200,
                            size_hint_y = None,
                            height = 30,
                            background_normal = '',
                            background_color = (1, 0, 0, 1),
                            pos = (120, 25)
                            )
        self.add_widget(self.login)
        self.login.bind(on_press=self.registerFunction)

    def loginFunction(self, button):
        file = open("./credentials.txt", "rb")
        usernameFile = str(file.readline()).split("'")[1].split('\\')[0]
        passwordFile = file.readline()
        passwordEntered = bytes(self.password.text, 'ASCII')

        if usernameFile == self.username.text and bcrypt.checkpw(passwordEntered, passwordFile):
            print("zalogowano")
        else:
            closeButton = Button(text='Close',
                                 size_hint_x=None,
                                 width=100,
                                 size_hint_y=None,
                                 height=30,
                                 pos = (0, 50))
            information = Popup(title = "Wrong username or password",
                                auto_dismiss=False,
                                content = closeButton,
                                size_hint_x=None,
                                width=230,
                                size_hint_y=None,
                                height=100,
                                )
            closeButton.bind(on_press = information.dismiss)
            information.open()

        #abcd
        #1234

    def registerFunction(self, button):
        salt = bcrypt.gensalt()
        password = bytes(self.password.text, 'ASCII')
        file = open("./credentials.txt", "wb")
        file.write(bytes(self.username.text, 'ASCII'))
        file.write(bytes("\n", 'ASCII'))
        file.write(bcrypt.hashpw(password, salt))
        file.close()
        print("user registered")


class MyApp(App):
    def build(self):
        self.title = "Password Manager"
        return Login()


MyApp().run()