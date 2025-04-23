import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QListView, QLabel, QStackedWidget, QStyle, QGridLayout, QSlider, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acoustic Player Demo")

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(180)  # Make the sidebar wider
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)
        self.btn_home = QPushButton("Home")
        self.btn_home.setCheckable(True)
        self.btn_library = QPushButton("Library")
        self.btn_library.setCheckable(True)
        self.btn_settings = QPushButton("Settings")
        self.btn_settings.setCheckable(True)
        self.btn_home.setChecked(True)
        sidebar_layout.addWidget(self.btn_home)
        sidebar_layout.addWidget(self.btn_library)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()

        # Main content area as QStackedWidget
        self.stacked = QStackedWidget()
        # Home Page
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_layout.setContentsMargins(20, 20, 20, 20)
        home_layout.setSpacing(15)
        home_layout.addWidget(QLabel("Welcome to Acoustic Player!"))
        # Album grid for Home
        home_album_grid = QWidget()
        home_album_grid.setObjectName("AlbumGrid")
        grid = QGridLayout(home_album_grid)
        grid.setSpacing(20)
        for i in range(2):
            for j in range(4):
                album = QPushButton()
                album.setObjectName("AlbumBlock")
                album.setFixedSize(160, 160)
                album.setCursor(Qt.PointingHandCursor)
                album.setLayout(QVBoxLayout())
                album.layout().addStretch(1)
                label = QLabel(f"Album {i*4+j+1}")
                label.setAlignment(Qt.AlignCenter)
                album.layout().addWidget(label)
                template = QLabel("This is a template album description.")
                template.setAlignment(Qt.AlignCenter)
                template.setStyleSheet("font-size: 12px; color: #555;")
                album.layout().addWidget(template)
                grid.addWidget(album, i, j)
        home_layout.addWidget(home_album_grid)
        home_layout.addStretch()
        # Library Page
        library_page = QWidget()
        library_layout = QVBoxLayout(library_page)
        library_layout.setContentsMargins(20, 20, 20, 20)
        library_layout.setSpacing(15)
        library_layout.addWidget(QLabel("Library Page"))
        # Responsive album grid in a scroll area
        album_count = 15
        responsive_grid = ResponsiveAlbumGrid(album_count)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(responsive_grid)
        library_layout.addWidget(scroll, 1)
        library_layout.addStretch()
        # Settings Page
        settings_page = QWidget()
        settings_layout = QVBoxLayout(settings_page)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(15)
        settings_layout.addWidget(QLabel("Settings Page"))
        settings_layout.addWidget(QLineEdit("Username"))
        settings_layout.addWidget(QLineEdit("Email"))
        self.stacked.addWidget(home_page)
        self.stacked.addWidget(library_page)
        self.stacked.addWidget(settings_page)

        # Connect sidebar buttons to page switching
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        self.btn_library.clicked.connect(lambda: self.switch_page(1))
        self.btn_settings.clicked.connect(lambda: self.switch_page(2))

        # Bottom controller widget
        controller = QWidget()
        controller.setObjectName("Controller")
        controller_layout = QVBoxLayout(controller)
        controller_layout.setContentsMargins(10, 5, 10, 5)
        controller_layout.setSpacing(5)
        # Slider row
        slider_row = QHBoxLayout()
        slider_row.setContentsMargins(0, 0, 0, 0)
        slider_row.setSpacing(10)
        slider_row.addStretch(1)
        slider = QSlider(Qt.Horizontal)
        slider.setObjectName("ProgressSlider")
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(0)
        slider_row.addWidget(slider, 8)
        time_label = QLabel("00:00 / 03:45")
        time_label.setObjectName("TimeLabel")
        slider_row.addWidget(time_label, 0, Qt.AlignmentFlag.AlignHCenter)
        slider_row.addStretch(1)
        controller_layout.addLayout(slider_row)
        # Playback buttons row
        playback_row = QHBoxLayout()
        playback_row.setContentsMargins(0, 0, 0, 0)
        playback_row.setSpacing(20)
        playback_row.addStretch(1)
        btn_prev = QPushButton()
        btn_prev.setObjectName("ControllerButton")
        btn_prev.setText("")
        btn_prev.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        btn_prev.setIconSize(QSize(22, 22))
        btn_play = QPushButton()
        btn_play.setObjectName("ControllerButton")
        btn_play.setText("")
        btn_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        btn_play.setIconSize(QSize(22, 22))
        btn_pause = QPushButton()
        btn_pause.setObjectName("ControllerButton")
        btn_pause.setText("")
        btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        btn_pause.setIconSize(QSize(22, 22))
        btn_next = QPushButton()
        btn_next.setObjectName("ControllerButton")
        btn_next.setText("")
        btn_next.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        btn_next.setIconSize(QSize(22, 22))
        playback_row.addWidget(btn_prev)
        playback_row.addWidget(btn_play)
        playback_row.addWidget(btn_pause)
        playback_row.addWidget(btn_next)
        playback_row.addStretch(1)
        controller_layout.addLayout(playback_row)

        # Layout: sidebar + main content + controller
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(0)
        content_row.addWidget(sidebar)
        content_row.addWidget(self.stacked, 1)
        layout.addLayout(content_row, 1)
        layout.addWidget(controller, 0)

        self.setCentralWidget(central)
        self.resize(1100, 700)  # Make the default window bigger

    def switch_page(self, idx):
        self.stacked.setCurrentIndex(idx)
        self.btn_home.setChecked(idx == 0)
        self.btn_library.setChecked(idx == 1)
        self.btn_settings.setChecked(idx == 2)

class ResponsiveAlbumGrid(QWidget):
    def __init__(self, album_count, columns=5, parent=None):
        super().__init__(parent)
        self.album_count = album_count
        self.columns = columns
        self.grid = QGridLayout(self)
        self.grid.setSpacing(20)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.populate_albums()

    def populate_albums(self):
        # Remove old widgets
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        for idx in range(self.album_count):
            album = QPushButton()
            album.setObjectName("AlbumBlock")
            album.setFixedSize(160, 160)
            album.setCursor(Qt.PointingHandCursor)
            album.setLayout(QVBoxLayout())
            album.layout().addStretch(1)
            label = QLabel(f"Album {idx+1}")
            label.setAlignment(Qt.AlignCenter)
            album.layout().addWidget(label)
            template = QLabel("This is a template album description.")
            template.setAlignment(Qt.AlignCenter)
            template.setStyleSheet("font-size: 12px; color: #555;")
            album.layout().addWidget(template)
            row = idx // self.columns
            col = idx % self.columns
            self.grid.addWidget(album, row, col)
        self.grid.setColumnStretch(self.columns, 1)
        self.grid.setRowStretch((self.album_count-1)//self.columns+1, 1)

    def resizeEvent(self, event):
        width = self.width()
        # 160px album + 20px spacing
        columns = max(1, width // (160 + 20))
        if columns != self.columns:
            self.columns = columns
            self.populate_albums()
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    try:
        with open("style.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
    except FileNotFoundError:
        print("Warning: style.qss not found. Using default style.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())