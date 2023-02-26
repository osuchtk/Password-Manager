from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '320')

from login import Login
from kivy.app import App


class MyApp(App):
    def build(self):
        self.title = "Password Manager"
        return Login()


MyApp().run()
