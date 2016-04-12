__author__ = 'user'

class chatGroup():
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.users = []
        self.messages = []
    def GetName(self):
        return self.name
    def ChangeName(self,newName):
        self.name == newName

    def AddUser(self,user):
        self.users.append(user)
