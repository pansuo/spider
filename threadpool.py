#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tankywoo@2013-02-27

from threading import Thread
from Queue import Queue, Empty

class Worker(Thread):
	def __init__(self, taskQueue):
		Thread.__init__(self)
		self.state = True
		self.taskQueue = taskQueue
		self.start()

	def run(self):
		while True:
			if not self.state:
				break
			try:
				func, argv = self.taskQueue.get()
				func(argv)
				self.taskQueue.task_done()
			except Empty:
				continue
	
	def stop(self):
		self.state = False


class ThreadPool:
	def __init__(self, poolSize):
		self.taskQueue = Queue()
		self.pool = list()
		self.poolSize = poolSize

	def initPool(self):
		for i in xrange(self.poolSize):
			worker = Worker(self.taskQueue)
			self.pool.append(worker)
	
	def stopPool(self):
		for _thread in self.pool:
			_thread.stop()
	
	def putTask(self, func, **kwargs):
		self.taskQueue.put((func, kwargs))

	def getTask(self):
		pass

	def taskJoin(self):
		self.taskQueue.join()

