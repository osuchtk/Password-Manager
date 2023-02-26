from login import Login
from kivy.app import App


class MyApp(App):
    def build(self):
        self.title = "Password Manager"
        return Login()


MyApp().run()
