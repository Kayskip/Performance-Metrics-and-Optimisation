# -*- coding: utf-8 -*-
"""Classification-Pipeline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D2bVYW0vlmZwxjGykzp5KwPwS0yRFOeP
"""

# Load and import general libraries
import numpy
# Load and import general libraries
import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
# MSE
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
# Regression
from sklearn.metrics import precision_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
from sklearn import metrics
from google.colab import files
import io
from google.colab import drive
import time

# read in file
# dataTrain = pd.read_csv('adultTrain.csv')
# dataTest = pd.read_csv('adultTest.csv')
drive.mount('/content/gdrive')
train_data = pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/adultTrain.csv')

test_data = pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/adultTest.csv')

train_data.columns = ["Age", "workclass", "Final_Weight", "Education", "Highest_Grade", "Marital_Status", "Occupation", "Relationship", "Race", "Sex", "Capital_Gain", "Capital_Loss", "Hours_per_Week", "Native_Country", "Income_Class"]
test_data.columns = ["Age", "workclass", "Final_Weight", "Education", "Highest_Grade", "Marital_Status", "Occupation", "Relationship", "Race", "Sex", "Capital_Gain", "Capital_Loss", "Hours_per_Week", "Native_Country", "Income_Class"]

# drop the index column
print(train_data.head())
print(test_data.head())

# transform work-class to int
def trans_work_class(x):
    if x == " Never-worked":
        return 7
    elif x == " Without-pay":
        return 6
    elif x == " State-gov":
        return 5
    elif x == " Local-gov":
        return 4
    elif x == " Federal-gov":
        return 3
    elif x == " Self-emp-inc":
        return 2
    elif x == " Self-emp-not-inc":
        return 1
    elif x == " Private":
        return 0
    else:
        return "?"

# transform education to int
def trans_education(x):
    if x == " Preschool":
        return 1
    elif x == " 1st-4th":
        return 2
    elif x == " 5th-6th":
        return 3
    elif x == " 7th-8th":
        return 4
    elif x == " 9th":
        return 5
    elif x == " 10th":
        return 6
    elif x == " 11th":
        return 7
    elif x == " 12th":
        return 8
    elif x == " HS-grad":
        return 9
    elif x == " Some-college":
        return 10
    elif x == " Assoc-voc":
        return 11
    elif x == " Assoc-acdm":
        return 12
    elif x == " Bachelors":
        return 13
    elif x == " Masters":
        return 14
    elif x == " Prof-school":
        return 15
    elif x == " Doctorate":
        return 16
    else:
        return '?'

# transform marital_status to int
def trans_marital_status(x):
    if x == " Married-AF-spouse":
        return 6
    elif x == " Married-spouse-absent":
        return 5
    elif x == " Widowed":
        return 4
    elif x == " Separate":
        return 3
    elif x == " Never-married":
        return 2
    elif x == " Divorced":
        return 1
    elif x == " Married-civ-spouse":
        return 0
    else:
        return '?'

# transform occupation to int
def trans_occupation(x):
    if x == " Armed-Forces":
        return 13
    elif x == " Protective-serv":
        return 12
    elif x == " Priv-house-serv":
        return 11
    elif x == " Transport-moving":
        return 10
    elif x == " Farming-fishing":
        return 9
    elif x == " Adm-clerical":
        return 8
    elif x == " Machine-op-inspct":
        return 7
    elif x == " Handlers-cleaners":
        return 6
    elif x == " Prof-specialty":
        return 5
    elif x == " Exec-managerial":
        return 4
    elif x == " Sales":
        return 3
    elif x == " Other-service":
        return 2
    elif x == " Craft-repair":
        return 1
    elif x == " Tech-support":
        return 0
    else:
        return '?'

# transform relationship to int
def trans_relationship(x):
    if x == " Unmarried":
        return 5
    elif x == " Other-relative":
        return 4
    elif x == " Not-in-family":
        return 3
    elif x == " Husband":
        return 2
    elif x == " Own-child":
        return 1
    elif x == " Wife":
        return 0
    else:
        return '?'

