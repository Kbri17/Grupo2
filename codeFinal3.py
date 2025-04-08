import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QRadioButton, QCheckBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox, QSpinBox, QListWidget, QComboBox, QCalendarWidget)
from PyQt5.QtCore import Qt, QDate
from PyQt5.uic import loadUi


class SistemaCalificacionesAsistencia(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("sistema_calificaciones.ui", self)
        self.setWindowTitle("Sistema de Calificaciones y Asistencias")

        self.add_button.clicked.connect(self.add_student)
        self.save_button.clicked.connect(self.save_report)
        self.delete_button.clicked.connect(self.delete_student)
        self.filter_button.clicked.connect(self.apply_filters)
        

        self.combo_attendance.addItems(["Presente", "Ausente", "Tarde"])
        self.filter_attendance.addItems(
            ["Todos", "Presente", "Ausente", "Tarde"])
        self.filter_min_grade.setMaximum(20)

        self.tblGrades.setColumnCount(5)
        self.tblGrades.setHorizontalHeaderLabels(
            ["Estudiante", "Calificación", "Asistencia", "Fecha", "Comentario"]
        )
        self.tblGrades.setEditTriggers(self.tblGrades.DoubleClicked)
        
        
        

    def add_student(self):
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Advertencia", "Ingrese un nombre.")
            return

        for row in range(self.tblGrades.rowCount()):
            if self.tblGrades.item(row, 0) and self.tblGrades.item(row, 0).text() == name:
                QMessageBox.warning(self, "Advertencia",
                                    "El estudiante ya está registrado.")
                return

        grade = str(self.spin_grade.value())
        attendance = self.combo_attendance.currentText()
        date = self.calendar.selectedDate().toString("dd/MM/yyyy")
        comment = self.comentario.toPlainText()

        self.list_students.addItem(name)

        row = self.tblGrades.rowCount()
        self.tblGrades.insertRow(row)
        self.tblGrades.setItem(row, 0, QTableWidgetItem(name))
        self.tblGrades.setItem(row, 1, QTableWidgetItem(grade))
        self.tblGrades.setItem(row, 2, QTableWidgetItem(attendance))
        self.tblGrades.setItem(row, 3, QTableWidgetItem(date))
        self.tblGrades.setItem(row, 4, QTableWidgetItem(comment))

        self.input_name.clear()
        self.spin_grade.setValue(0)
        self.combo_attendance.setCurrentIndex(0)
        self.comentario.clear()

    def delete_student(self):
        selected_row = self.tblGrades.currentRow()
        if selected_row >= 0:
            student_name = self.tblGrades.item(selected_row, 0).text()
            self.tblGrades.removeRow(selected_row)
            items = self.list_students.findItems(student_name, Qt.MatchExactly)
            for item in items:
                self.list_students.takeItem(self.list_students.row(item))
            QMessageBox.information(
                self, "Eliminado", f"Estudiante '{student_name}' eliminado.")
        else:
            QMessageBox.warning(self, "Advertencia",
                                "Seleccione un estudiante para eliminar.")

  # funcion que me permite editar a el estudiante seleccionado : nota , nombre , asistencia y fecha
    def edit_student(self):
        selected_row = self.tblGrades.currentRow()
        if selected_row >= 0:
            student_name = self.tblGrades.item(selected_row, 0).text()
            grade = self.tblGrades.item(selected_row, 1).text()
            attendance = self.tblGrades.item(selected_row, 2).text()
            date = self.tblGrades.item(selected_row, 3).text()

            self.input_name.setText(student_name)
            self.spin_grade.setValue(int(grade))
            index = self.combo_attendance.findText(attendance)
            if index != -1:
                self.combo_attendance.setCurrentIndex(index)
            date_parts = date.split("/")
            if len(date_parts) == 3:
                day, month, year = map(int, date_parts)
                self.calendar.setSelectedDate(QDate(year, month, day))
 

    def save_report(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Guardar Reporte", "", "CSV Files (*.csv)"
        )
        if file_name:
            try:
                with open(file_name, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        ["Estudiante", "Calificación", "Asistencia", "Fecha"])
                    for row in range(self.tblGrades.rowCount()):
                        student = self.tblGrades.item(row, 0).text(
                        ) if self.tblGrades.item(row, 0) else ""
                        grade = self.tblGrades.item(row, 1).text(
                        ) if self.tblGrades.item(row, 1) else ""
                        attendance = self.tblGrades.item(
                            row, 2).text() if self.tblGrades.item(row, 2) else ""
                        date = self.tblGrades.item(row, 3).text(
                        ) if self.tblGrades.item(row, 3) else ""
                        writer.writerow([student, grade, attendance, date])
                QMessageBox.information(
                    self, "Guardado", "El reporte se guardó correctamente.")
            except (IOError, OSError) as e:
                QMessageBox.critical(
                    self, "Error", f"No se pudo guardar el archivo: {e}")

    def apply_filters(self):
        min_grade = self.filter_min_grade.value()
        attendance_filter = self.filter_attendance.currentText()

        for row in range(self.tblGrades.rowCount()):
            show_row = True
            grade = int(self.tblGrades.item(row, 1).text())
            attendance = self.tblGrades.item(row, 2).text()

            if grade < min_grade:
                show_row = False
            if attendance_filter != "Todos" and attendance != attendance_filter:
                show_row = False

            self.tblGrades.setRowHidden(row, not show_row)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("estilo.qss", "r") as file:
            style = file.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Archivo de estilo no encontrado.")

    window = SistemaCalificacionesAsistencia()
    window.show()
    sys.exit(app.exec_())

