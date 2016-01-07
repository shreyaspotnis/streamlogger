from PyQt4 import QtGui, QtCore, uic
from datetime import datetime
import os
import zmq

zmq_context = zmq.Context()

main_package_dir = os.path.join(os.path.dirname(__file__), os.pardir)
ui_filename = os.path.join(main_package_dir, "ui/ZMQSubscriber.ui")
Ui_ZMQSubscriber, QWidget = uic.loadUiType(ui_filename)


class ZMQSubscriber(QWidget, Ui_ZMQSubscriber):
    """The only window of the application."""

    def __init__(self, settings, parent=None):
        super(ZMQSubscriber, self).__init__(parent)
        self.settings = settings

        self.setupUi(self)
        self.made_socket = False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.grabData)
        self.timer.start()
        self.loadSettings()

    def loadSettings(self):
        self.settings.beginGroup('zmqsubscriber')
        self.lineEditIP.setText(self.settings.value('ipaddr').toString())
        self.lineEditPort.setText(self.settings.value('port').toString())
        self.lineEditTopic.setText(self.settings.value('topic').toString())
        self.lineEditPeriod.setText(self.settings.value('period').toString())
        self.settings.endGroup()

    def saveSettings(self):
        self.settings.beginGroup('zmqsubscriber')
        self.settings.setValue('ipaddr', self.lineEditIP.text())
        self.settings.setValue('port', self.lineEditPort.text())
        self.settings.setValue('topic', self.lineEditTopic.text())
        self.settings.setValue('period', self.lineEditPeriod.text())
        self.settings.endGroup()

    def handleUpdateClicked(self):
        self.timer.setInterval(int(self.lineEditPeriod.text()))
        self.makeConnection()

    def makeConnection(self):
        ip_addr = str(self.lineEditIP.text())
        port = str(self.lineEditPort.text())
        topic = str(self.lineEditTopic.text())

        if self.made_socket:
            self.socket.close()
        else:
            self.made_socket = True

        # Socket to talk to server
        self.socket = zmq_context.socket(zmq.SUB)

        connect_string = "tcp://%s:%s" % (ip_addr, port)
        self.lineEditFinalForm.setText(connect_string)
        self.socket.connect(connect_string)
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)

    def grabData(self):
        if self.made_socket:
            string = self.socket.recv()
            topic, messagedata = string.split()
            print('test')
            self.lineEditDisp.setText(messagedata)

