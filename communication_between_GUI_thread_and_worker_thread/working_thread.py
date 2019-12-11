#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""synchronous communication between GUI thread and working thread in PyQt5 """
import sys
import time
from collections import deque
from PyQt5 import QtCore


class WorkingThread(QtCore.QThread):
    taskStarted = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int)
    taskFinished = QtCore.pyqtSignal(str)
    threadMessage = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.tasks = deque()  # task queue
        self.exitThread = False
        self.mutex = QtCore.QMutex()
        self.taskAdded = QtCore.QWaitCondition()


    def exit_thread(self):
        ''' 调用此函数安全结束线程(在任务完成后) '''
        self.exitThread = True
        self.taskAdded.wakeOne()

    def add_task(self, task:str):
        ''' 添加线程任务，此处用str代替具体任务 '''
        with QtCore.QMutexLocker(self.mutex):
            # 将任务加入到队列，并唤醒线程
            self.tasks.append(task)
            self.taskAdded.wakeOne()

    def run(self):
        while True:
            with QtCore.QMutexLocker(self.mutex):
                if not len(self.tasks):
                    self.threadMessage.emit('working thread is waiting...')
                    self.taskAdded.wait(self.mutex)
                # 退出线程
                if self.exitThread:
                    break
                # 从任务队列中获取最先加入的任务
                task = self.tasks.popleft()
            # 通知主线程开始处理某个任务
            self.taskStarted.emit(task)
            # 假设此处有一个5s的耗时任务，任务过程中不断汇报进度
            for i in range(100):
                time.sleep(0.05)
                self.progressSignal.emit(i+1)
            # 完成任务，通知主线程
            self.taskFinished.emit(task)

        self.exitThread = False
        self.threadMessage.emit('thread exit.')

            


