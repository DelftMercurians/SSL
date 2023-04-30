import sys
import threading

import PyQt6.QtWidgets
import requests
from Gamelog import Gamelog, get_frames
from log_player import LogPlayer
from PyQt6.QtCore import Qt


def get_all_logs():
    url = "http://100.119.147.55:8080/api/logfiles/search"
    headers = {"Content-Type": "text/plain"}
    body = ".log"
    try:
        response = requests.request("GET", url, headers=headers, data=body)
    except requests.exceptions.RequestException:
        print("having trouble connecting to the database")
        sys.exit(1)
    return response.json()


class DraggableProgressBar(PyQt6.QtWidgets.QSlider):
    def __init__(self, game_log: Gamelog, speed: float):
        super().__init__()
        self.setOrientation(Qt.Orientation.Horizontal)
        self.player = LogPlayer(game_log.headers, game_log.data, speed)
        self.is_paused = True
        self.bind = threading.Thread(target=self.updateV)
        self.bind.start()

    def start(self):
        st_index = (self.value() - self.minimum()) * len(self.player.header) / self.width()
        self.stop_event = threading.Event()
        self.play = threading.Thread(target=self.player.play, args=(self.stop_event, int(st_index)))
        self.play.start()
        self.is_paused = False

    def pause(self):
        if self.play.is_alive():
            self.stop_event.set()
        self.is_paused = True

    def switch_status(self):
        if self.is_paused:
            self.start()
        else:
            self.pause()

    def updateV(
        self,
    ):
        while True:
            if not self.is_paused:
                self.set_value_according_to_position(float(self.player.pointer) / len(self.player.header))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.is_paused:
                self.pause()
            value = self.minimum() + (self.maximum() - self.minimum()) * event.position().x() / self.width()
            self.setValue(int(value))
            self.start()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not self.is_paused:
            self.pause()
        value = self.minimum() + (self.maximum() - self.minimum()) * event.position().x() / self.width()
        self.setValue(int(value))
        self.start()

    def set_value_according_to_position(self, position: float):
        value = self.minimum() + (self.maximum() - self.minimum()) * position
        # print(value)
        self.setValue(int(value))


class LogSearchApp(PyQt6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Sample log data
        self.logs = get_all_logs()
        self.log_selected = ""
        self.game_log = None
        # Set up the user interface
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Log system")
        self.main_layout = PyQt6.QtWidgets.QVBoxLayout()

        self.log_retrieval = PyQt6.QtWidgets.QHBoxLayout()
        self.search_layout = PyQt6.QtWidgets.QVBoxLayout()
        self.search_layout.addWidget(PyQt6.QtWidgets.QLabel("Log Retrival:"))
        self.search_bar = PyQt6.QtWidgets.QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for a log file")
        self.search_bar.textChanged.connect(self.update_dropdown)
        self.search_layout.addWidget(self.search_bar)
        self.search_results = PyQt6.QtWidgets.QComboBox(self)
        self.search_layout.addWidget(self.search_results)
        self.selection_label = PyQt6.QtWidgets.QLabel("Please select the log", self)
        self.search_layout.addWidget(self.selection_label)
        self.search_results.currentIndexChanged.connect(self.display_selected_log)
        self.log_retrieval.addLayout(self.search_layout)
        fetch_button = PyQt6.QtWidgets.QPushButton("Fetch", self)
        fetch_button.clicked.connect(self.fetch_log)
        self.log_retrieval.addWidget(fetch_button)
        self.main_layout.addLayout(self.log_retrieval)

        h_line = PyQt6.QtWidgets.QFrame()
        h_line.setFrameShape(PyQt6.QtWidgets.QFrame.Shape.HLine)
        h_line.setFrameShadow(PyQt6.QtWidgets.QFrame.Shadow.Sunken)
        self.main_layout.addWidget(h_line)

        self.log_display = PyQt6.QtWidgets.QVBoxLayout()
        self.log_display.addWidget(PyQt6.QtWidgets.QLabel("Log player:"))
        self.draggable_progress_bar = PyQt6.QtWidgets.QProgressBar(self)
        self.log_display.addWidget(self.draggable_progress_bar)
        # check box for choose the speed

        self.speed = PyQt6.QtWidgets.QComboBox(self)
        self.speed.addItems(["1.0x", "0.2x", "0.4x", "0.6x", "0.8x"])
        self.log_display.addWidget(self.speed)
        self.speed.currentIndexChanged.connect(self.change_speed)

        self.main_layout.addLayout(self.log_display)

        self.setLayout(self.main_layout)

    def change_speed(self):
        speed = self.speed.currentText()
        if not isinstance(self.draggable_progress_bar, DraggableProgressBar):
            return
        if speed == "0.2x":
            self.draggable_progress_bar.player.speed_factor = 0.2
        elif speed == "0.4x":
            self.draggable_progress_bar.player.speed_factor = 0.4
        elif speed == "0.6x":
            self.draggable_progress_bar.player.speed_factor = 0.6
        elif speed == "0.8x":
            self.draggable_progress_bar.player.speed_factor = 0.8
        else:
            self.draggable_progress_bar.player.speed_factor = 1.0

    def fetch_log(self):
        url = "http://100.119.147.55:8080/api/logfiles/"
        headers = {"Content-Type": "text/plain"}
        body = self.log_selected
        if not body:
            return
        try:
            response = requests.request("GET", url, headers=headers, data=body)

        except requests.exceptions.RequestException:
            print("having trouble connecting to the database")
            sys.exit(1)
        d, h = get_frames(response.content)
        self.game_log = Gamelog(d, h)
        self.draggable_progress_bar = DraggableProgressBar(
            self.game_log, float(self.speed.currentText()[:-1])
        )
        self.log_display.itemAt(1).widget().deleteLater()
        print()
        self.log_display.insertWidget(1, self.draggable_progress_bar)
        self.log_display.update()
        self.main_layout.update()
        directory = PyQt6.QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Directory", "")
        if directory:
            if self.game_log and self.log_selected:
                self.game_log.to_binary(directory + "/" + self.log_selected)

        return

    def update_dropdown(self):
        query = self.search_bar.text()
        max_allowed = 20
        res = [item for item in self.logs if query in item]
        if len(res) >= max_allowed:
            res = res[:max_allowed]

        self.search_results.clear()
        self.search_results.addItems(res)

    def display_selected_log(self, index):
        selected_log = self.search_results.itemText(index)
        self.selection_label.setText(f"Selected log: {selected_log}")
        self.log_selected = selected_log


if __name__ == "__main__":
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    log_search_app = LogSearchApp()
    log_search_app.show()
    sys.exit(app.exec())
