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

    def initUI(self):
        self.setWindowTitle('Matriz de Eisenhower')
        self.setGeometry(100, 100, 800, 600)

        # Aplicar o modo escuro
        self.setDarkMode()

        # Layout principal
        mainLayout = QVBoxLayout()

        # Layout da matriz
        matrixLayout = QGridLayout()

        # Quadrantes
        self.createQuadrant(matrixLayout, 'Urgente e Importante', 0, 0)
        self.createQuadrant(matrixLayout, 'Não Urgente e Importante', 0, 1)
        self.createQuadrant(matrixLayout, 'Urgente e Não Importante', 1, 0)
        self.createQuadrant(matrixLayout, 'Não Urgente e Não Importante', 1, 1)

        mainLayout.addLayout(matrixLayout)
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

    def createQuadrant(self, layout, title, row, col):
        quadrantLayout = QVBoxLayout()
        
        # Título do quadrante
        titleLabel = QLabel(title)
        quadrantLayout.addWidget(titleLabel)

        # Campo de entrada de tarefa
        taskInput = QLineEdit()
        taskInput.setPlaceholderText('Nova Tarefa')
        quadrantLayout.addWidget(taskInput)

        # Botão para adicionar tarefa
        addButton = QPushButton('Adicionar Tarefa')
        addButton.clicked.connect(lambda: self.addTask(taskInput, taskList))
        quadrantLayout.addWidget(addButton)

        # Lista de tarefas
        taskList = QListWidget()
        quadrantLayout.addWidget(taskList)

        layout.addLayout(quadrantLayout, row, col)

    def addTask(self, taskInput, taskList):
        task = taskInput.text()
        if task:
            listItem = QListWidgetItem(task)
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

            taskInput.clear()

    def removeTask(self, taskList, listItem):
        taskList.takeItem(taskList.row(listItem))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EisenhowerMatrixApp()
    ex.show()
    sys.exit(app.exec_())
