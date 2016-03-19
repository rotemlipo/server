__author__ = 'user'
from threading import Thread

class Group(Thread):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.users = []
        Thread.__init__(self)

    def run(self):
        for message in messages:
            if message[2] == self.ID:
                for user in onlineUsers:
                    for user1 in self.users:
                        if user[0].getusername() == user1:
                            user[1].send(message[1])

    def ChangeName(self,newName):
        self.name == newName

    def AddUser(self,user):
        self.users.append(user)
