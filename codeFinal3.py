import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QRadioButton, QCheckBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox, QSpinBox, QListWidget, QComboBox, QCalendarWidget)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class SistemaCalificacionesAsistencia(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("sistema_calificaciones.ui", self)
        self.setWindowTitle("Sistema de Calificaciones y Asistencias")

        
        self.add_button.clicked.connect(self.add_student)
        self.save_button.clicked.connect(self.save_report)

        # Configurar el ComboBox con opciones de asistencia

        self.combo_attendance.addItems(["Presente", "Ausente", "Tarde", "Justificado"])

    def add_student(self):
/*************  ✨ Windsurf Command ⭐  *************/
    """
    Adds a student to the system by retrieving input data, updating the student list 
    and grades table, and clearing the input fields.

    Retrieves the student's name, grade, attendance status, and selected date 
    from the user interface. Adds the student's name to a list widget and 
    inserts a new row into the grades table to display the student's details. 
    After adding, the input fields are reset for new entries.

    Expects:
    - The input fields for name, grade, and attendance to be filled appropriately.
    - The calendar widget to have a selected date.

    Effects:
    - Modifies the list of students and grades table in the UI.
    - Clears the input fields for new input.
    """

/*******  d51a47ef-497e-413f-8ae6-b99d27962323  *******/
        name = self.input_name.text()
        grade = str(self.spin_grade.value())
        attendance = self.combo_attendance.currentText()
        date = self.calendar.selectedDate().toString("dd/MM/yyyy")

        if name:
            # Añadir a la lista de estudiantes
        
            self.list_students.addItem(name)

            # Añadir a la tabla
            row = self.tblGrades.rowCount()
            self.tblGrades.insertRow(row)
            self.tblGrades.setItem(row, 0, QTableWidgetItem(name))
            self.tblGrades.setItem(row, 1, QTableWidgetItem(grade))
            self.tblGrades.setItem(row, 2, QTableWidgetItem(attendance))
            self.tblGrades.setItem(row, 3, QTableWidgetItem(date))

            # Limpiar los campos
            self.input_name.clear()
            self.spin_grade.setValue(0)
            self.combo_attendance.setCurrentIndex(0)

    def save_report(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "CSV Files (*.csv)")
        if file_name:
            try:
                with open(file_name, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Estudiante", "Calificación", "Asistencia", "Fecha"])
                    for row in range(self.tblGrades.rowCount()):
                        student = self.tblGrades.item(row, 0).text() if self.tblGrades.item(row, 0) else ""
                        grade = self.tblGrades.item(row, 1).text() if self.tblGrades.item(row, 1) else ""
                        attendance = self.tblGrades.item(row, 2).text() if self.tblGrades.item(row, 2) else ""
                        date = self.tblGrades.item(row, 3).text() if self.tblGrades.item(row, 3) else ""
                        writer.writerow([student, grade, attendance, date])
                QMessageBox.information(self, "Guardado", "El reporte se guardó correctamente.")
            except (IOError, OSError) as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        with open("estilo.qss", "r") as file:
            style = file.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Archivo de estilo no encontrado. Usando el estilo predeterminado.")

    window = SistemaCalificacionesAsistencia()
    window.show()
    sys.exit(app.exec_())
