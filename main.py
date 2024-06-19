from kivy.app import App
from kivy.uix.button import Button


class DemoApp(App):
    def build(self):
        b = Button()
        return b

if __name__ == '__main__':
    DemoApp().run()
