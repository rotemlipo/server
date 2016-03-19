from threading import Thread,Condition
import socket
import pickle
import Group
import UserReciever
import User

usersFileName = "D:/newNewnewserverfinalversionnewNewnew2/users.pkl"
groupsFileName = "D:/newNewnewserverfinalversionnewNewnew2/groups.pkl"
onlineUsers = [] ##list of the users that are currently connected
messages = []
count = 0
condition = Condition()
class Connection(Thread):
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1",8870))
        self.socket.listen(3)
        Thread.__init__(self)

    def run(self):
        global clientList
        while True:
            client, clientAddr = self.socket.accept()
            data = client.recv(1024)
            details = data.split(" ")
            if details[0] == "1":
                user = self.CheckLogin(details[1], details[2])
            elif details[0] == "2":
                user = self.Register(details[1],details[2],details[4],details[3])
            if details[0] == "1" or details[0] == "2" and user:
                if details[0] == "1":
                    client.send("2")
                elif details[0] == "2":
                    client.send("3")
                usergroups = self.FindingUserGroups(clientAddr)
                groupsNames = ""
                for group in usergroups:
                    groupsNames.append(group[1])
                    groupsNames.append(";")
                client.send(";"+groupsNames)
                condition.acquire()
                onlineUsers.append((user,client))
                condition.notify()
                condition.release()
                ur = UserReciever(client,user)
                ur.start()
            elif details[0] == "1" or details[0] =="2" and not user:
                client.send("1")
            elif details[0] == "3":
                usersForTheGroup = data[2:]
                l = usersForTheGroup.split(" ")
                self.NewGroup(l)

    def FindingUserGroups(self,clientAddr):
        groupsfile = open(groupsFileName,"rb")
        usergroups = []
        l1 = pickle.load(groupsfile)
        groupsfile.close()
        for group in l1:
            for u in group.users:
                if u[1] == clientAddr:
                    usergroups.append((group.ID,group.name))
        return usergroups
    def NewGroup(self, l):
        global count
        gr = Group(count,"group number "+str(count))
        count = count+1
        for username in l:
            for user1 in onlineUsers:
                if user1[0].getUserName() == username:
                    Group.AddUser(user1)
        groupsfile = open(groupsFileName,"rb")
        pickle.dump(gr)
        groupsfile.close()


    def CheckLogin(self, userName,password):
        userfile = open(usersFileName, "rb")
        l = pickle.load(userfile)
        userfile.close()
        for u in l:
            if u.getUserName() == userName and u.getPassword() == password:
                return u
        return 0


    def Register(self,userName , password, firstName, lastName):
        """
        the function checks if the user's username already exists and if it doesnt it creates the new user
        :param userName:
        :param password:
        :param firstName:
        :param lastName:
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
        :param user:
        :param oldList:
        """
        oldList.append(user)
        pickle.dump(oldList,open(usersFileName,"wb"))




c=Connection()
c.start()


