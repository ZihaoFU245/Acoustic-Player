from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
import sys
import importlib
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ObjectDisplayWindow(QMainWindow):
    def __init__(self, obj, obj_name="Imported Object"):
        super().__init__()
        self.setWindowTitle(f"Object Viewer: {obj_name}")
        self.resize(600, 400)
        central = QWidget()
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel(f"<b>Name:</b> {obj_name}"))
        layout.addWidget(QLabel(f"<b>Type:</b> {type(obj)}"))
        # Add the widget if it's a QWidget
        layout.addWidget(QLabel("<b>Widgets:</b>"))
        if isinstance(obj, QWidget):
            layout.addWidget(obj)
        else:
            layout.addWidget(QLabel(f"<b>Object is not a QWidget:</b> {obj}"))
        layout.addWidget(QLabel(f"<b>String Representation:</b>"))
        str_edit = QTextEdit(str(obj))
        str_edit.setReadOnly(True)
        layout.addWidget(str_edit)

        layout.addWidget(QLabel("<b>Attributes:</b>"))
        attr_edit = QTextEdit("\n".join(f"{k}: {v}" for k, v in vars(obj).items()) if hasattr(obj, '__dict__') else "No __dict__ available.")
        attr_edit.setReadOnly(True)
        layout.addWidget(attr_edit)

        self.setCentralWidget(central)

def import_and_show_object(module_name, object_name):
    module = importlib.import_module(module_name)
    obj = getattr(module, object_name)
    app = QApplication(sys.argv)
    # If obj is a class and is a QWidget subclass, instantiate it with required args
    if isinstance(obj, type) and issubclass(obj, QWidget):
        # MiniTest requires a 'text' argument
        if object_name == "MiniTest":
            obj_instance = obj("Test Button")
        else:
            obj_instance = obj()
    else:
        obj_instance = obj
    win = ObjectDisplayWindow(obj_instance, object_name)
    win.show()
    app.exec()

if __name__ == "__main__":
    """used for testing purposes"""
    import_and_show_object("app.mini_test", "MiniTest")
