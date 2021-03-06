from tkinter import *
import numpy as np
import pandas as pd
import csv

obs=0 #--------------------------------------------->>>>>Global variable to store obesity index
finalpred=[]#------------------------------------------>>>>>> Store the 3 values
age_cat=""
most_prob=""

l1=['back_pain','constipation',
    'abdominal_pain','fatigue','diarrhoea',
    'mild_fever','yellowing_of_eyes',
    'swelled_lymph_nodes',
    'malaise','blurred_and_distorted_vision','phlegm',
    'throat_irritation','redness_of_eyes','sinus_pressure',
    'runny_nose','congestion','chest_pain','fast_heart_rate','dizziness',
    'obesity','excessive_hunger',
    'stiff_neck','loss_of_balance',
    'loss_of_smell',
    'passage_of_gases','internal_itching',
    'toxic_look_(typhos)','depression','irritability',
    'muscle_pain',
    'red_spots_over_body','belly_pain',
    'dischromic _patches',
    'watering_from_eyes','increased_appetite',
    'polyuria','family_history','mucoid_sputum',
    'rusty_sputum','lack_of_concentration',
    'visual_disturbances','blood_in_sputum',
    'pus_filled_pimples','blackheads',
    'scurring']

disease=['Fungal infection','Allergy',
'Peptic ulcer diseae','Diabetes','Bronchial Asthma','Hypertension',
' Migraine','Jaundice','Malaria','Chicken pox','Dengue','Typhoid','Tuberculosis',
'Common Cold','Pneumonia','Acne',]


l2=[]
for x in range(0,len(l1)):
    l2.append(0)
    
#--------------------------------------------------------------------------------------------------------   


"""
ysP=sa[["Prognosis"]]
np.ravel(ysP)
ysA=sa[["Age"]]
np.ravel(ysA)
ysR1=sa[["Rec1"]]
np.ravel(ysR1)
ysR2=sa[["Rec2"]]
np.ravel(ysR2)
ysR3=sa[["Rec3"]]
np.ravel(ysR3)

#slt_df = sa[(sa['Age'] == 'Adults') & (sa['Prognosis'] == 'Acne')] 
#print(slt_df['Rec1'])

for i in range(len(ysP)):
    if (ysP[i]=="Acne" and ysA[i]=="Teenagers"):
        print("yes")"""


# TRAINING DATA -------------------------------------------------------------------------------------
df=pd.read_csv("Training.csv")
df.replace({'prognosis':{'Fungal infection':0,'Allergy':1,
'Peptic ulcer diseae':2,'Diabetes ':3,'Bronchial Asthma':4,'Hypertension ':5,
'Migraine':6,'Jaundice':7,'Malaria':8,'Chicken pox':9,'Dengue':10,'Typhoid':11,'Tuberculosis':12,
'Common Cold':13,'Pneumonia':14,'Acne':15,}},inplace=True)

# print(df.head())

X= df[l1]

y = df[["prognosis"]]
np.ravel(y)
# print(y)

tr=pd.read_csv("Testing.csv")
tr.replace({'prognosis':{'Fungal infection':0,'Allergy':1,
'Peptic ulcer diseae':2,'Diabetes ':3,'Bronchial Asthma':4,'Hypertension ':5,
'Migraine':6,'Jaundice':7,'Malaria':8,'Chicken pox':9,'Dengue':10,'Typhoid':11,'Tuberculosis':12,
'Common Cold':13,'Pneumonia':14,'Acne':15,}},inplace=True)

X_test= tr[l1]
y_test = tr[["prognosis"]]
np.ravel(y_test)
# ------------------------------------------------------------------------------------------------------
def CalcBMI():
    global obs
    global age_cat
    personal = [Age.get(),Height.get(),Weight.get()]
    age=int(personal[0])
    h=float(personal[1])
    w=float(personal[2])
    bmi=(w/(h*h))
    print(bmi)
    if(bmi>29):
        obs=1
    else:
        obs=0
    print("Obesity: ",obs)
    
    if(age>55):
        age_cat="Senior Citizens"
    elif(age>17):
        age_cat="Adults"
    elif(age>8):
        age_cat="Teenagers"
    else:
        age_cat="Children"
    
    DecisionTree()
    
