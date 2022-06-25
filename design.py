import os
from kivy.core.window import Window 
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp


class Design(TabbedPanel):

    Window.size = (800, 600) 
    Window.minimum_width, Window.minimum_height = Window.size
    
    controller = ObjectProperty()
    model = ObjectProperty()

    baud = ['4800', '9600', '115200']

            
    def __init__(self, **kw):
        super().__init__(**kw)
        ths_items = [
            {
                "text": f"{i}",
                "theme_text_color": 'Custom',
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.menu_ths_callback(x),
            } for i in 'AEMSV'
        ]
        self.menu_ths = MDDropdownMenu(
            caller=self.ids.indicator_field,
            items=ths_items,
            position="center",
            width_mult=4,
        )
        baud_items = [
            {
                "text": f"{i}",
                "theme_text_color": 'Custom',
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.menu_baud_callback(x),
            } for i in self.baud
        ]
        self.menu_baud = MDDropdownMenu(
            caller=self.ids.port_baudrate,
            items=baud_items,
            position="center",
            width_mult=4,
        )

    def menu_ths_callback(self, text_item):
        self.ids.indicator_field.text = text_item
        self.menu_ths.dismiss()
        self.controller.set_ths_indicator(text_item)

    def menu_baud_callback(self, text_item):
        self.ids.port_baudrate.text = text_item
        self.menu_baud.dismiss()
        self.controller.set_port_baudrate(text_item)

    def set_hdt_course(self, active, value):
        if not active:
            self.controller.set_hdt_course(value)

    def set_hdt_t(self, focus, value):
        if not focus:
            self.controller.set_hdt_t(value)

    def set_hdg_course(self, active, value):
        if not active:
            self.controller.set_hdg_course(value)

    def set_hdg_edev(self, active, value):
        if not active:
            self.controller.set_hdg_edev(value)
    
    def set_hdg_wdev(self, active, value):
        if not active:
            self.controller.set_hdg_wdev(value)

    def set_ths_course(self, active, value):
        if not active:
            self.controller.set_ths_course(value)

    def set_hdt_checkbx(self, instance, value):
        self.controller.set_hdt_checkbx(value)

    def set_hdg_checkbx(self, instance, value):
        self.controller.set_hdg_checkbx(value)

    def set_ths_checkbx(self, instance, value):
        self.controller.set_ths_checkbx(value)
    
    def set_hdt_sum(self, instance, value):
        self.controller.set_hdt_sum(value)
    
    def set_hdg_sum(self, instance, value):
        self.controller.set_hdg_sum(value)
    
    def set_ths_sum(self, instance, value):
        self.controller.set_ths_sum(value)

    def set_port_name(self, focus, value):
        if not focus:
            self.controller.set_port_name(value)

    def start_button(self):
        self.controller.start_button()

    def close_button(self):
        self.controller.close_button()

    def set_type_tr(self, instance, value):
        if self.ids.serial.active:
            self.controller.set_type_tr(value=1)
        elif self.ids.tcp.active:
            self.controller.set_type_tr(value=2)

    def set_tcp_port(self, focus, value):
        if not focus:
            self.controller.set_tcp_port(value)

    def set_frequency(self, active, value):
        if not active:
            self.controller.set_frequency(value)

Builder.load_file(os.path.join(os.path.dirname(__file__), "design.kv"))