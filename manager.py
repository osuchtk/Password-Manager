from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '320')
import kivy
import bcrypt

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from kivy.app import App

kivy.require('2.1.0')


class MainScreen(GridLayout):
    def __init__(self):
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
        self.savedAccountsList = []
        self.printSavedCredentials()
        #self.add_widget(self.root)
        self.add_widget(self.savedAccountsLayout)
        # self.addData = Button(text="Add data 2",
        #                       size_hint = (None, None),
        #                       width=90,
        #                       height=30,
        #                       background_normal='',
        #                       background_color=(1, 0, 0, 1),
        #                       #pos=(120, 25)
        #                       )
        # self.savedAccountsLayout.add_widget(self.addData)
        #
        # self.addData = Button(text="Add data 2",
        #                       size_hint = (None, None),
        #                       width=90,
        #                       height=30,
        #                       background_normal='',
        #                       background_color=(1, 0, 0, 1),
        #                       #pos=(120, 25)
        #                       )
        # self.savedAccountsLayout.add_widget(self.addData)
        # self.add_widget(self.savedAccountsLayout)

    def addNewLoginCredentials(self, button):
        # popup where user can add new credentials
        addingLayout = GridLayout(rows=6, padding=5)
        addingLayout.spacing = (7, 7)
        self.WhereToUse = TextInput(multiline=False,
                                    hint_text="Where to use credentials",
                                    size_hint=(1, 1),
                                    pos=(200, 200),
                                    )

        self.username = TextInput(multiline=False,
                                  hint_text = "Username",
                                  size_hint=(1, 1),
                                  pos=(200, 200),
                                  )

        self.password = TextInput(multiline=False,
                                  hint_text="Password",
                                  size_hint=(1, 1),
                                  pos=(200, 200),
                                  )

        self.description = TextInput(multiline=True,
                                     hint_text="Description",
                                     size_hint=(1, 1),
                                     pos=(200, 200),
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

    def saveCredentials(self, button):
        # checking credentials and saving them to file
        if len(self.WhereToUse.text) != 0 and self.WhereToUse.text != " " and\
                len(self.username.text) != 0 and self.username != " " and\
                len(self.password.text) != 0 and self.password != " ":

            if len(self.description.text) == 0:
                self.description.text = "empty"

            salt = bcrypt.gensalt()
            password = bytes(self.password.text, 'ASCII')

            file = open("./credentials.txt", "ab")
            file.write(bytes("\n", 'ASCII'))
            file.write(bytes(self.WhereToUse.text, 'ASCII'))
            file.write(bytes("\n", 'ASCII'))
            file.write(bytes(self.username.text, 'ASCII'))
            file.write(bytes("\n", 'ASCII'))
            file.write(bcrypt.hashpw(password, salt))
            file.write(bytes("\n", 'ASCII'))
            file.write(bytes(self.description.text, 'ASCII'))
            file.close()

            # closing popup and refreshing list with accounts
            self.addNewInformation.dismiss()
            self.savedAccountsLayout.clear_widgets()
            self.printSavedCredentials()
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

    def printSavedCredentials(self):
        # reading data from file
        file = open("./credentials.txt", "rb")
        fileContent = file.read().split(b'\n')
        file.close()

        # iterating through data and selecting WhereToUse property to use it as button text
        for index, element in enumerate(fileContent[2:]):
            if index % 4 == 0:
                title = str(element).split("'")[1]
                self.listPosition = Button(text=title,
                                           size_hint=(0.2, None),
                                           #width = 70,
                                           height=30,
                                           background_normal='',
                                           background_color=(0.96, 0.71, 0, 1)
                                           )
                self.savedAccountsLayout.add_widget(self.listPosition)
        # self.root = ScrollView(do_scroll_x = False,
        #                        width=70,
        #                        height=30,
        #                        bar_color = (1, 1, 1, 1),
        #                        effect_cls = 'ScrollEffect'
        #                        )
        # self.root.add_widget(self.savedAccountsLayout)
                #print("Where to use: ", element)
            # if index % 4 == 1:
            #     print("Username: ", element)
            # if index % 4 == 2:
            #     print("Password: ", element)
            # if index % 4 == 3:
            #     print("Description: ", element)



class MyApp(App):
    def build(self):
        self.title = "Password Manager"
        return MainScreen()


MyApp().run()