def OverallPred():
    global finalpred
    global age_cat
    global most_prob
    print(finalpred)
    print(age_cat)
    max=1
    if(finalpred.count(finalpred[0])>max):
        most_prob=finalpred[0]
    elif(finalpred.count(finalpred[1])>max):
        most_prob=finalpred[1]
    else:
        finalpred=[]
        DecisionTree()
    print(most_prob)
    
    t4.delete("1.0", END)
    t4.insert(END, most_prob)
    
    
    sa=pd.read_csv("samp.csv")
    sa.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'Peptic ulcer diseae':2,'Diabetes ':3,'Bronchial Asthma':4,'Hypertension ':5,'Migraine':6,'Jaundice':7,'Malaria':8,'Chicken pox':9,'Dengue':10,'Typhoid':11,'Tuberculosis':12,'Common Cold':13,'Pneumonia':14,'Acne':15,}},inplace=True)

    sl1=['Age','Rec1','Rec2','Rec3']
    Xs=sa[sl1]
    
    slt_df = sa[(sa['Age'] == age_cat) & (sa['Prognosis'] == most_prob)] 
    print(slt_df['Rec1'])
    print(slt_df['Rec2'])
    print(slt_df['Rec3'])
    
    
    t5.delete("1.0", END)
    t5.insert(END, slt_df['Rec1'])
    
    t6.delete("1.0", END)
    t6.insert(END, slt_df['Rec3'])
    
    t7.delete("1.0", END)
    t7.insert(END, slt_df['Rec2'])

    finalpred=[]
    

def DecisionTree():

    from sklearn import tree
    clf3 = tree.DecisionTreeClassifier()
    clf3 = clf3.fit(X,y)

    if(obs==1):
        psymptoms = [Symp1.get(),Symp2.get(),Symp3.get(),Symp4.get(),Symp5.get(),"obesity"]  #Patient Symptoms
    else:
        psymptoms = [Symp1.get(),Symp2.get(),Symp3.get(),Symp4.get(),Symp5.get()]

    for k in range(0,len(l1)):
        # print (k,)
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = clf3.predict(inputtest)
    predicted=predict[0]
    print(disease[predicted])
    
    global finalpred

    h='no'
    for a in range(0,len(disease)):
        if(predicted == a):
            h='yes'
            break


    if (h=='yes'):
    #    t1.delete("1.0", END)
     #   t1.insert(END, disease[a])
        finalpred.append(disease[predicted])

    else:
        print("")
     #   t1.delete("1.0", END)
     #   t1.insert(END, "Not Found")
        
    randomforest()


def randomforest():
    from sklearn.ensemble import RandomForestClassifier
    clf4 = RandomForestClassifier()
    clf4 = clf4.fit(X,np.ravel(y))
    
    if(obs==1):
        psymptoms = [Symp1.get(),Symp2.get(),Symp3.get(),Symp4.get(),Symp5.get(),"obesity"]
    else:
        psymptoms = [Symp1.get(),Symp2.get(),Symp3.get(),Symp4.get(),Symp5.get()]

    for k in range(0,len(l1)):
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = clf4.predict(inputtest)
    predicted=predict[0]
    print(disease[predicted])

    h='no'
    for a in range(0,len(disease)):
        if(predicted == a):
            h='yes'
            break
    global finalpred
    if (h=='yes'):
     #   t2.delete("1.0", END)
     #   t2.insert(END, disease[a])
        finalpred.append(disease[predicted])
    else:
        print("")
      #  t2.delete("1.0", END)
       # t2.insert(END, "Not Found")
    
    NaiveBayes()


def NaiveBayes():
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    gnb=gnb.fit(X,np.ravel(y))
    
    if(obs==1):
        psymptoms = [Symp1.get(),Symp2.get(),Symp3.get(),Symp4.get(),Symp5.get(),"obesity"]
    else:
        psymptoms = [Symp1.get(),Symp2.get(),Symp3.get(),Symp4.get(),Symp5.get()]
        
    for k in range(0,len(l1)):
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = gnb.predict(inputtest)
    predicted=predict[0]
    print(disease[predicted])

    h='no'
    for a in range(0,len(disease)):
        if(predicted == a):
            h='yes'
            break
    global finalpred
    if (h=='yes'):
        #t3.delete("1.0", END)
       # t3.insert(END, disease[a])
        finalpred.append(disease[predicted])
    else:
        print("")
        #t3.delete("1.0", END)
        #t3.insert(END, "Not Found")
        
    OverallPred()

# GUI BUILD - > Version 1

root = Tk()

# entry variables
Symp1 = StringVar()
Symp1.set(None)
Symp2 = StringVar()
Symp2.set(None)
Symp3 = StringVar()
Symp3.set(None)
Symp4 = StringVar()
Symp4.set(None)
Symp5 = StringVar()
Symp5.set(None)
Height = StringVar()
Weight = StringVar()
Age = StringVar()

