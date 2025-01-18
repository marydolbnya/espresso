import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog

class addCoffeeForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/addEditCoffeeForm.ui', self)
        self.conn = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.conn.cursor()
        self.setWindowTitle('Добавление новой позиции')
        self.pushButton.clicked.connect(self.save)
        for item in  self.cur.execute('SELECT id, name FROM coffee_types').fetchall():
            self.comboBox.addItem(item[1], item[0])

    def save(self):
        self.cur.execute(f'INSERT INTO catalog (variety_name, '
                    f'roasting_degree, '
                    f'type_id, '
                    f'taste_description, '
                    f'price, '
                    f'package_size) '
                    f'VALUES ("{self.lineEdit.text()}", '
                    f'{self.spinBox.value()}, '
                    f'{self.comboBox.currentData()}, '
                    f'"{self.lineEdit_3.text()}", '
                    f'{self.lineEdit_4.text()}, '
                    f'{self.lineEdit_5.text()})')
        self.conn.commit()
        self.conn.close()
        self.close()


class editCoffeeForm(QDialog):
    def __init__(self, record):
        super().__init__()
        uic.loadUi('UI/addEditCoffeeForm.ui', self)
        self.conn = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.conn.cursor()
        self.id = record.value('catalog.id')

        self.setWindowTitle('Изменение')
        self.pushButton.clicked.connect(self.save)
        self.lineEdit.setText(str(record.value('Сорт')))
        if record.value('Обжарка'):
            self.spinBox.setValue(int(record.value('Обжарка')))
        sel = -1
        for i, item in  enumerate(self.cur.execute('SELECT id, name FROM coffee_types').fetchall()):
            self.comboBox.addItem(item[1], item[0])
            if item[1] == record.value('Вид'):
                sel = i
        if sel != -1:
            self.comboBox.setCurrentIndex(sel)

        self.lineEdit_3.setText(str(record.value('Описание')))
        self.lineEdit_4.setText(str(record.value('Цена')))
        self.lineEdit_5.setText(str(record.value('Вес упаковки')))

    def save(self):
        self.cur.execute(f'UPDATE catalog SET '
                         f'variety_name = "{self.lineEdit.text()}", '
                         f'roasting_degree = {self.spinBox.value()}, '
                         f'type_id = {self.comboBox.currentData()}, '
                         f'taste_description = "{self.lineEdit_3.text()}", '
                         f'price = {self.lineEdit_4.text()}, '
                         f'package_size = {self.lineEdit_5.text()} '
                         f'WHERE id = {self.id}')
        self.conn.commit()
        self.conn.close()
        self.close()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/main.ui', self)

        self.query = ('SELECT catalog.id, '
                      'catalog.variety_name AS "Сорт", '
                      'catalog.roasting_degree AS "Обжарка", '
                      'coffee_types.name AS "Вид", '
                      'catalog.taste_description AS "Описание", '
                      'catalog.price AS "Цена", '
                      'catalog.package_size AS "Вес упаковки" '
                      'FROM catalog LEFT JOIN coffee_types ON catalog.type_id = coffee_types.id')

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data/coffee.sqlite')
        self.db.open()

        self.model = QSqlTableModel(self, self.db)
        self.model.setQuery(self.query)
        self.model.select()

        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setColumnWidth(1, 300)
        self.tableView.setColumnWidth(2, 60)
        self.tableView.setColumnWidth(4, 300)

        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)

    def add(self):
        addCoffeeForm().exec()
        self.model.setQuery(self.query)

    def edit(self):
        selected = self.tableView.selectionModel().selectedIndexes()
        if selected:
            editCoffeeForm(self.model.record(selected[0].row())).exec()
            self.model.setQuery(self.query)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyWindow()
    wnd.show()
    sys.exit(app.exec())
