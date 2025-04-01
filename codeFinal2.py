import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QRadioButton, QCheckBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class SistemaCalificacionesAsistencia(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("sistema_calificaciones.ui", self)  # Cargar el archivo .ui generado por QtDesigner
        self.setWindowTitle("Sistema de Calificaciones y Asistencias")

        # Conectar botones a funciones
        self.add_button.clicked.connect(self.add_student)
        self.save_button.clicked.connect(self.save_report)

    def add_student(self):
        name = self.input_name.text()
        grade = self.input_grade.text()
        attendance = "Sí" if self.checkbox_attendance.isChecked() else "No"
        if name and grade:
            row = self.tblGrades.rowCount()
            self.tblGrades.insertRow(row)
            self.tblGrades.setItem(row, 0, QTableWidgetItem(name))
            self.tblGrades.setItem(row, 1, QTableWidgetItem(grade))
            self.tblGrades.setItem(row, 2, QTableWidgetItem(attendance))
            self.input_name.clear()
            self.input_grade.clear()
            self.checkbox_attendance.setChecked(False)

    def save_report(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "CSV Files (*.csv)")
        if file_name:
            try:
                with open(file_name, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Estudiante", "Calificación", "Asistencia"])
                    for row in range(self.tblGrades.rowCount()):
                        student = self.tblGrades.item(row, 0).text() if self.tblGrades.item(row, 0) else ""
                        grade = self.tblGrades.item(row, 1).text() if self.tblGrades.item(row, 1) else ""
                        attendance = self.tblGrades.item(row, 2).text() if self.tblGrades.item(row, 2) else ""
                        writer.writerow([student, grade, attendance])
                QMessageBox.information(self, "Guardado", "El reporte se guardó correctamente.")
            except (IOError, OSError) as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")

    def load_report(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la cabecera
                for row in reader:
                    yield row  # Uso de generador para eficiencia
        except (IOError, OSError) as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {e}")

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar Reporte", "", "CSV Files (*.csv)")
        if file_name:
            self.tblGrades.setRowCount(0)
            for row_data in self.load_report(file_name):
                row = self.tblGrades.rowCount()
                self.tblGrades.insertRow(row)
                for col, data in enumerate(row_data):
                    self.tblGrades.setItem(row, col, QTableWidgetItem(data))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar la hoja de estilo (QSS)
    try:
        with open("estilo.qss", "r") as file:
            style = file.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Archivo de estilo no encontrado. Usando el estilo predeterminado.")

    window = SistemaCalificacionesAsistencia()
    window.show()
    sys.exit(app.exec_())
