from PyQt5.QtCore import QObject, pyqtSignal, QRunnable
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from errors import ConverterError

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
        print('Thread conversion')
        print(f'THREAD TASK: Source path:{self.main_window.view1.source_file}')
        self.convert()

    def convert(self):
        print(f'THREAD TASK: Source path:{self.main_window.view1.source_file}')
        print(f'THREAD TASK: Conversion to:{self.main_window.view1.conversion_to}')
        try:
            if self.main_window.view1.conversion_to == 'cfg':
                self.obj = SignalsConverterToCfg.from_excel(self.main_window.view1.source_file)
            elif self.main_window.view1.conversion_to == 'xlsx':
                self.obj = SignalsConverterToExcel.from_cfg(self.main_window.view1.source_file)
            self.obj.signals = self.signals
            print('THREAD TASK: Obj created')
            # emit signal to attach signals to obj
            # self.main_window.attach_views_to_model() w argumencie obj?
            self.obj.convert(self.main_window.view1.destination_file)
            print('CONVERSION DONE !!')
        except ConverterError as e:
            self.obj.signals.error_message.emit(e)


        self.inform_user_conversion_finished()
        #self.init_app_after_conversion()

    def inform_user_conversion_finished(self):
        self.obj.signals.finished.emit()

    def set_new_param(self, new_param):
        self.obj.user_new_param = new_param
        self.obj.is_paused = False

    def pause(self):
        self.obj.is_paused = True

    def resume(self):
        self.obj.is_paused = False

    def kill(self):
        self.obj.is_killed = True


