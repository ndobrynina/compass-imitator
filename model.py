import threading
from time import sleep
from serial import Serial
import socket
import socketserver


class DesignModel:

    def __init__(self):
        self._started = False
        self._hdt_course = 0.0
        self._hdt_t = 'T'
        self._hdg_course = 0.0
        self._hdg_edev = 0.0
        self._hdg_wdev = 0.0
        self._ths_course = 0.0
        self._ths_indicator = 'A'
        self._hdt_sentence = '$HEHDT,' + str(round(self._hdt_course, 2)) + ',' + str(self._hdt_t) + '*'
        self._hdg_sentence = '$NDHDG,' + str(round(self._hdg_course, 2)) + ',' + str(
            round(self._hdg_edev, 2)) + ',E,' + str(round(self._hdg_wdev, 2)) + ',W*'
        self._ths_sentence = '$HETHS,' + str(round(self._ths_course, 2)) + ',' + str(self._ths_indicator) + '*'
        self._hdt_checksum = False
        self._hdg_checksum = False
        self._ths_checksum = False
        self._hdt_checkbx = True
        self._hdg_checkbx = True
        self._ths_checkbx = True
        self._port = '/dev/ttyUSB0'
        self._baudrate = 9600
        self._type_tr = False
        self._transmitter = None
        self._tcp_port = '34444'
        self._mvar = ''
        self._mdev = ''
        self._frequency = 1


    @property
    def port(self):
        return self._port

    @property
    def baudrate(self):
        return self._baudrate

    @property
    def hdt_course(self):
        return self._hdt_course

    @property
    def hdt_t(self):
        return self._hdt_t

    @property
    def hdg_course(self):
        return self._hdg_course

    @property
    def hdg_edev(self):
        return self._hdg_edev

    @property
    def hdg_wdev(self):
        return self._hdg_wdev

    @property
    def ths_course(self):
        return self._ths_course

    @property
    def ths_indicator(self):
        return self._ths_indicator

    @property
    def hdt_sentence(self):
        return self._hdt_sentence

    @property
    def hdg_sentence(self):
        return self._hdg_sentence

    @property
    def ths_sentence(self):
        return self._ths_sentence

    @property
    def hdt_sum(self):
        return self._hdt_checksum

    @property
    def hdg_sum(self):
        return self._hdg_checksum

    @property
    def ths_sum(self):
        return self._ths_checksum

    @property
    def hdt_checkbx(self):
        return self._hdt_checkbx

    @property
    def hdg_checkbx(self):
        return self._hdg_checkbx

    @property
    def ths_checkbx(self):
        return self._ths_checkbx

    @property
    def type_tr(self):
        return self._type_tr

    @property
    def tcp_port(self):
        return self._tcp_port

    @property
    def frequency(self):
        return self._frequency

    @port.setter
    def port(self, value):
        self._port = value

    @baudrate.setter
    def baudrate(self, value):
        self._baudrate = value

    @tcp_port.setter
    def tcp_port(self, value):
        self._tcp_port = value

    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    @hdt_course.setter
    def hdt_course(self, value):
        self._hdt_course = value
        self._hdt_sentence = '$HEHDT,' + str(round(self._hdt_course, 2)) + ',' + str(self._hdt_t) + '*'

    @hdt_t.setter
    def hdt_t(self, value):
        self._hdt_t = value
        self._hdt_sentence = '$HEHDT,' + str(round(self._hdt_course, 2)) + ',' + str(self._hdt_t) + '*'

    @hdg_course.setter
    def hdg_course(self, value):
        self._hdg_course = value
        self._hdg_sentence = '$NDHDG,' + str(round(self._hdg_course, 2)) + ',' + str(
            abs(round(self._hdg_edev, 2))) + ',' + self._mdev + ',' + str(
            abs(round(self._hdg_wdev, 2))) + ',' + self._mvar + '*'

    @hdg_edev.setter
    def hdg_edev(self, value):
        self._hdg_edev = value
        if -360 < int(
                self._hdg_edev) < 0:  # ???????? ?????????????????????????? ????????????????, ???? ?????????????????? ???????? ?????????? W, ???????? ?????????????????????????? - ??
            self._mdev = 'W'
            self._hdg_sentence = '$NDHDG,' + str(round(self._hdg_course, 2)) + ',' + str(
                abs(round(self._hdg_edev, 2))) + ',' + self._mdev + ',' + str(
                abs(round(self._hdg_wdev, 2))) + ',' + self._mvar + '*'
        if 0 <= int(self._hdg_edev) < 360:
            self._mdev = 'E'
            self._hdg_sentence = '$NDHDG,' + str(round(self._hdg_course, 2)) + ',' + str(
                abs(round(self._hdg_edev, 2))) + ',' + self._mdev + ',' + str(
                abs(round(self._hdg_wdev, 2))) + ',' + self._mvar + '*'

    @hdg_wdev.setter
    def hdg_wdev(self, value):
        self._hdg_wdev = value
        if -360 < int(self._hdg_wdev) < 0:
            self._mvar = 'W'
            self._hdg_sentence = '$NDHDG,' + str(round(self._hdg_course, 2)) + ',' + str(
                abs(round(self._hdg_edev, 2))) + ',' + self._mdev + ',' + str(
                abs(round(self._hdg_wdev, 2))) + ',' + self._mvar + '*'
        if 0 <= int(self._hdg_wdev) < 360:
            self._mvar = 'E'
            self._hdg_sentence = '$NDHDG,' + str(round(self._hdg_course, 2)) + ',' + str(
                abs(round(self._hdg_edev, 2))) + ',' + self._mdev + ',' + str(
                abs(round(self._hdg_wdev, 2))) + ',' + self._mvar + '*'

    @ths_course.setter
    def ths_course(self, value):
        self._ths_course = value
        self._ths_sentence = '$HETHS,' + str(round(self._ths_course, 2)) + ',' + str(self._ths_indicator) + '*'

    @ths_indicator.setter
    def ths_indicator(self, value):
        self._ths_indicator = value
        self._ths_sentence = '$HETHS,' + str(round(self._ths_course, 2)) + ',' + str(
            self._ths_indicator) + '*'

    @hdt_sum.setter
    def hdt_sum(self, value):
        self._hdt_checksum = value

    @hdg_sum.setter
    def hdg_sum(self, value):
        self._hdg_checksum = value

    @ths_sum.setter
    def ths_sum(self, value):
        self._ths_checksum = value

    @hdt_checkbx.setter
    def hdt_checkbx(self, value):
        self._hdt_checkbx = value

    @hdg_checkbx.setter
    def hdg_checkbx(self, value):
        self._hdg_checkbx = value

    @ths_checkbx.setter
    def ths_checkbx(self, value):
        self._ths_checkbx = value

    @type_tr.setter
    def type_tr(self, value):
        self._type_tr = value

    def get_ths(self):
        xor = 0
        if self._ths_checksum:
            s = self._ths_sentence[1:-1]
            for char in s:
                xor ^= ord(char)  # ?????????????????? ?????????????? ?????????????? ?? ???????????? ?????? ?????????????? ?? ???????????????????? ??????????????
            s_xor = format(xor, '#04x')  # ?????????????? ?? 16-???????????? ?????????????? ?? ???????????????????????? ????????????????
            ths_sent = str.encode(self._ths_sentence + s_xor[2:].upper() + '\r\n')
        if not self._ths_checksum:
            ths_sent = str.encode(self._ths_sentence + 'HH\r\n')
        return ths_sent

    def get_hdg(self):
        xor = 0
        if self._hdg_checksum:
            s = self._hdg_sentence[1:-1]
            for char in s:
                xor ^= ord(char)
            s_xor = format(xor, '#04x')
            hdg_sent = str.encode(self._hdg_sentence + s_xor[2:].upper() + '\r\n')
        if not self._hdg_checksum:
            hdg_sent = str.encode(self._hdg_sentence + 'HH\r\n')
        return hdg_sent

    def get_hdt(self):
        xor = 0
        if self._hdt_checksum:
            s = self._hdt_sentence[1:-1]
            for char in s:
                xor ^= ord(char)
            s_xor = format(xor, '#04x')
            hdt_sent = str.encode(self._hdt_sentence + s_xor[2:].upper() + '\r\n')
        if not self._hdt_checksum:
            hdt_sent = str.encode(self._hdt_sentence + 'HH\r\n')
        return hdt_sent

    def get_data(self):
        data_list = []
        s1 = self.get_ths()
        s2 = self.get_hdt()
        s3 = self.get_hdg()
        if self._ths_checkbx:
            data_list.append(s1)
        if self._hdt_checkbx:
            data_list.append(s2)
        if self._hdg_checkbx:
            data_list.append(s3)
        return data_list

    def start_button(self):
        if self._started:  # ???????????????? ?????????????????????? ????????????
            return
        if self._type_tr == 1:  # ???????????????? ????????????????????????
            self._transmitter = SerialTransmitter(self._port,
                                                  self._baudrate)  # ???????????????? ???????????????????? ???????????? SerialTransmitter
            print('switch')
        else:
            self._transmitter = TCP(self, int(self._tcp_port)) # ???????????????? ???????????????? ???????????????????? ???????????? DesignModel ?????? ???????????????????????? ?????????????????? ??????????????????
            print('ready')
        self._started = True  # ???????? ?????? ?????????????? ????????????
        work_thread = threading.Thread(target=self.work)  # ???????????????? ????????????
        work_thread.daemon = True
        work_thread.start()

    def work(self):
        if self._type_tr != 1:
            while self._started:
                s = self.get_data()
                print(s)
                self._transmitter.connect()
                self._transmitter.handle()
        else:
            while self._started:
                for data in self.get_data():
                    self._transmitter.transmit(data)
                    sleep(1 / self._frequency)

    def close_button(self):
        self._started = False
        self._transmitter.sclose()

