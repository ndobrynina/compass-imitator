from design import Design


class DesignController:


    def __init__(self, model):

        self.model = model
        self.view = Design(controller=self, model=self.model)

    def get_screen(self):

        return self.view

    def set_hdt_course(self, value):
        self.model.hdt_course = value

    def set_hdt_t(self, value):
        self.model.hdt_t = value

    def set_hdg_course(self, value):
        self.model.hdg_course = value

    def set_hdg_edev(self, value):
        self.model.hdg_edev = value

    def set_hdg_wdev(self, value):
        self.model.hdg_wdev = value
    
    def set_ths_course(self, value):
        self.model.ths_course = value

    def set_ths_indicator(self, value):
        self.model.ths_indicator = value

    def set_hdt_checkbx(self, value):
        self.model.hdt_checkbx = value

    def set_hdg_checkbx(self, value):
        self.model.hdg_checkbx = value

    def set_ths_checkbx(self, value):
        self.model.ths_checkbx = value

    def set_port_name(self, value):
        self.model.port = value

    def set_port_baudrate(self, value):
        self.model.baudrate = value

    def set_tcp_port(self, value):
        self.model.tcp_port = value

    def set_frequency(self, value):
        self.model.frequency = value

    def set_hdt_sum(self, value):
        self.model.hdt_sum = value
    
    def set_hdg_sum(self, value):
        self.model.hdg_sum = value

    def set_ths_sum(self, value):
        self.model.ths_sum = value

    def start_button(self):
        self.model.start_button()
    
    def close_button(self):
        self.model.close_button()

    def set_type_tr(self, value):
        self.model.type_tr = value
