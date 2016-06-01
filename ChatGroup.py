
class ChatGroup():
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []
        onlineusers = []

    def GetName(self):
        return self.name

    def AddMessage(self, mess):
        self.messages.append(mess)

    def GetMessages(self):
        return self.messages

    def GetUsers(self):
        return self.users

    def ChangeName(self,newName):
        self.name == newName

    def AddUser(self,user):
        self.users.append(user)
