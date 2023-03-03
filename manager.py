from cryptography.fernet import Fernet
from functools import partial
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class MainScreen(GridLayout):
    # constructor in which main layouts are prepared
    def __init__(self, fernetGenerator, key):
        super(MainScreen, self).__init__()
        # declaring elements
        self.WhereToUse = None
        self.username = None
        self.usernameEdited = None
        self.password = None
        self.passwordEdited = None
        self.addButton = None
        self.cancelButton = None
        self.saveEditedButton = None
        self.description = None
        self.descriptionEdited = None
        self.addNewInformation = None
        self.listPosition = None
        self.fernetGenerator = fernetGenerator
        self.privateKey = key

        # preparing layout for main window
        self.cols = 2
        self.padding = 5
        self.spacing = (10, 10)

        # button for addind new records
        self.addData = Button(text="Add data",
                              size_hint=(0.2, None),
                              height=30,
                              background_normal='',
                              background_color=(1, 0, 0, 1))
        self.addData.bind(on_press=self.addNewLoginCredentials)
        self.add_widget(self.addData)

        # preparing label for column with details about account
        self.addData = Label(text="Details",
                             size_hint=(0.5, None),
                             width=90,
                             height=30,
                             underline=True,
                             font_size=17)
        self.add_widget(self.addData)

        # preparing layout for accounts list
        self.savedAccountsLayout = GridLayout(cols=1,
                                              spacing=(10, 10),
                                              size_hint=(0.2, None))
        self.savedAccountsLayout.bind(minimum_height=self.savedAccountsLayout.setter('height'))

        # preparing layout for account details
        self.showAccountDetailsLayout = FloatLayout(size_hint=(0.5, 1))
        self.showSavedCredentials()

        # add scroll bar to accounts list
        self.scroll = ScrollView(do_scroll_y=True,
                                 do_scroll_x=False,
                                 size_hint=(0.22, 1),
                                 bar_color=(1, 1, 1, 1))
        self.scroll.add_widget(self.savedAccountsLayout)
        self.add_widget(self.scroll)

        # friendly information to choose one account from the list
        informationLabel = Label(text="Choose account to see credentials.",
                                 size_hint=(0.5, 0.5),
                                 pos_hint={'x': 0.28, 'y': 0.6})
        self.logoutButton = Button(text="Logout",
                                   size_hint=(0.3, 0.1),
                                   pos_hint={'x': 0.35, 'y': 0.05},
                                   background_normal='',
                                   background_color=(0.36, 0.34, 0.42, 1))
        self.logoutButton.bind(on_press=self.logout)
        self.showAccountDetailsLayout.add_widget(informationLabel)
        self.showAccountDetailsLayout.add_widget(self.logoutButton)
        self.add_widget(self.showAccountDetailsLayout)

    # method where view for adding new data is prepared
    def addNewLoginCredentials(self, object):
        # popup where user can add new credentials
        # preparing layout
        addingLayout = GridLayout(rows=6, padding=5)
        addingLayout.spacing = (7, 7)

        # where credential is used
        self.WhereToUse = TextInput(multiline=False,
                                    hint_text="Where to use credentials",
                                    write_tab=False)

        # text input for username
        self.username = TextInput(multiline=False,
                                  hint_text="Username",
                                  write_tab=False)

        # text input for password
        self.password = TextInput(multiline=False,
                                  hint_text="Password",
                                  password=True,
                                  write_tab=False)

        # text input for additional description
        self.description = TextInput(multiline=True,
                                     hint_text="Description",
                                     write_tab=False)

        # button for saving information
        self.addButton = Button(text="Save",
                                background_normal='',
                                background_color=(1, 0, 0, 1))

        # button to reject changes
        self.cancelButton = Button(text="Cancel",
                                   size_hint=(1, 1),
                                   background_normal='',
                                   background_color=(1, 0, 0, 1),
                                   pos=(120, 25))

        # adding widgets
        addingLayout.add_widget(self.WhereToUse)
        addingLayout.add_widget(self.username)
        addingLayout.add_widget(self.password)
        addingLayout.add_widget(self.description)
        addingLayout.add_widget(self.addButton)
        addingLayout.add_widget(self.cancelButton)

        # popup when data is succesfully added
        self.addNewInformation = Popup(title="Adding new credentials",
                                       content=addingLayout,
                                       size_hint=(0.52, 1))

        self.addButton.bind(on_press=self.saveCredentials)
        self.cancelButton.bind(on_press=self.addNewInformation.dismiss)

        self.addNewInformation.open()

    # methow where new data are saved into a file
    def saveCredentials(self, object):
        # checking credentials and saving them to file
        if len(self.WhereToUse.text) != 0 and self.WhereToUse.text != " " and \
                len(self.username.text) != 0 and self.username != " " and \
                len(self.password.text) != 0 and self.password != " ":

            # when description was empty
            if len(self.description.text) == 0:
                self.description.text = "empty"

            # encoding password
            password = Fernet(self.fernetGenerator)
            password = password.encrypt(self.password.text.encode())

            # saving data to a file
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
            newCredentialsLayoutError = FloatLayout()
            info = Label(text="Description can not be empty.\n"
                              "Username can not be empty.\n"
                              "Password can not be empty.",
                         pos_hint={'x': 0., 'y': 0.20})
            button = Button(text="OK",
                            size_hint=(0.3, 0.2),
                            pos_hint={'x': 0.35, 'y': 0.1}
                            )

            newCredentialsLayoutError.add_widget(info)
            newCredentialsLayoutError.add_widget(button)

            # show popup with warning about data
            information = Popup(title="Warning",
                                content=newCredentialsLayoutError,
                                size_hint=(0.6, 0.6))
            information.open()
            button.bind(on_press=information.dismiss)

    # method showing saved data
    def showSavedCredentials(self):
        # reading data from file
        file = open("./credentials.txt", "rb")
        fileContent = file.read().split(b'\n')
        file.close()

        # making list from all lines of file
        credentialsList = fileContent[4:]

        # iterating through data and selecting WhereToUse property to use it as button text
        for index, element in enumerate(fileContent[4:]):
            if index % 4 == 0:
                # getting items from list to use them in detailed view
                self.WhereToUse = str(credentialsList[0 + index]).split("'")[1]
                self.username = str(credentialsList[1 + index]).split("'")[1]
                self.password = str(credentialsList[2 + index]).split("'")[1]

                # decoding password
                decryptedPassword = Fernet(self.fernetGenerator)
                decryptedPassword = decryptedPassword.decrypt(bytes(self.password, 'ASCII')).decode()

                # when description was left empty
                if str(credentialsList[3 + index]).split("'")[1] == "empty":
                    self.description = ""
                else:
                    self.description = str(credentialsList[3 + index]).split("'")[1]
                title = str(element).split("'")[1]

                # adding buttons with title
                self.listPosition = Button(text=title,
                                           size_hint=(None, None),
                                           width=125,
                                           height=30,
                                           background_normal='',
                                           background_color=(0.86, 0.62, 0, 1))

                # adding username, password and description to details
                self.listPosition.bind(on_press=partial(self.showAccountInformation, self.username, decryptedPassword,
                                                        self.description, index))
                self.savedAccountsLayout.add_widget(self.listPosition)

    # method preparing view to show when button with account is clicked
    def showAccountInformation(self, username, password, description, whereUsedIndex, object):
        # clearing view from any widgets
        self.showAccountDetailsLayout.clear_widgets()

        # preparing labels for username, password and description
        usernameLabel = Label(text="Username:",
                              size_hint=(0.5, None),
                              pos_hint={'x': 0, 'y': 0.7})
        passwordLabel = Label(text="Password:",
                              size_hint=(0.5, None),
                              pos_hint={'x': 0, 'y': 0.5})
        descriptionLabel = Label(text="Description:",
                                 size_hint=(0.5, None),
                                 pos_hint={'x': 0, 'y': 0.3})

        # preparing text inputs to display data
        usernameValue = TextInput(text="{}".format(username),
                                  readonly=True,
                                  multiline=False,
                                  size_hint=(0.49, 0.12),
                                  pos_hint={'x': 0.5, 'y': 0.83})
        passwordValue = TextInput(text="{}".format(password),
                                  readonly=True,
                                  multiline=False,
                                  size_hint=(0.49, 0.12),
                                  pos_hint={'x': 0.5, 'y': 0.63})
        descriptionValue = TextInput(text="{}".format(description),
                                     readonly=True,
                                     multiline=True,
                                     size_hint=(0.49, 0.2),
                                     pos_hint={'x': 0.5, 'y': 0.35})

        # adding buttons to delete and edit data
        editButton = Button(text="Edit",
                            size_hint=(0.3, 0.1),
                            pos_hint={'x': 0.15, 'y': 0.2},
                            background_normal='',
                            background_color=(0.17, 0.35, 0.76, 1))
        editButton.bind(on_press=partial(self.editCredentials, username, password, description, whereUsedIndex))
        deleteButton = Button(text = "Delete",
                              size_hint=(0.3, 0.1),
                              pos_hint={'x': 0.55, 'y': 0.2},
                              background_normal='',
                              background_color=(0.17, 0.35, 0.76, 1))
        deleteButton.bind(on_press=partial(self.deleteCredentials, whereUsedIndex))
        closeButton = Button(text="Close",
                             size_hint=(0.3, 0.1),
                             pos_hint={'x': 0.35, 'y': 0.05},
                             background_normal='',
                             background_color=(0.36, 0.34, 0.42, 1)
                             )
        closeButton.bind(on_press=self.clearDetails)

        self.showAccountDetailsLayout.add_widget(usernameLabel)
        self.showAccountDetailsLayout.add_widget(usernameValue)

        self.showAccountDetailsLayout.add_widget(passwordLabel)
        self.showAccountDetailsLayout.add_widget(passwordValue)

        self.showAccountDetailsLayout.add_widget(descriptionLabel)
        self.showAccountDetailsLayout.add_widget(descriptionValue)

        self.showAccountDetailsLayout.add_widget(editButton)
        self.showAccountDetailsLayout.add_widget(deleteButton)
        self.showAccountDetailsLayout.add_widget(closeButton)

    # clearing detailed view from any widgets and showing friendly information
    def clearDetails(self, ojb):
        # clearing main window from any widgets connected to detailed view
        self.showAccountDetailsLayout.clear_widgets()
        informationLabel = Label(text="Choose account to see credentials.",
                                 size_hint=(0.5, 0.5),
                                 pos_hint={'x': 0.28, 'y': 0.6})
        self.showAccountDetailsLayout.add_widget(informationLabel)
        self.showAccountDetailsLayout.add_widget(self.logoutButton)

    # editing saved credentials
    def editCredentials(self, username, password, description, whereUsedIndex, obj):
        # popup where user can add new credentials
        # preparing layout
        editingLayout = GridLayout(rows=5, padding=5)
        editingLayout.spacing = (7, 7)

        # text input for username
        self.usernameEdited = TextInput(multiline=False,
                                        text="{}".format(username),
                                        hint_text="Username",
                                        size_hint=(1, 1),
                                        pos=(200, 200),
                                        write_tab=False)

        # text input for password
        self.passwordEdited = TextInput(multiline=False,
                                        text="{}".format(password),
                                        hint_text="Password",
                                        size_hint=(1, 1),
                                        pos=(200, 200),
                                        write_tab=False)

        # text input for additional description
        self.descriptionEdited = TextInput(multiline=True,
                                           text="{}".format(description),
                                           hint_text="Description",
                                           size_hint=(1, 1),
                                           pos=(200, 200),
                                           write_tab=False)

        # button for saving information
        self.saveEditedButton = Button(text="Save",
                                       size_hint=(1, 1),
                                       background_normal='',
                                       background_color=(1, 0, 0, 1),
                                       pos=(120, 25))

        # button to reject changes
        self.cancelButton = Button(text="Cancel",
                                   size_hint=(1, 1),
                                   background_normal='',
                                   background_color=(0.36, 0.34, 0.42, 1),
                                   pos=(120, 25))

        # adding widgets
        editingLayout.add_widget(self.usernameEdited)
        editingLayout.add_widget(self.passwordEdited)
        editingLayout.add_widget(self.descriptionEdited)
        editingLayout.add_widget(self.saveEditedButton)
        editingLayout.add_widget(self.cancelButton)

        # popup with editable text inputs
        self.addNewInformation = Popup(title="Editing credentials",
                                       content=editingLayout,
                                       size_hint=(0.52, 1))

        self.saveEditedButton.bind(on_press=partial(self.saveEditedCredentials, whereUsedIndex))
        self.cancelButton.bind(on_press=self.addNewInformation.dismiss)

        self.addNewInformation.open()

    def saveEditedCredentials(self, whereUsedIndex, obj):
        # popup when username or password are empty
        if len(self.usernameEdited.text) == 0 or len(self.passwordEdited.text) == 0:
            rejectEditLayout = FloatLayout()
            emptyDataLabel = Label(text="Username can not be empty.\nPassword can not be empty",
                                   pos_hint={'x': 0., 'y': 0.15})
            confirmButton = Button(text="OK",
                                   size_hint=(0.3, 0.2),
                                   pos_hint={'x': 0.35, 'y': 0.1},
                                   background_normal='',
                                   background_color=(0.36, 0.34, 0.42, 1))

            rejectEditLayout.add_widget(emptyDataLabel)
            rejectEditLayout.add_widget(confirmButton)

            rejectEditPopup = Popup(title="Edit error",
                                    content=rejectEditLayout,
                                    size_hint=(0.5, 0.5),)
            confirmButton.bind(on_press=rejectEditPopup.dismiss)
            rejectEditPopup.open()
        else:
            self.addNewInformation.dismiss()
            # reading data from file
            file = open("./credentials.txt", "rb")
            fileContent = file.read().split(b'\n')
            file.close()

            # making list from all lines of file
            credentialsList = fileContent[4:]

            # writing edited data in place of old credentials
            credentialsList[whereUsedIndex + 1] = bytes(self.usernameEdited.text, 'ASCII')

            # encoding password
            passwordDecode = Fernet(self.fernetGenerator)
            passwordDecode = passwordDecode.encrypt(self.passwordEdited.text.encode())
            credentialsList[whereUsedIndex + 2] = bytes(passwordDecode)

            # decoding password
            passwordDecode = str(passwordDecode).split("'")[1]
            decryptedPassword = Fernet(self.fernetGenerator)
            decryptedPassword = decryptedPassword.decrypt(bytes(passwordDecode, 'ASCII')).decode()

            # when description was left empty
            if len(credentialsList[whereUsedIndex + 3]) == 0:
                credentialsList[whereUsedIndex + 3] = bytes("empty", 'ASCII')
            else:
                credentialsList[whereUsedIndex + 3] = bytes(self.descriptionEdited.text, 'ASCII')

            # combinig master credentials and remined saved accounts
            allCredentials = fileContent[:4] + credentialsList

            # saving to file
            file = open("./credentials.txt", "wb")
            for ix, line in enumerate(allCredentials):
                if ix < len(allCredentials) - 1:
                    file.write(line + bytes("\n", 'ASCII'))
                else:
                    file.write(line)

            file.close()

            # reloading the view
            self.savedAccountsLayout.clear_widgets()
            self.clearDetails(self)
            self.showSavedCredentials()

    # deleting saved credentials
    def deleteCredentials(self, whereUsedIndex, obj):
        # preparing warning popup
        deleteLayout = FloatLayout()
        informationLabel = Label(text="Do you want to delete\nthis saved account?",
                                 pos_hint={'x': 0., 'y': 0.25})
        confirmButton = Button(text="OK",
                               size_hint=(0.3, 0.25),
                               pos_hint={'x': 0.55, 'y': 0.1},
                               background_normal='',
                               background_color=(1, 0., 0., 1))
        cancelButton = Button(text="Cancel",
                              size_hint=(0.3, 0.25),
                              pos_hint={'x': 0.15, 'y': 0.1},
                              background_normal='',
                              background_color=(0.36, 0.34, 0.42, 1))

        deleteLayout.add_widget(informationLabel)
        deleteLayout.add_widget(confirmButton)
        deleteLayout.add_widget(cancelButton)
        information = Popup(title="Warning",
                            content=deleteLayout,
                            size_hint=(0.5, 0.5),
                            pos_hint={'x': 0.25, 'y': 0.25})
        confirmButton.bind(on_press=self.clearDetails)
        confirmButton.bind(on_press=partial(self.confirmDeleting, whereUsedIndex))
        confirmButton.bind(on_press=information.dismiss)
        cancelButton.bind(on_press=information.dismiss)
        information.open()

    # deleting from file
    def confirmDeleting(self, whereUsedIndex, obj):
        # reading data from file
        file = open("./credentials.txt", "rb")
        fileContent = file.read().split(b'\n')
        file.close()

        # making list from all lines of file
        credentialsList = fileContent[4:]

        # opening file again, but this time to delete lines
        file = open("./credentials.txt", "wb")
        for index, element in enumerate(credentialsList):
            if index == whereUsedIndex:
                del credentialsList[index:index+4]

        # combinig master credentials and remined saved accounts
        remainedCredentials = fileContent[:4] + credentialsList

        # saving to file
        for ix, line in enumerate(remainedCredentials):
            if ix < len(remainedCredentials) - 1:
                file.write(line + bytes("\n", 'ASCII'))
            else:
                file.write(line)

        file.close()
        # clearing layout and reloading it
        self.savedAccountsLayout.clear_widgets()
        self.showSavedCredentials()

    # function logging out user
    def logout(self, obj):
        self.clear_widgets()
        from login import Login
        self.add_widget(Login())
