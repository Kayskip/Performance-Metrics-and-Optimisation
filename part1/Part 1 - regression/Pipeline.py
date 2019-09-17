
# coding: utf-8

# In[1]:


# Load and import general libraries

import pandas as pd
from sklearn import linear_model
from sklearn import tree
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
import seaborn as sns
import time
sns.set(style="white", color_codes=True)
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR


# In[2]:


# read in file
data = pd.read_csv('diamonds.csv')

# drop the index column
data = data.drop(data.columns[0], axis=1)


# In[3]:


# transform cut to int
def trans_cut(x):
    if x == "Fair": return 4
    if x == "Good": return 3
    if x == "Very Good": return 2
    if x == "Ideal": return 1
    if x == "Premium": return 0


# In[4]:


# transform color into int
def trans_color(x):
    if x == "D": return 0
    if x == "E": return 1
    if x == "F": return 2
    if x == "G": return 3
    if x == "H": return 4
    if x == "I": return 5
    if x == "J": return 6


# In[5]:


# transform clarity to int
def trans_clarity(x):
    if x == "I1": return 7
    if x == "SI1": return 6
    if x == "SI2": return 5
    if x == "VS1": return 4
    if x == "VS2": return 3
    if x == "VVS1": return 2
    if x == "VVS2": return 1
    if x == "IF": return 0


# In[6]:


# replace current columns with new int versions
data['cut'] = data['cut'].apply(trans_cut)
data['color'] = data['color'].apply(trans_color)
data['clarity'] = data['clarity'].apply(trans_clarity)


# In[7]:


# drop missing values
data = data[(data[['x', 'y', 'z']] != 0).all(axis=1)]


# In[8]:


label_cut = LabelEncoder()
label_color = LabelEncoder()
label_clarity = LabelEncoder()
data['cut'] = label_cut.fit_transform(data['cut'])
data['color'] = label_color.fit_transform(data['color'])
data['clarity'] = label_clarity.fit_transform(data['clarity'])


# In[9]:


# splitting to train and test
X = data.drop(['price'], axis=1)
y = data['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=309)


# In[10]:


RSquared_Scores = []


# In[11]:


def eval_model(model_type):
    start_time = time.time()
    model = model_type
    model.fit(X_train , y_train)
    cross_val_results = cross_val_score(estimator = model, X = X_train, y = y_train, cv = 5,verbose = 1)

    y_predict = model.predict(X_test)
    print('----------------------------------------------------------------------------')
    print(model_type)
    print('----------------------------------------------------------------------------')
    print('Results: %.2f' % model.score(X_test, y_test))
    print(cross_val_results)

    mse = mean_squared_error(y_test, y_predict)
    rmse = mean_squared_error(y_test, y_predict)**0.5
    r2 = r2_score(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)

    print()
    print('MSE    : %0.2f ' % mse)
    print('RMSE   : %0.2f ' % rmse)
    print('R2     : %0.2f ' % r2)
    print('MAE    : %0.2f ' % mae)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n\n')

    RSquared_Scores.append(r2)


# In[12]:


def ScaledSGDRegression():
    start_time = time.time()

    scaler = StandardScaler()
    scaler.fit(X)
    Xs = scaler.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.3, random_state=309)
    sgd = linear_model.SGDRegressor()
    sgd.fit(X_train, y_train)


    y_pred=sgd.predict(X_test)
    print('Results: %.2f' % sgd.score(X_test, y_test))

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred)**0.5
    r2 = r2_score(y_test, y_pred)

    print()
    print('MSE    : %0.2f ' % mse)
    print('RMSE   : %0.2f ' % rmse)
    print('R2     : %0.2f ' % r2)
    print('MAE    : %0.2f ' % mae)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n\n')


# In[13]:


def ScaledSVR():
    start_time = time.time()


    print('###### Support Vector Regression (SVR) #######')
    scaler = StandardScaler()
    scaler.fit(X)
    Xs = scaler.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.3, random_state=309)


    #Then we fit the regressor to the scaled dataset :

    #fitting the SVR to the dataset

    regressor = SVR(kernel='rbf',C=100)
    regressor.fit(X_train, y_train)
    y_pred=regressor.predict(X_test)

    print('')
    print('Score : %.4f' % regressor.score(X_test, y_test))

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred)**0.5
    r2 = r2_score(y_test, y_pred)

    print('')
    print('MSE    : %0.2f ' % mse)
    print('MAE    : %0.2f ' % mae)
    print('RMSE   : %0.2f ' % rmse)
    print('R2     : %0.2f ' % r2)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n\n')


# In[14]:


def main():
    eval_model(LinearRegression())
    eval_model(KNeighborsRegressor())
    eval_model(Ridge(alpha=1.0))
    eval_model(tree.DecisionTreeClassifier())
    ScaledSGDRegression()
    ScaledSVR()
    eval_model(RandomForestRegressor())
    eval_model(GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=309, loss='ls', verbose=1))
    eval_model(LinearSVR(random_state=309, tol=1e-5))
    eval_model(MLPRegressor(max_iter=1000))


# In[ ]:


main()