# Heading
w2 = Label(root, justify=LEFT, text="Enter the 5 main Symptoms")
w2.config(font=(30))
w2.grid(row=1, column=0, columnspan=2, padx=100)

# labels
GenLb = Label(root, text="Enter Age")
GenLb.grid(row=4, column=0, pady=15, sticky=W)

HgLb = Label(root, text="Height in Meters")
HgLb.grid(row=5, column=0, pady=15, sticky=W)

WgLb = Label(root, text="Weight in kg")
WgLb.grid(row=6, column=0, pady=15, sticky=W)

S1Lb = Label(root, text="Symptom 1")
S1Lb.grid(row=7, column=0, pady=10, sticky=W)

S2Lb = Label(root, text="Symptom 2")
S2Lb.grid(row=8, column=0, pady=10, sticky=W)

S3Lb = Label(root, text="Symptom 3")
S3Lb.grid(row=9, column=0, pady=10, sticky=W)

S4Lb = Label(root, text="Symptom 4")
S4Lb.grid(row=10, column=0, pady=10, sticky=W)

S5Lb = Label(root, text="Symptom 5")
S5Lb.grid(row=11, column=0, pady=10, sticky=W)


#lrLb = Label(root, text="DecisionTree")
#lrLb.grid(row=15, column=0, pady=10,sticky=W)

#destreeLb = Label(root, text="RandomForest")
#destreeLb.grid(row=17, column=0, pady=10, sticky=W)

#ranfLb = Label(root, text="NaiveBayes")
#ranfLb.grid(row=18, column=0, pady=10, sticky=W)

oLb = Label(root, text="Final Predicion")
oLb.grid(row=19, column=0, pady=10, sticky=W)

rcm1Lb = Label(root, text="Immidiate solutions")
rcm1Lb.grid(row=20, column=0, pady=10, sticky=W)

rcm2Lb = Label(root, text="Specialist to Consult if persisting symptoms")
rcm2Lb.grid(row=21, column=0, pady=10, sticky=W)

rcm3Lb = Label(root, text="Other potential solutions")
rcm3Lb.grid(row=22, column=0, pady=10, sticky=W)

# entries
OPTIONS = sorted(l1)

AEn = Entry(root, textvariable=Age)
AEn.grid(row=4, column=1)

HgEn = Entry(root, textvariable=Height)
HgEn.grid(row=5, column=1)

WgEn = Entry(root, textvariable=Weight)
WgEn.grid(row=6, column=1)

S1En = OptionMenu(root, Symp1,*OPTIONS)
S1En.grid(row=7, column=1)

S2En = OptionMenu(root, Symp2,*OPTIONS)
S2En.grid(row=8, column=1)

S3En = OptionMenu(root, Symp3,*OPTIONS)
S3En.grid(row=9, column=1)

S4En = OptionMenu(root, Symp4,*OPTIONS)
S4En.grid(row=10, column=1)

S5En = OptionMenu(root, Symp5,*OPTIONS)
S5En.grid(row=11, column=1)


dst = Button(root, text="Predict", command=CalcBMI)
dst.grid(row=5, column=3,padx=10)

#dst = Button(root, text="Overall", command=OverallPred)
#dst.grid(row=6, column=3,padx=10)

#dst = Button(root, text="Predict", command=DecisionTree)
#dst.grid(row=8, column=3,padx=10)

#rnf = Button(root, text="Randomforest", command=randomforest)
#rnf.grid(row=9, column=3,padx=10)

#lr = Button(root, text="NaiveBayes", command=NaiveBayes)
#lr.grid(row=10, column=3,padx=10)

#textfileds
"""t1 = Text(root, height=1, width=40)
t1.grid(row=15, column=1, padx=10)

t2 = Text(root, height=1, width=40)
t2.grid(row=17, column=1 , padx=10)

t3 = Text(root, height=1, width=40)
t3.grid(row=18, column=1 , padx=10)"""

t4 = Text(root, height=1, width=40)
t4.grid(row=19, column=1 , padx=10)

t5 = Text(root, height=1, width=40)
t5.grid(row=20, column=1 , padx=10)

t6 = Text(root, height=1, width=40)
t6.grid(row=21, column=1 , padx=10)

t7= Text(root, height=1, width=40)
t7.grid(row=22, column=1 , padx=10)

root.mainloop()
