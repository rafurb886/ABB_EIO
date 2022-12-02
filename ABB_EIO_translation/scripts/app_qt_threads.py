from PyQt5.QtCore import QObject, pyqtSignal, QRunnable

class ThreadConversionSignals(QObject):
    finished = pyqtSignal()
    question = pyqtSignal(str)
    error_message = pyqtSignal(str)
    set_user_new_param = pyqtSignal(str)


class ThreadConversion(QRunnable):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.signals = ThreadConversionSignals()

    def run(self):
        self.convert()

    def convert(self):
        self.main_window.view1.convert_file_in_thread()

    def pause(self):
        self.main_window.view1.converted_obj.is_paused = True

    def resume(self):
        self.main_window.view1.converted_obj.is_paused = False

    def kill(self):
        self.main_window.view1.converted_obj.is_killed = True


