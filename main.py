import sqlite3
import sys

from qtpy.QtCore import Qt  # Importando Qt para usar as cores
from qtpy.QtGui import QColor, QPalette
from qtpy.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class EisenhowerMatrixApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()
        self.loadTasks()

    def initUI(self):
        self.setWindowTitle('Matriz de Eisenhower')
        self.setGeometry(100, 100, 800, 600)

        # Aplicar o modo escuro
        self.setDarkMode()

        # Layout principal
        mainLayout = QGridLayout()

        # Quadrantes
        self.createQuadrant(mainLayout, '1º Quadrante', 'Faça agora', QColor(230, 230, 250), QColor(220, 20, 60), 0, 0)
        self.createQuadrant(mainLayout, '2º Quadrante', 'Agende', QColor(255, 165, 0), QColor(220, 20, 60), 0, 1)
        self.createQuadrant(mainLayout, '3º Quadrante', 'Delegue', QColor(230, 230, 250), QColor(25, 25, 112), 1, 0)
        self.createQuadrant(mainLayout, '4º Quadrante', 'Elimine', QColor(255, 165, 0), QColor(25, 25, 112), 1, 1)

        self.setLayout(mainLayout)

    def setDarkMode(self):
        darkPalette = QPalette()
        darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.WindowText, Qt.white)
        darkPalette.setColor(QPalette.Base, QColor(25, 25, 25))
        darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        darkPalette.setColor(QPalette.Text, Qt.white)
        darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ButtonText, Qt.white)
        darkPalette.setColor(QPalette.BrightText, Qt.red)
        darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.HighlightedText, Qt.black)
        darkPalette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        QApplication.setPalette(darkPalette)

        self.setStyleSheet("""
            QWidget {
                background-color: #353535;
                color: white;
            }
            QLineEdit {
                background-color: #555555;
                color: white;
            }
            QTextEdit {
                background-color: #555555;
                color: white;
            }
            QListWidget {
                background-color: #555555;
                color: white;
            }
            QPushButton {
                background-color: #444444;
                color: white;
            }
        """)

    def initDB(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                quadrant TEXT
            )
        ''')
        self.conn.commit()

    def loadTasks(self):
        self.cursor.execute('SELECT id, description, quadrant FROM tasks')
        for task_id, description, quadrant in self.cursor.fetchall():
            self.addTaskToList(task_id, description, quadrant)

    def createQuadrant(self, layout, title, action, col_color, row_color, row, col):
        quadrantLayout = QVBoxLayout()

        # Título do quadrante
        titleLabel = QLabel(title)
        titleLabel.setStyleSheet(f"background-color: {col_color.name()}; color: black; font-weight: bold; padding: 5px;")
        quadrantLayout.addWidget(titleLabel)

        # Ação do quadrante
        actionLabel = QLabel(action)
        actionLabel.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px;")
        quadrantLayout.addWidget(actionLabel)

        # Campo de entrada de tarefa
        taskInput = QLineEdit()
        taskInput.setPlaceholderText('Nova Tarefa')
        quadrantLayout.addWidget(taskInput)

        # Botão para adicionar tarefa
        addButton = QPushButton('Adicionar Tarefa')
        addButton.clicked.connect(lambda: self.addTask(taskInput, title))
        quadrantLayout.addWidget(addButton)

        # Lista de tarefas
        taskList = QListWidget()
        quadrantLayout.addWidget(taskList)

        quadrantWidget = QWidget()
        quadrantWidget.setAutoFillBackground(True)
        p = quadrantWidget.palette()
        p.setColor(QPalette.Window, row_color)
        quadrantWidget.setPalette(p)
        quadrantWidget.setLayout(quadrantLayout)

        layout.addWidget(quadrantWidget, row, col)

        # Armazenar a lista de tarefas no objeto da janela principal
        if not hasattr(self, 'taskLists'):
            self.taskLists = {}
        self.taskLists[title] = taskList

    def addTask(self, taskInput, quadrant):
        task = taskInput.text()
        if task:
            self.cursor.execute('INSERT INTO tasks (description, quadrant) VALUES (?, ?)', (task, quadrant))
            task_id = self.cursor.lastrowid
            self.conn.commit()
            self.addTaskToList(task_id, task, quadrant)
            taskInput.clear()

    def addTaskToList(self, task_id, task, quadrant):
        taskList = self.taskLists[quadrant]
        listItem = QListWidgetItem(task)
        listItem.setData(Qt.UserRole, task_id)

        deleteButton = QPushButton('x')
        deleteButton.setFixedSize(20, 20)
        deleteButton.clicked.connect(lambda: self.removeTask(taskList, listItem))

        itemWidget = QWidget()
        itemLayout = QHBoxLayout()
        itemLayout.addWidget(QLabel(task))
        itemLayout.addWidget(deleteButton)
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemWidget.setLayout(itemLayout)

        listItem.setSizeHint(itemWidget.sizeHint())
        taskList.addItem(listItem)
        taskList.setItemWidget(listItem, itemWidget)

    def removeTask(self, taskList, listItem):
        task_id = listItem.data(Qt.UserRole)
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        taskList.takeItem(taskList.row(listItem))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EisenhowerMatrixApp()
    ex.show()
    sys.exit(app.exec_())