# transform race to int
def trans_race(x):
    if x == " Black":
        return 4
    elif x == " Other":
        return 3
    elif x == " Amer-Indian-Eskimo":
        return 2
    elif x == " Asian-Pac-Islander":
        return 1
    elif x == " White":
        return 0
    else:
        return '?'

# transform sex to int
def trans_sex(x):
    if x == " Female":
        return 1
    elif x == " Male":
        return 0
    else:
        return "?"

# transform occupation to int
def trans_native_country(x):
    if x == " Holand-Netherlands":
        return 40
    elif x == " Hong":
        return 39
    elif x == " Peru":
        return 38
    elif x == " Trinadad&Tobago":
        return 37
    elif x == " El-Salvador":
        return 36
    elif x == " Yugoslavia":
        return 35
    elif x == " Thailand":
        return 34
    elif x == " Scotland":
        return 33
    elif x == " Nicaragua":
        return 32
    elif x == " Guatemala":
        return 31
    elif x == " Hungary":
        return 30
    elif x == " Columbia":
        return 29
    elif x == " Haiti":
        return 28
    elif x == " Taiwan":
        return 27
    elif x == " Ecuador":
        return 26
    elif x == " Laos":
        return 25
    elif x == " Dominican-Republic":
        return 24
    elif x == " France":
        return 23
    elif x == " Ireland":
        return 22
    elif x == " Portugal":
        return 21
    elif x == " Mexico":
        return 20
    elif x == " Vietnam":
        return 19
    elif x == " Jamaica":
        return 18
    elif x == " Poland":
        return 17
    elif x == " Italy":
        return 16
    elif x == " Philippines":
        return 15
    elif x == " Honduras":
        return 14
    elif x == " Iran":
        return 13
    elif x == " Cuba":
        return 12
    elif x == " China":
        return 11
    elif x == " South":
        return 10
    elif x == " Greece":
        return 9
    elif x == " Japan":
        return 8
    elif x == " India":
        return 7
    elif x == " Outlying-US(Guam-USVI-etc)":
        return 6
    elif x == " Germany":
        return 5
    elif x == " Canada":
        return 4
    elif x == " Puerto-Rico":
        return 3
    elif x == " England":
        return 2
    elif x == " Cambodia":
        return 1
    elif x == " United-States":
        return 0
    else:
        return '?'

# transform income_class to int
def trans_income_class(x):
    if x == " <=50K":
        return 1
    elif x == " >50K":
        return 0
    else:
        return '?'

# transform income_class to int
def trans_income_class_test(x):
    if x == " <=50K.":
        return 1
    elif x == " >50K.":
        return 0
    else:
        return '?'

# replace current columns with new int versions
#train
train_data['workclass'] = train_data['workclass'].apply(trans_work_class)
train_data['Education'] = train_data['Education'].apply(trans_education)
train_data['Marital_Status'] = train_data['Marital_Status'].apply(trans_marital_status)
train_data['Occupation'] = train_data['Occupation'].apply(trans_occupation)
train_data['Relationship'] = train_data['Relationship'].apply(trans_relationship)
train_data['Race'] = train_data['Race'].apply(trans_race)
train_data['Sex'] = train_data['Sex'].apply(trans_sex)
train_data['Native_Country'] = train_data['Native_Country'].apply(trans_native_country)
train_data['Income_Class'] = train_data['Income_Class'].apply(trans_income_class)
#test
test_data['workclass'] = test_data['workclass'].apply(trans_work_class)
test_data['Education'] = test_data['Education'].apply(trans_education)
test_data['Marital_Status'] = test_data['Marital_Status'].apply(trans_marital_status)
test_data['Occupation'] = test_data['Occupation'].apply(trans_occupation)
test_data['Relationship'] = test_data['Relationship'].apply(trans_relationship)
test_data['Race'] = test_data['Race'].apply(trans_race)
test_data['Sex'] = test_data['Sex'].apply(trans_sex)
test_data['Native_Country'] = test_data['Native_Country'].apply(trans_native_country)
test_data['Income_Class'] = test_data['Income_Class'].apply(trans_income_class_test)

#final weight and education have low correlations, lets remove them! we cannot check the correlations of columns with missing values untill we have dealt with them
train_data=train_data.drop(columns=['Final_Weight', 'Education'])
test_data=test_data.drop(columns=['Final_Weight', 'Education'])

