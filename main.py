import sys
from PyQt6 import uic
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setQuery('SELECT catalog.id, '
                       'catalog.variety_name AS "Сорт", '
                       'catalog.roasting_degree AS "Обжарка", '
                       'coffee_types.name AS "Вид", '
                       'catalog.taste_description AS "Описание", '
                       'catalog.price AS "Цена", '
                       'catalog.package_size AS "Вес упаковки" '
                       'FROM catalog LEFT JOIN coffee_types ON catalog.type_id = coffee_types.id')
        model.select()

        self.tableView.setModel(model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setColumnWidth(1, 300)
        self.tableView.setColumnWidth(2, 60)
        self.tableView.setColumnWidth(4, 300)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyWindow()
    wnd.show()
    sys.exit(app.exec())
