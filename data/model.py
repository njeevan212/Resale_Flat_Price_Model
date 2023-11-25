import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV

df = pd.read_csv('/home/jeeva/Projects/python/Resale_Flat_Price_Model/data/combined.csv')

#print(df.dtypes)
#print(df.isnull().sum())

def get_median(x):
    split_list = x.split(' TO ')
    float_list = [float(i) for i in split_list]
    median = statistics.median(float_list)
    return median

df['storey_median'] = df['storey_range'].apply(lambda x: get_median(x))


scope_df = df[['cbd_dist','min_dist_mrt','floor_area_sqm','lease_remain_years','storey_median','resale_price']]
scope_df = scope_df.drop_duplicates()


#Checking Skewness
#sns.distplot(scope_df['cbd_dist']) # OK
#plt.show()

#sns.distplot(scope_df['min_dist_mrt']) # OK
#plt.show()

#sns.distplot(scope_df['floor_area_sqm']) # NOT OK
#plt.show()

#sns.distplot(scope_df['lease_remain_years']) # OK
#plt.show()

#sns.distplot(scope_df['storey_median']) # NOT OK
#plt.show()

#sns.distplot(scope_df['resale_price']) # NOT OK
#plt.show()


# Change the data of floor_area_sqm, storey_median and resale_price
scope_df['floor_area_sqm'] = np.log(scope_df['floor_area_sqm'])
#sns.distplot(scope_df['floor_area_sqm'])
#plt.show()

scope_df['storey_median'] = np.log(scope_df['storey_median'])
#sns.distplot(scope_df['storey_median'])
#plt.show()

scope_df['resale_price'] = np.log(scope_df['resale_price'])
#sns.distplot(scope_df['resale_price'])
#plt.show()


X=scope_df[['cbd_dist','min_dist_mrt','floor_area_sqm','lease_remain_years','storey_median']]
y=scope_df['resale_price']

# Normalizing the encoded data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# test and train split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


# Decision Tree Regressor
dtr = DecisionTreeRegressor()

# hyperparameters
param_grid = {
    'max_depth': [2, 5, 10, 15, 20, 22],
    'min_samples_split': [2, 3, 4, 5],
    'min_samples_leaf': [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
    'max_features': ['auto', 'sqrt', 'log2']
}


# gridsearchcv
grid_search = GridSearchCV(estimator=dtr, param_grid=param_grid, cv=5)
grid_search.fit(X_train, y_train)
print("Best hyperparameters:", grid_search.best_params_)
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)


# evalution metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
print(" ")
print('Mean squared error:', mse)
print('Mean Absolute Error', mae)
print('Root Mean squared error:', rmse)
print(" ")
print('R-squared:', r2)

# Saving the model
import pickle
with open('/home/jeeva/Projects/python/Resale_Flat_Price_Model/model.pkl', 'wb') as file:
    pickle.dump(best_model, file)
with open('/home/jeeva/Projects/python/Resale_Flat_Price_Model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)