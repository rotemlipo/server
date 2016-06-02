#group class
class ChatGroup():
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def GetName(self):
        #returning group's name
        return self.name

    def AddMessage(self, mess):
        #adding a message ("mess") to group's messages list
        self.messages.append(mess)

    def GetMessages(self):
        #returning group's messages
        return self.messages

    def GetUsers(self):
        #returning group's users
        return self.users

    def AddUser(self,user):
        #adding a user ("user") to the list of users
        self.users.append(user)
