from threading import Thread,Condition
import socket
import pickle
import ChatGroup
import os
import User


HOST = '127.0.0.1'
PORT = 8870
#the type of pacages recieved fron the client
comPacageLogin = "1"
comPacageNewUser = "2"
comPacageNewGroup = "3"
comPacageGetActiveUsers = "4"
comGroupName = "7"
comChatMessage = "8"

#return comands
ackCommandLogin = "1"
ackComandRegister = "2"
nac = "0"
ackComandUsersList = "4"
ackComandUsersGroups = "5"
nacGroup = "6"
ackGroupIsOk = "7"
ackMessages = "8"
ackChatMessage = "9"

#file paths
usersFileName = os.path.dirname(os.path.realpath(__file__)) + "/users.pkl"
groupsFileName = os.path.dirname(os.path.realpath(__file__)) + "/groups.pkl"

condition = Condition()

onlineUsers = {}

class HandleEachUser(Thread):
    def __init__(self,client,clientAddr):
        Thread.__init__(self)
        self.client = client
        self.clientAddr=clientAddr
        self.currentUsername = ""
        self.chosenGroupName = ""
    def run(self):
        while True:
            try:
                data = self.client.recv(1024)
                details = data.split(" ")
                self.HandleClientsComData(details,self.client,data,self.clientAddr)
            except Exception,e:
                print e
                if onlineUsers.has_key(self.currentUsername):
                    del onlineUsers[self.currentUsername]
                break
    def HandleClientsComData(self,clientData,client,data,clientAddr):
        returnComand = ""
        messages = []
        print clientData
        user = User.User("","","","")

        #take care of login command
        if clientData[0] == comPacageLogin:
            user = self.CheckLogin(clientData[1],clientData[2])
            if user:
                returnComand =ackCommandLogin
            else:
                returnComand = nac


        #take care of register command
        if clientData[0] == comPacageNewUser:
            print clientData
            user = self.Register(clientData[1],clientData[2],clientData[4],clientData[3])
            if user:
                returnComand = ackComandRegister
            else:
                returnComand = nac

        if clientData[0] == comGroupName:
            grouplist = pickle.load(open(groupsFileName,"rb"))
            for group in grouplist:
                if group.GetName() == clientData[1]:
                    self.chosenGroupName = clientData[1]
                    messages = group.GetMessages()
            returnComand = ackMessages+";"
            for message in messages:
                returnComand = returnComand+message+";"



        if clientData[0] == comPacageGetActiveUsers:
            returnComand = ackComandUsersList+" "+self.GetUsers()

        #take care of new group command
        if clientData[0] == comPacageNewGroup:
            try:
                usersForTheGroup = data[2:]
                listOfUsers = usersForTheGroup.split(" ")
                groupName = listOfUsers[0]
                listOfUsers.remove(groupName)
                gr=self.NewGroup(listOfUsers,groupName)
                if gr != 0:
                    returnComand = ackGroupIsOk
                else:
                    returnComand = nacGroup
            except Exception,e:
                print e

        if clientData[0] == comChatMessage:
            message = ackChatMessage
            for i in range (1, len(clientData)):
                message = message +" "+clientData[i]
            grouplist = pickle.load(open(groupsFileName, "rb"))
            for group in grouplist:
                if group.GetName() == self.chosenGroupName:
                    group.AddMessage(message[2:])
                    group1 = group
            pickle.dump(grouplist,open(groupsFileName,"wb"))
            for user in group1.GetUsers():
                if onlineUsers.has_key(user.GetUserName()):
                    onlineUsers[user.GetUserName()].send(message)


        client.send(returnComand)

        # after login send the client the user group this user is part of
        if clientData[0] == comPacageLogin or clientData[0] == comPacageNewUser:
            onlineUsers.update({user.GetUserName():client})
            self.currentUsername = user.GetUserName()
            userGroups = self.FindingUserGroups(user)
            client.send(userGroups) # send the client the user's groups


    def NewGroup(self, l,groupName):
        global count
        flag = False
        gr = ChatGroup.ChatGroup(groupName)
        usersList = pickle.load(open(usersFileName, "rb"))
        for username in l:
            for user in usersList:
                if user.GetUserName() == username:
                    gr.AddUser(user)
        groupslist = pickle.load(open(groupsFileName,"rb"))
        for group in groupslist:
            if group.GetName() == groupName:
                flag = True
        if flag:
            return 0
        if not flag:
            self.SaveNewGroup(groupslist,gr)
        return gr

    def SaveNewGroup(self,oldList,newGroup):
        oldList.append(newGroup)
        pickle.dump(oldList,open(groupsFileName,"wb"))

    def GetUsers(self):
        usersList = pickle.load(open(usersFileName, "rb"))
        usersNames = ""
        i = 1
        for user in usersList:
            usersNames = usersNames + user.GetUserName()
            if i < len(usersList):
                usersNames = usersNames + " "
            i=i+1

        return usersNames

    def FindingUserGroups(self,user):
        groupsfile = open(groupsFileName,"rb")
        l1 = pickle.load(groupsfile)
        groupsfile.close()
        usergroups = ";"
        for group1 in l1:
            for u in group1.users:
                if u.GetUserName() == user.GetUserName():
                  usergroups = usergroups+ group1.GetName()+ ";"
        return usergroups




    def CheckLogin(self, userName,password):
        """
        checking if the user exists in the pickle
        :return: user (if the user exists), 0(if it doesnt)
        """
        listOfUsers = pickle.load(open(usersFileName, "rb"))
        print listOfUsers
        for user1 in listOfUsers:
            print user1
            print user1.GetUserName()
            print user1.GetPass()
            if user1.GetUserName() == userName and user1.GetPass() == password:
               return user1
        return 0 #the user doesnt exist


    def Register(self,firstName, lastName, password,userName):
        """
        the function checks if the user's username already exists and if it doesnt it creates the new user
        :return: user (if the username didnt exist), 0 (if the username exist)
        """
        print firstName+lastName+password+userName
        user = User.User(firstName, lastName, password,userName)
        listOfUsers = pickle.load(open(usersFileName, "rb"))
        print listOfUsers
        for user1 in listOfUsers:
            if user1.GetUserName() == userName:
                return 0 #the username exists
        self.SaveNewUser(user,listOfUsers)
        return user



    def SaveNewUser(self, user, oldList):
        """
        the username does not exist, we add the new user to the list in the pickle
        :param oldList: old list of users from the pickle
        """
        oldList.append(user)
        pickle.dump(oldList,open(usersFileName,"wb"))


def Main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print 'server is up'
    print 'Listening on:', PORT
    while 1:
        try:
            conn, addr = sock.accept()
            print 'new client was connected - ',addr
            handleEachUser = HandleEachUser(conn, addr)
            handleEachUser.start()
        except Exception, e:
            print e



Main()