class SerialTransmitter:

    def __init__(self, port, baud):
        self._serial_port = Serial(port=port, baudrate=baud)

    def sclose(self):
        self._serial_port.close()

    def transmit(self, sent):
        self._serial_port.write(sent)

# Windows
def get_ip():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return ip_addr

#Linux
# def get_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     s.connect(('<broadcast>', 0))
#     return s.getsockname()[0]

class MyHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            print(f'{get_ip()} sending to {self.client_address} {self.server.update()} with {self.server.get_freq()}')
            for d in self.server.update():
                self.request.send(d)
            sleep(1 / self.server.get_freq())
        except BrokenPipeError:
            self.server.shutdown_request(self.request)


class TCP(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, dm, port):
        self._host = get_ip()
        self._port = port
        self._obj = dm
        self._data = None
        self._tcp_start = False
        self._frequency = None
        super().__init__((self._host, self._port), MyHandler)  # ?????????????? ?????????? ?????????????????????????? ???? ?????????????????????????? ????????????

    def connect(self):
        self.serve_forever()
        self._tcp_start = True

    def get_freq(self):
        self._frequency = self._obj.frequency
        return self._frequency

    def update(self):
        self._data = self._obj.get_data()
        return self._data

    def sclose(self):
        self.server_close()
        self._tcp_start = False
