import shutil
import subprocess
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PhoneControllerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cripos Phone Manager v1.0")
        self.setGeometry(300, 150, 450, 350)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #b4befe; }
            QLabel { color: #cdd6f4; font-size: 16px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.title_label = QLabel("Android USB Controller")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        self.status_label = QLabel("Holat: Telefon ulanishi kutilmoqda...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.btn_check = QPushButton("1. Telefonni tekshirish")
        self.btn_check.clicked.connect(self.check_device)
        layout.addWidget(self.btn_check)

        self.btn_start = QPushButton("2. Ekranni boshqarishni boshlash")
        self.btn_start.clicked.connect(self.start_mirroring)
        layout.addWidget(self.btn_start)

        btn_layout = QHBoxLayout()

        self.btn_power = QPushButton("Yoqish/O'chirish")
        self.btn_power.clicked.connect(lambda: self.send_adb_command("shell input keyevent 26"))
        btn_layout.addWidget(self.btn_power)

        self.btn_volume_up = QPushButton("Ovoz +")
        self.btn_volume_up.clicked.connect(lambda: self.send_adb_command("shell input keyevent 24"))
        btn_layout.addWidget(self.btn_volume_up)

        self.btn_volume_down = QPushButton("Ovoz -")
        self.btn_volume_down.clicked.connect(lambda: self.send_adb_command("shell input keyevent 25"))
        btn_layout.addWidget(self.btn_volume_down)

        layout.addLayout(btn_layout)

    def _adb_available(self):
        return shutil.which("adb") is not None

    def _scrcpy_available(self):
        return shutil.which("scrcpy") is not None

    def _run_adb(self, args, capture_output=True):
        if not self._adb_available():
            raise FileNotFoundError("ADB o'rnatilmagan! 'adb' PATH ichida topilmadi.")
        return subprocess.run(
            ["adb", *args],
            capture_output=capture_output,
            text=True,
            check=False,
        )

    def check_device(self):
        try:
            result = self._run_adb(["devices"])
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or "ADB buyruq bajarilmadi.")

            lines = result.stdout.strip().splitlines()
            devices = [
                line for line in lines[1:]
                if "device" in line.lower() and "offline" not in line.lower()
            ]

            if devices:
                self.status_label.setText("Holat: Telefon ulangan! ✅")
                self.status_label.setStyleSheet("color: #a6e3a1;")
            else:
                self.status_label.setText("Holat: Telefon topilmadi! ❌")
                self.status_label.setStyleSheet("color: #f38ba8;")
        except FileNotFoundError:
            QMessageBox.critical(self, "Xatolik", "ADB o'rnatilmagan! Ilovadan foydalanish uchun adb ni o'rnating.")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"ADB xatosi: {e}")

    def start_mirroring(self):
        if not self._scrcpy_available():
            QMessageBox.critical(self, "Xatolik", "scrcpy o'rnatilmagan! O'rnating va PATHga qo'shing.")
            return

        try:
            subprocess.Popen(["scrcpy", "--max-fps=60", "--window-title=Mening Telefonim"])
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"scrcpy ishga tushmadi: {e}")

    def send_adb_command(self, cmd):
        try:
            self._run_adb(cmd.split(), capture_output=False)
        except FileNotFoundError:
            QMessageBox.critical(self, "Xatolik", "ADB o'rnatilmagan! Ilovadan foydalanish uchun adb ni o'rnating.")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Buyruq xatosi: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhoneControllerApp()
    window.show()
    sys.exit(app.exec())
