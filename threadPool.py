import threading
import Queue
import time

class threadPool(object):
    def __init__(self,func,work_num=10000,thread_num=10):
        self.threads = []
        self.task_queue = Queue.Queue()
        self.func = func
        self.work_num = work_num
        self.thread_num = thread_num
        self.__init_work_num()
        self.__init_thread_num()
    def __init_thread_num(self):
        for i in range(self.thread_num):
            self.threads.append(Work(self.task_queue))
    def __init_work_num(self):
        for i in range(self.work_num):
            self.task_queue.put((self.func,i))
    def wait_all(self):
        for i in self.threads:
            if i.isAlive():i.join()

class Work(threading.Thread):
    def __init__(self,task_queue):
        super(Work,self).__init__()
        self.task_queue = task_queue
        self.start()
    def run(self):
        while 1:
            try:
                (func,args) = self.task_queue.get(block=False)
                func(args)
                self.task_queue.task_done()
            except:
                break

def dojob(args):
    time.sleep(0.1)
    print [threading.currentThread(),args]

if __name__ == "__main__":
    start = time.time()
    work_manager = threadPool(dojob,thread_num=20)
    work_manager.wait_all()
    end = time.time()
    print "cost time:",(time.time()-start)
