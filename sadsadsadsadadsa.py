l = []
f = open("users.pkl", "a+")
import pickle
pickle.dump(l,f)
f1 = open("groups.pkl","a+")
pickle.dump(l,f1)
