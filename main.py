from kivymd.app import MDApp

from controller import DesignController
from model import DesignModel


class Compass(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = DesignModel()
        self.controller = DesignController(self.model)

    def build(self):
        return self.controller.get_screen()


Compass().run()
