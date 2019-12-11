#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""synchronous communication between GUI thread and working thread in PyQt5"""

import sys
from PyQt5 import QtCore, QtWidgets
from working_thread import WorkingThread


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WorkingThread Demo')
        # 定义一个进度条，代表workingthread的耗时任务进度
        self.progressBar = QtWidgets.QProgressBar()
        # 定义一个消息显示控件，用于显示workingthread消息
        # self.informationEdit = QtWidgets.QLineEdit()
        self.informationEdit = QtWidgets.QTextEdit()
        self.putTaskButton = QtWidgets.QPushButton('Task to WorkingThread')
        self.exitThreadButton = QtWidgets.QPushButton('Exit WorkingThread')

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.putTaskButton)
        buttonLayout.addWidget(self.exitThreadButton)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.informationEdit)
        layout.addWidget(self.progressBar)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.thread = WorkingThread()
        self.thread.taskStarted.connect(self.task_started_show)
        self.thread.progressSignal.connect(self.update_progress)
        self.thread.taskFinished.connect(self.result_handle)
        self.thread.threadMessage.connect(self.thread_message_show)
        self.thread.start()

        self.putTaskButton.clicked.connect(self.put_task_button_clicked)
        self.exitThreadButton.clicked.connect(self.thread.exit_thread)

        self.task_id = 1

    def put_task_button_clicked(self):
        task = 'Task_{}'.format(self.task_id)
        self.thread.add_task(task)
        self.informationEdit.append('task [{}] added'.format(task))
        self.task_id += 1

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def result_handle(self, message):
        self.informationEdit.append('task [{}] finished.'.format(message))

    def task_started_show(self, task):
        self.informationEdit.append('task [{}] started.'.format(task))

    def thread_message_show(self, message):
        self.informationEdit.append(message)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.resize(500, 500)
    win.show()
    sys.exit(app.exec_())