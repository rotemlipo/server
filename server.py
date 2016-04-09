from threading import Thread,Condition
import socket
import pickle
import Group
import UserReciever
import User


HOST = '127.0.0.1'
PORT = 8870
#the type of pacages recieved fron the client
comPacageLogin = "1"
comPacageNewUser = "2"
comPacageNewGroup = "3"
comPacageGetActiveUsers = "4"
#return comands
ackCommandLogin = "1"
ackComandRegister = "2"
nac = "0"
ackComandUsersList = "4"
#file paths
usersFileName = "D:/newNewnewserverfinalversionnewNewnew2/users.pkl"
groupsFileName = "D:/newNewnewserverfinalversionnewNewnew2/groups.pkl"

onlineUsers = [] ##list of the users that are currently connected
messages = []
count = 0
condition = Condition()

class HandleEachUser(Thread):
    def __init__(self,client,clientAddr):
        Thread.__init__(self)
        self.client = client
        self.clientAddr=clientAddr
    def run(self):
        while True:
            try:
                data = self.client.recv(1024)
                details = data.split(" ")
                self.HandleClientsComData(details,self.client,data,self.clientAddr)
            except Exception,e:
                print e
    def HandleClientsComData(self,clientData,client,data,clientAddr):
        returnComand = ""
        userGroups = ""
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
            user = self.Register(clientData[1],clientData[2],clientData[4],clientData[3])
            if user:
                returnComand = ackComandRegister
            else:
                returnComand = nac



        if clientData[0] == comPacageGetActiveUsers:
            returnComand = ackComandUsersList+" "+self.GetUsers()

        #take care of new group command
        if clientData[0] == comPacageNewGroup:
            usersForTheGroup = data[2:]
            listOfUsers = usersForTheGroup.split(" ")
            groupName = listOfUsers[0]
            listOfUsers.remove(groupName)
            self.NewGroup(listOfUsers,groupName)
            returnComand = "4"

        client.send(returnComand)

        # after login send the client the user group this user is part of
        if clientData[0] == comPacageLogin or clientData[0] == comPacageNewUser:
            userGroups = self.FindingUserGroups(clientAddr)
            client.send(userGroups) # send the client the user's groups
            condition.acquire()
            onlineUsers.append((user,client))  # add the user to the list of online users
            condition.notify()
            condition.release()

    def NewGroup(self, l,groupName):
        global count
        gr = Group(count,groupName)
        count = count+1
        usersList = pickle.load(open(usersFileName, "rb"))
        for username in l:
            for user1 in usersList:
                if user1[0].getUserName() == username:
                    Group.AddUser(user1)
        groupslist = pickle.load(open(groupsFileName,"rb"))
        self.SaveNewGroup(groupslist,gr)

    def SaveNewGroup(self,oldList,newGroup):
        oldList.append(newGroup)
        pickle.dump(oldList,open(usersFileName,"wb"))


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

    def FindingUserGroups(self,clientAddr):
        groupsfile = open(groupsFileName,"rb")
        usergroups = []
        l1 = pickle.load(groupsfile)
        groupsfile.close()
        for group in l1:
            for u in group.users:
                if u[1] == clientAddr:
                    usergroups.append((group.ID,group.name))
        groupsNames = ""
        for group in usergroups:
            groupsNames.append(group[1])
            groupsNames.append(";")
        return ";"+groupsNames




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

