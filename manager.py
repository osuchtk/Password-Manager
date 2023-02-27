from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '320')
import kivy
import bcrypt
import rsa

from functools import partial
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from kivy.app import App

kivy.require('2.1.0')


from kivy.graphics import *


class MainScreen(GridLayout):
    def __init__(self, privateKey):
        super(MainScreen, self).__init__()
        # declaring elements
        self.WhereToUse = None
        self.username = None
        self.password = None
        self.addButton = None
        self.cancelButton = None
        self.description = None
        self.addNewInformation = None
        self.listPosition = None
        self.root = None
        self.privateKey = int(privateKey)

        # preparing layout for main window
        self.cols = 2
        self.padding = 5
        self.spacing = (10, 10)

        # button for addind new records
        self.addData = Button(text = "Add data",
                              size_hint = (0.2, None),
                              #width = 70,
                              height = 30,
                              background_normal = '',
                              background_color = (1, 0, 0, 1),
                              )
        self.addData.bind(on_press = self.addNewLoginCredentials)
        self.add_widget(self.addData)

        # preparing label for column with details about account
        self.addData = Label(text="Details",
                             size_hint = (0.5, None),
                             width=90,
                             height=30,
                             underline=True
                             #pos=(120, 25)
                              )
        self.add_widget(self.addData)

        self.savedAccountsLayout = GridLayout(cols = 1,
                                              spacing = (10, 10),
                                              size_hint = (0.2, None))
        self.showAccountDetailsLayout = GridLayout(cols = 2,
                                                   spacing = (10, 10),
                                                   size_hint = (0.5, None))

        self.showSavedCredentials()
        #self.add_widget(self.root)
        self.add_widget(self.savedAccountsLayout)

        informationLabel = Label(text = "Choose account to see credentials.")
        logoutButton = Button(text = "Logout",
                              size_hint = (0.3, 0.1))
        self.showAccountDetailsLayout.add_widget(informationLabel)
        #self.showAccountDetailsLayout.add_widget(logoutButton)
        self.add_widget(self.showAccountDetailsLayout)

    def addNewLoginCredentials(self, object):
        # popup where user can add new credentials
        addingLayout = GridLayout(rows=6, padding=5)
        addingLayout.spacing = (7, 7)
        self.WhereToUse = TextInput(multiline=False,
                                    hint_text="Where to use credentials",
                                    size_hint=(1, 1),
                                    pos=(200, 200),
                                    write_tab = False
                                    )

        self.username = TextInput(multiline=False,
                                  hint_text = "Username",
                                  size_hint=(1, 1),
                                  pos=(200, 200),
                                  write_tab=False
                                  )

        self.password = TextInput(multiline=False,
                                  hint_text="Password",
                                  size_hint=(1, 1),
                                  pos=(200, 200),
                                  write_tab=False
                                  )

        self.description = TextInput(multiline=True,
                                     hint_text="Description",
                                     size_hint=(1, 1),
                                     pos=(200, 200),
                                     write_tab=False
                                     )

        self.addButton = Button(text ="Save",
                                size_hint = (1, 1),
                                background_normal = '',
                                background_color = (1, 0, 0, 1),
                                pos = (120, 25))
        self.cancelButton = Button(text="Cancel",
                                   size_hint = (1, 1),
                                   background_normal='',
                                   background_color=(1, 0, 0, 1),
                                   pos=(120, 25))

        addingLayout.add_widget(self.WhereToUse)
        addingLayout.add_widget(self.username)
        addingLayout.add_widget(self.password)
        addingLayout.add_widget(self.description)
        addingLayout.add_widget(self.addButton)
        addingLayout.add_widget(self.cancelButton)

        self.addNewInformation = Popup(title="Adding new credentials",
                                       content = addingLayout,
                                       size_hint = (0.52, 1))

        self.addButton.bind(on_press = self.saveCredentials)
        self.cancelButton.bind(on_press = self.addNewInformation.dismiss)

        self.addNewInformation.open()

    def saveCredentials(self, object):
        # checking credentials and saving them to file
        if len(self.WhereToUse.text) != 0 and self.WhereToUse.text != " " and\
                len(self.username.text) != 0 and self.username != " " and\
                len(self.password.text) != 0 and self.password != " ":

            if len(self.description.text) == 0:
                self.description.text = "empty"

            #salt = bcrypt.gensalt()
            publicKey = 9487202569294169024209368019582571446386911515841866684148478612688885730862837815231856165838895818036386568793814145524941975906103735292825168830459061
            password = rsa.encrypt(self.password.text.encode(), publicKey)

            file = open("./credentials.txt", "ab")
            file.write(bytes("\n", 'ASCII'))
            file.write(bytes(self.WhereToUse.text, 'ASCII'))
            file.write(bytes("\n", 'ASCII'))
            file.write(bytes(self.username.text, 'ASCII'))
            file.write(bytes("\n", 'ASCII'))
            file.write(bytes(password))
            file.write(bytes("\n", 'ASCII'))
            file.write(bytes(self.description.text, 'ASCII'))
            file.close()

            # closing popup and refreshing list with accounts
            self.addNewInformation.dismiss()
            self.savedAccountsLayout.clear_widgets()
            self.showSavedCredentials()
        # if credentials are not good show another popup
        else:
            newCredentialsLayoutError = GridLayout(rows = 4)
            info = Label(text = "Descripton must not be empty.\n"
                                "Username must not be empty.\n"
                                "Password must not be empty.")
            button = Button(text = "OK")

            newCredentialsLayoutError.add_widget(info)
            newCredentialsLayoutError.add_widget(button)

            information = Popup(title="Warning",
                                content=newCredentialsLayoutError)
            information.open()
            button.bind(on_press = information.dismiss)

    def showSavedCredentials(self):
        # reading data from file
        file = open("./credentials.txt", "rb")
        fileContent = file.read().split(b'\n')
        file.close()

        # making list from all lines of file
        credentialsList = fileContent[3:]

        # iterating through data and selecting WhereToUse property to use it as button text
        for index, element in enumerate(fileContent[3:]):
            if index % 4 == 0:
                #self.WhereToUse = str(credentialsList[0 + index]).split("'")[1]
                self.username = str(credentialsList[1 + index]).split("'")[1]
                self.password = str(credentialsList[2 + index]).split("'")[1]
                self.description = str(credentialsList[3 + index]).split("'")[1]
                title = str(element).split("'")[1]
                self.listPosition = Button(text=title,
                                           size_hint=(0.2, None),
                                           #width = 70,
                                           height=30,
                                           background_normal='',
                                           background_color=(0.96, 0.71, 0, 1)
                                           )
                self.listPosition.bind(on_press=partial(self.showAccountInformation, self.username, self.password,
                                                        self.description))
                self.savedAccountsLayout.add_widget(self.listPosition)
        # self.root = ScrollView(do_scroll_x = False,
        #                        width=70,
        #                        height=30,
        #                        bar_color = (1, 1, 1, 1),
        #                        effect_cls = 'ScrollEffect'
        #                        )
        # self.root.add_widget(self.savedAccountsLayout)

    def showAccountInformation(self, username, password, description, object):
        self.showAccountDetailsLayout.clear_widgets()
        usernameLabel = Label(text = "Username:")
        passwordLabel = Label(text="Password:")
        descriptionLabel = Label(text="Description:")
        usernameValue = TextInput(text = "{}".format(username),
                                  readonly = True,
                                  multiline = False,
                                  width = 1)
        passwordValue = TextInput(text="{}".format(password),
                                  readonly=True,
                                  multiline = False,)
        descriptionValue = TextInput(text="{}".format(description),
                                     readonly=True,
                                     multiline = True,
                                     height = 100
                                     )

        self.showAccountDetailsLayout.add_widget(usernameLabel)
        self.showAccountDetailsLayout.add_widget(usernameValue)

        self.showAccountDetailsLayout.add_widget(passwordLabel)
        self.showAccountDetailsLayout.add_widget(passwordValue)

        self.showAccountDetailsLayout.add_widget(descriptionLabel)
        self.showAccountDetailsLayout.add_widget(descriptionValue)



# private = 9487202569294169024209368019582571446386911515841866684148478612688885730862837815231856165838895818036386568793814145524941975906103735292825168830459061
# class MyApp(App):
#     def build(self):
#         self.title = "Password Manager"
#         return MainScreen(private)
#
#
# MyApp().run()
