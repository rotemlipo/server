__author__ = 'user'
__author__ = 'RachelSch'
class User():
    def __init__(self,username, firstname,lastname,password):
        self.firsname=firstname
        self.lastname=lastname
        self.password=password
        self.username=username
    def SetClient(self,myClient):
        self.MyClient = myClient
    def GetClient(self):
        return self.MyClient
    def GetName(self):
        return  self.firsname
    def GetLast(self):
        return  self.lastname
    def GetPass(self):
        return  self.password
    def GetUserName(self):
        return  self.username
    def __repr__(self):
        return self.firsname+" "+self.lastname+" "+self.GetUserName()+" "+self.GetPass()