#Firstly we need to understand if these missing values are random or not, analysing the data we can #see that if workclass is missing then so is occupation
#These two columns seem to relate to each other in terms of missing values, we can conclude that these missing missing values arent completly random and maybe due to the adult being off the radar
#so for both work class and occupation, we want to set the missing values to some new numeric number that currently does not exist in that attribute.
train_data[["workclass", "Occupation"]] = train_data[["workclass", "Occupation"]].replace('?', 99)
test_data[["workclass", "Occupation"]] = test_data[["workclass", "Occupation"]].replace('?', 99)

#seeing as the remaining missing values on the test set is still larger than 5% we will impute the remaining missing values using the mean of the respective attribute
#on the training set!

#first change '?' to NaN
train_data[["Age", "workclass", "Highest_Grade", "Marital_Status", "Occupation", "Relationship", "Race", "Sex", "Capital_Gain", "Capital_Loss", "Hours_per_Week", "Native_Country"]] = train_data[["Age", "workclass", "Highest_Grade", "Marital_Status", "Occupation", "Relationship", "Race", "Sex", "Capital_Gain", "Capital_Loss", "Hours_per_Week", "Native_Country"]].replace('?', numpy.NaN)
test_data[["Age", "workclass", "Highest_Grade", "Marital_Status", "Occupation", "Relationship", "Race", "Sex", "Capital_Gain", "Capital_Loss", "Hours_per_Week", "Native_Country"]] = test_data[["Age", "workclass", "Highest_Grade", "Marital_Status", "Occupation", "Relationship", "Race", "Sex", "Capital_Gain", "Capital_Loss", "Hours_per_Week", "Native_Country"]].replace('?', numpy.NaN)

#remember the missing values for the test set have to be imputed by the mean of the training set!!
train_data.fillna(train_data.mean(), inplace=True)
test_data.fillna(test_data.mean(), inplace=True)

#Missing values all done!! Now lets just check the correlations again to check the correlations of the attributes we couldnt check before
# plt.title("Correlation Plot")
# corr = dataTrain.corr()
# sns.heatmap(data=corr, square=True, annot=True, cbar=True)
# plt.show()

#all correlations are above 0.01 so lets go ahead and train/test
RSquared_Scores = []

def getXNYVals(data):
    X = data.drop(["Income_Class"], axis=1)
    y = data["Income_Class"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=1)

    return X_train, y_train

X_trn, y_trn = getXNYVals(train_data)
X_tst, y_tst = getXNYVals(test_data)

X_train=X_trn
y_train=y_trn

X_test=X_tst
y_test=y_tst

def eval_model(model_type):
    start_time = time.time()
    model = model_type
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    auc = metrics.roc_auc_score(y_test, y_predict)
    print('----------------------------------------------------------------------------')
    print(model_type)
    print('----------------------------------------------------------------------------')

    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict, average='weighted')
    recall = recall_score(y_test, y_predict, average='binary')
    f1 = 2 * (precision * recall) / (precision + recall)

    print()
    print('Accuracy: %0.2f ' % accuracy)
    print('Precision score: {0:0.2f}'.format(precision))
    print('Average recall score: %0.2f' % recall)
    print('F1_score: %0.2f' % f1)
    print('AUC: %0.2f' % auc)
    print('\n\n')
    print("--- %s seconds ---" % (time.time() - start_time))

# (1) kNN
# (2) naiveBayes
# (3) SVM
# (4) decision tree
# (5) random forest
# (6) AdaBoost
# (7) gradient Boosting
# (8) linear discriminant analysis
# (9) multi-layer perceptron
# (10) logistic regression


def main():
    eval_model(KNeighborsClassifier())
    eval_model(GaussianNB())
    eval_model(svm.SVC(gamma='auto'))
    eval_model(tree.DecisionTreeClassifier())
    eval_model(RandomForestClassifier(n_estimators=100, max_depth=2,random_state=309))
    eval_model(AdaBoostClassifier(n_estimators=50, learning_rate=1, random_state=309))
    eval_model(GradientBoostingClassifier())
    eval_model(LinearDiscriminantAnalysis())
    eval_model(MLPClassifier())
    eval_model(LogisticRegression())

main()