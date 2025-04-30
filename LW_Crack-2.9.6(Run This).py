import sys
import types
import importlib.util
import os
from PyQt5.QtWidgets import QApplication

# Create fake gsheets_auth module
fake_gs = types.ModuleType("gsheets_auth")
fake_gs.sheet = types.SimpleNamespace(get_all_records=lambda: [])
sys.modules["gsheets_auth"] = fake_gs

# Get the directory where the executable is located
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_dir = sys._MEIPASS
else:
    # Running as a normal Python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the decompiled lynchware code
decompiled_path = os.path.join(base_dir, "LW_src.py")
spec = importlib.util.spec_from_file_location("lynchware", decompiled_path)
lynchware = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lynchware)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if hasattr(lynchware, "STYLESHEET"):
        app.setStyleSheet(lynchware.STYLESHEET)
    # show the platform‑choice window first
    window = lynchware.GamePlatformChoiceWindow()
    sys.exit(app.exec_())