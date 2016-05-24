
class ChatGroup():
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def GetName(self):
        return self.name

    def GetMessages(self):
        return self.messages

    def ChangeName(self,newName):
        self.name == newName

    def AddUser(self,user):
        self.users.append(user)
