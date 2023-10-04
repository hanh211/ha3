from kivy.app import App
from kivy.uix.label import Label
class MyApp(App):
    def build(self):
        self.icon="images/appicon.png"
        self.title="chao"
        return Label(text="chao")

if __name__ == '__main__':
    app=MyApp()
    app.run()
