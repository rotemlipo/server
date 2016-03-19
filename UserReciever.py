__author__ = 'user'
from threading import Thread, Condition

class UserReceiver(Thread):
    def __init__(self, client, user):
        self.cl = client
        self.user = user
        Thread.__init__(self)

    def run(self):
        is_running = 1
        while is_running:
            try:
                data = self.cl.recv(1024*8)
                # 2 SFAROT RISHONOT = GROUP ID
                groupID = int(data[:1])
                message = data[2:]
                condition.acquire()
                messages.append((self.user, message, groupID))
                condition.notify()
                condition.release()
            except Exception, e:
                is_running = 0
                print e
