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

        # connect some slots that were not connected in the .ui fli
        # self.checkLogStream.stateChanged.connect(self.handleLogStateChanged)

        self.made_socket = False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.grabData)
        self.timer.start()
        self.loadSettings()

        self.file_pointer = None

    def loadSettings(self):
        self.settings.beginGroup('zmqsubscriber')
        self.lineEditIP.setText(self.settings.value('ipaddr').toString())
        self.lineEditPort.setText(self.settings.value('port').toString())
        self.lineEditTopic.setText(self.settings.value('topic').toString())
        self.lineEditPeriod.setText(self.settings.value('period').toString())
        self.lineEditLogFile.setText(self.settings.value('path_to_log_file').toString())
        self.settings.endGroup()

    def saveSettings(self):
        self.settings.beginGroup('zmqsubscriber')
        self.settings.setValue('ipaddr', self.lineEditIP.text())
        self.settings.setValue('port', self.lineEditPort.text())
        self.settings.setValue('topic', self.lineEditTopic.text())
        self.settings.setValue('period', self.lineEditPeriod.text())
        self.settings.setValue('path_to_log_file', self.lineEditLogFile.text())
        self.settings.endGroup()

        if self.file_pointer is not None:
            self.file_pointer.close()

    def handleUpdateClicked(self):
        self.timer.setInterval(int(self.lineEditPeriod.text()))
        self.makeConnection()

    def handleChangeLogFile(self):
        """Called when the user clicks the Change Log File button."""
        path_to_log_file = self.lineEditLogFile.text()
        new_path_to_log_file = str(QtGui.QFileDialog.getSaveFileName(self,
                                   "Select log file", path_to_log_file))

        if new_path_to_log_file != '':
            self.lineEditLogFile.setText(new_path_to_log_file)

    def handleLogStateChanged(self):
        state = self.checkLogStream.checkState()
        if state == 2:
            try:
                self.file_pointer = open(str(self.lineEditLogFile.text()), 'a')
            except:
                QtGui.QMessageBox.critical(self, 'Error opening log file')
                self.file_pointer = None
        elif state == 0:
            if self.file_pointer is not None:
                self.file_pointer.close()
                self.file_pointer = None

        print(state)

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
            try:
                string = self.socket.recv(flags=zmq.NOBLOCK)
            except zmq.ZMQError:
                return

            print(string)
            topic, date, time, messagedata = string.split(' ')
            self.lineEditDisp.setText(messagedata)

            if self.file_pointer is not None:
                # write the data
                self.file_pointer.write('%s\t%s\t%s\t\n' %
                                        (date, time, messagedata))

