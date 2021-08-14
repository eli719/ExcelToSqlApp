import threading

from cx_Oracle import DatabaseError


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self,daemon=True)
        self.args = args
        self.func = func
        self.result = ()

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except DatabaseError:
            return False
