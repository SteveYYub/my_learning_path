from PySide6 import QtWidgets, QtCore, QtGui
import time

# second submission

# Multithreading example using QThreadPool to ignore blocking GUI operations
class WorkerSignals(QtCore.QObject):

    finished = QtCore.Signal()
    error = QtCore.Signal(str)
    result = QtCore.Signal(str)
    progress = QtCore.Signal(int, object)


class Worker(QtCore.QRunnable):
    """
        work thread
    """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @QtCore.Slot()
    def run(self):  # run the command in a separate thread
        try:
            res = self.fn(*self.args, **self.kwargs)
        except:
            e = sys.exc_info()[1]
            self.signals.error.emit(str(e))
        else:
            self.signals.result.emit(res)
        finally:
            self.signals.finished.emit()


# customized class
class FileQLineEdit(QtWidgets.QLineEdit):
    def __init__(self, place_holder_text, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(f"Enter file path of {place_holder_text}")
        '''
        self.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        '''
    # re-write mouseDoubleClick behavior
    def mouseDoubleClickEvent(self, arg__1: QtGui.QMouseEvent) -> None:
        if arg__1.button() == QtCore.Qt.LeftButton:
            # open file dialog
            file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
            if file_path:
                self.setText(file_path[0])
        return super().mouseDoubleClickEvent(arg__1)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Window")
        self.setGeometry(100,100,700, 900)
        self.threadPool = QtCore.QThreadPool()

    # Define main panel;
        _main_panel = QtWidgets.QSplitter(QtCore.Qt.Vertical, self)
        _central_layout = QtWidgets.QVBoxLayout()
        self.setLayout(_central_layout)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        _central_layout.addWidget(_main_panel)
        _main_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    
    # add first box:
        self.sg = self.grid_box("ShotGrid")
        self.sg_icon = QtWidgets.QPushButton()
        self.sg_icon.setIcon(QtGui.QIcon("icon/icon.jpg"))
        self.sg_icon.setFixedSize(50, 50)
        self.sg_icon.setIconSize(QtCore.QSize(45,45))
        # self.sg_icon.clicked.connect(self.on_sg_clicked)

        _sg_items = ["apr", "intapr", "rfc", "latest"]
        self.sg_items = QtWidgets.QComboBox()
        self.sg_items.addItems(_sg_items)

        self.sg.layout().addWidget(self.sg_icon, 0, 0, 2, 2)
        self.sg.layout().addWidget(self.sg_items, 1, 1, 1, 1)
        self.sg.layout().addWidget(QtWidgets.QFrame(), 0, 2, 2, 4, QtCore.Qt.AlignRight)

        _main_panel.addWidget(self.sg)

        # add second box:
        row = 0
        self.func = self.grid_box("Func")
        _main_panel.addWidget(self.func)
        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("select output path")
        self.func.layout().addWidget(QtWidgets.QLabel("Output Folder"), row, 0, 1, 1, QtCore.Qt.AlignRight)
        self.func.layout().addWidget(self.output_path, row, 1, 1, 4)
        self.output_path_dialg = QtWidgets.QPushButton("Open")
        self.output_path_dialg.clicked.connect(self.browse_folder)
        self.func.layout().addWidget(self.output_path_dialg, row, 5, 1, 1)
        self.output_path.textChanged.connect(lambda x : self.log_info(x + ' is opened'))

        row +=1
        self.file_path = FileQLineEdit("MyFile")
        self.func.layout().addWidget(QtWidgets.QLabel("File"), row, 0, 1, 1, QtCore.Qt.AlignRight)
        self.func.layout().addWidget(self.file_path, row, 1, 1, 5)
        self.file_path.textChanged.connect(lambda x: self.log_window.setText(x + ' is seleceted '))
 
        row +=1
        self.thread_test = QtWidgets.QPushButton("Dev")
        self.thread_test_progress = QtWidgets.QProgressBar()
        self.func.layout().addWidget(self.thread_test, row, 0, 1, 3)
        self.func.layout().addWidget(self.thread_test_progress, row, 3, 1, 3)
        self.thread_test.clicked.connect(self.worker)
        

        row = 0 
        # add console
        self.console = self.grid_box("Console")
        self.log_window = QtWidgets.QTextEdit()
        self.log_window.setReadOnly(True)
        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.clear_btn.clicked.connect(lambda: self.log_window.clear())
        self.console.layout().addWidget(self.log_window, row, 0, 1, 6)

        row +=1 
        self.console.layout().addWidget(self.clear_btn, row, 0, 1, 6)
        _main_panel.addWidget(self.console)


    def grid_box(self, box_name, parent = None):
        # Define customized box widget; return a widget
        _widget = QtWidgets.QGroupBox(box_name, parent)
        _widget.setStyleSheet("QGroupBox { background-color: #f0f0f0; }")

        _font   = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
        _widget.setFont(_font)
        _layout = QtWidgets.QGridLayout(_widget)
        _widget.setLayout(_layout)

        return _widget
    def browse_folder(self):
        # Open a file dialog to select a folder
        dialg = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Folder", "", QtWidgets.QFileDialog.ShowDirsOnly)
        if dialg:
            self.output_path.setText(dialg)

    def progess_fn(self, percentage, progress):
        # Update the progress bar with the given value
        progress.setValue(percentage)

    def print_output(self, s):
        self.log_info(s)

    def thread_finished(self):
        self.log_info("Thread finished")

    def error(self, s):
        print(f"Error is {s}")

    def oh_test(self, progress_bar, progress_callback):
        # create a long time task simulation

        total = 10

        for i in range(10):
            time.sleep(1)
            percentage = (i+1) / total * 100
            progress_callback.emit(percentage, progress_bar)

        return "WORKER DONE!!!"
    
    def worker(self):

        worker = Worker(self.oh_test, self.thread_test_progress)
        worker.signals.finished.connect(self.thread_finished)
        worker.signals.error.connect(self.error)
        worker.signals.progress.connect(self.progess_fn)
        worker.signals.result.connect(self.print_output)
        self.threadPool.start(worker)

    def log_info(self,msg):
        self.log_window.insertHtml('<style>p {font-family: Arial, sans-serif; font-size: 14px;}</style><p>' + msg + '<br></p>')
        self.log_window.moveCursor(QtGui.QTextCursor.End)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())