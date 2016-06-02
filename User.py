__author__ = 'user'
__author__ = 'RachelSch'


#user class.
class User():
    def __init__(self,username, firstname,lastname,password):
        self.firsname=firstname
        self.lastname=lastname
        self.password=password
        self.username=username
    def GetName(self):
        #returning user's first name
        return  self.firsname
    def GetLast(self):
        #returning user's last name
        return  self.lastname
    def GetPass(self):
        #returning user's password
        return  self.password
    def GetUserName(self):
        #returning user's username
        return  self.username