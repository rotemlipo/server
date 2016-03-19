from threading import Thread,Condition
import socket
import pickle
import Group
import UserReciever
import User


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
        groupsfile = open("D:/newNewnewserverfinalversionnewNewnew2/groups.pkl","rb")
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
        groupsfile = open("D:/newNewnewserverfinalversionnewNewnew2/groups.pkl","rb")
        pickle.dump(gr)
        groupsfile.close()


    def CheckLogin(self, userName,password):
        userfile = open("D:/newNewnewserverfinalversionnewNewnew2/users.pkl", "rb")
        l = pickle.load(userfile)
        userfile.close()
        for u in l:
            if u.getUserName() == userName and u.getPassword() == password:
                return u
        return 0

    def Register(self,userName , password, firstName, lastName):
        userfile = open("D:/newNewnewserverfinalversionnewNewnew2/users.pkl", "rb")
        user = User.User(firstName, lastName, password,userName)
        l = pickle.load(userfile)
        for u in l:
            if u.getusername() == userName:
                return 0
        userfile.close()
        userfile=open("D:/newNewnewserverfinalversionnewNewnew2/users.pkl","w+")
        pickle.dump(user,userfile)
        userfile.close()
        return user


c=Connection()
c.start()


