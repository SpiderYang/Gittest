import util
import threading
import Queue
import os
from os import path
import time
import shutil

class Mget(object):
    def __init__(self,queue,url,save_path=None,debug=False):
        self.url = url
        self.queue = queue
        self.debug = debug
        if not save_path:
            save_path = path.join(os.getcwd(),self.url.split('/')[-1])
        self.save_path = save_path
        self.hash = util.md5(url)
        self.temp_dir = path.join(os.getcwd(),'tmp')
        self.data_path = path.join(self.temp_dir,self.hash)
        self.meta = {}
        self.info_queue = Queue.Queue()
        #self.thread_num = 10
        self.start_time = time.time()
        self.threads = []
    def print_msg(self,*args):
        if self.debug:
            print " ".join([str(f) for f in args])

    def init(self):
        if not path.exists(self.temp_dir) and not path.isdir(self.temp_dir):
            os.mkdir(self.temp_dir)
        if not path.exists(self.data_path) and not path.isdir(self.data_path):
            os.mkdir(self.data_path)

        size = util.get_url_length(self.url,3)
        if size:  #不可能为负数.
            self.meta['size'] = size
            self.meta['readable_size'] = util.readable_size(size)
            if size > 1024*128:
                self.meta['num'] = size / 1024 /128
            else:
                self.meta['num'] = 1
            self.meta['chunk_size'] = size / self.meta['num']
        else:
            raise Exception("cant get Content-Length ")
        for i in range(self.meta['num']):
            self.threads.append(Work(self.url,util.download,self.queue))
    def process(self):
        chunk = [f for f in os.listdir(self.data_path) if '-' in f]
        return len(chunk) * 1.0 /self.meta['num']

    def is_finished(self):
        if not os.path.exists(self.data_path):
            return False
        for i in range(0,self.meta['num']):
            if not path.exists(self.chunk_path(i)):
                return False
        return True
    def combine(self):
        if self.is_finished():
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time
            with open(self.save_path,'w') as f:
                for i in range(0,self.meta['num']):
                    ck_path = self.chunk_path(i)
                    with open(ck_path) as fp:
                        f.write(fp.read())
                self.print_msg('All Done! elapsed time: %.3f' % self.elapsed_time)
        else:
            raise Exception("Not finish download")

    def clean(self):
        if path.exists(self.data_path) and path.isdir(self.data_path):
            shutil.rmtree(self.data_path)
        if not os.listdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def chunk_range(self,index):
        _start = index * self.meta['chunk_size']
        _end = _start + self.meta['chunk_size'] -1
        if index is self.meta['num'] -1 :
            _end += self.meta['size'] % self.meta['num']
        self.queue.put((_start,_end))

    def  chunk_path(self,index):
        return path.join(self.data_path,str(_start)+'-'+str(_end))
    def run(self):
        self.init()
        for i in range(self.threads):
            if i.isAlive():
                i.join()


class Work(threading.Thread):
    def __init__(self,url,func,queue):
        super(Work,self).__init__()
        self.func = func
        self.url = url
        self.queue = queue
        self.start()
    def run(self):
        while not self.queue.empty():
            try:
                _start,_end = self.queue.get()
                self.func(url,_start,_end)
            except:
                break
            self.queue.task_done()


    
