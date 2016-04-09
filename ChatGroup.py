
class ChatGroup():
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.users = []
        self.messages = []

    def ChangeName(self,newName):
        self.name == newName

    def AddUser(self,user):
        self.users.append(user)
