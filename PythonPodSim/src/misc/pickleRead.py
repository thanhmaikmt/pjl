import pickle


x=[2,3,4]
y=[4,5,6]


f=open("tmp","w")


pickle.dump(x,f)

pickle.dump(y,f)