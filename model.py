#this will be the forecasting model for the data ingested
#model to use could be a simple random forest, winters holt etc 
#use test data set to evaluate model and train 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt 
import matplotlib.pyplot as plt
import os
def Model_1_RF (x_train,y_train,x_test,y_test):
    #create model
    model = RandomForestRegressor()
    params = {'n_estimators': 300, 'max_depth': 5, 'random_state': 42}
    model.set_params(**params)
    #train model 
    model.fit(x_train,y_train)
    #predict on test data
    y_pred = model.predict(x_test)
    '''
    #remove Grade 10's 
    inds = np.where(x_test['Grade'] == 10)
    y_pred = np.delete(y_pred, inds)
    y_test = np.delete(y_test, inds)
    '''
    #RMSE 
    RMSE = np.sqrt(mean_squared_error(y_test, y_pred))
    #split up the data by grades from results
    print("Predicted Results: ",y_pred) 
    print("Actual Results: ",y_test)
    pred_res = pd.DataFrame({'Actual Price': y_test, 'Predicted Price': y_pred})
    pred_res['Grade']= x_test['Grade']
    #Print each grade mean predicted price
    print(f"Each grade mean predicted price: ",pred_res.groupby('Grade').mean())
    #finished dataframe
    pred_res = pred_res.groupby('Grade').mean()
    pred_res = pred_res.reset_index()
    #fix column names 
    pred_res = pred_res.rename(columns={'Actual Price': 'Avg. Actual Price', 'Predicted Price': 'Forecasted Price', 'Grade': 'Grade'})
    #print each grades mean predicted price 
    #evaluate model
    print(f"The mean squared error is {RMSE}")
    ax, fig = plt.subplots()
    fig = sns.scatterplot(x = y_test, y = x_test['Grade'], label = "Actual", color = "blue")
    fig = sns.scatterplot(x = y_pred, y = x_test['Grade'], label = "Predicted", color = "red")
    plt.show()
    return pred_res
def clean_data(Data):
    #clean and split data 
    #remove description column 
    Data1 = Data.drop(Data.columns[1], axis=1)
    #remove name column 
    Data1 = Data1.drop(Data1.columns[3], axis=1)
    print(Data1.head())
    
    #make date column date time 
    Data1['Date Sold'] = pd.to_datetime(Data1['Date Sold'])
    #sort data by date
    Data1.sort_index(inplace = True , ascending = True)
    #get weekday/ weekend 
    Data1['Weekend'] = Data1['Date Sold'].dt.dayofweek.apply(lambda x: 0 if x < 5 else 1)# 0 = weekday, 1 = weekend
    #drop date column
    Data1 = Data1.drop('Date Sold', axis=1)
    #use incase Date Sold changes placement in data
    #split data into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(Data1.drop("Price", axis=1), Data1['Price'], test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test,Data
def main(data):
    #make data frame from existing data
    PkmnData = data
    #enter name and
    #subset data 
    while True:
        #Forecast pokemon data
        PkmnData1 = PkmnData
        #clean data and split data
        X_train, X_test, y_train, y_test,Data = clean_data(PkmnData1)
        #print(X_train.head())
        #run model
        card_data = Model_1_RF(X_train,y_train,X_test,y_test)
        #write to excel file 
        #card_data['name'] = PkmnData['name'].unique()
        #Market_Price_Forecast(card_data)
        #print(f"{name} \nForecasted Prices: {card_data}")
        return card_data 
if __name__ == "__main__": 
    main()
