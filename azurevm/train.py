import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = pd.read_csv("train.csv")
data = data.drop(data.columns[[0, 3, 6, 7, 8, 9, 10]], axis=1)
data = data.dropna()
data = pd.get_dummies(data=data, columns=['Sex','Pclass','Embarked'])
X = data.drop("Survived", axis=1)
y = data['Survived']
regressor = LinearRegression()
regressor.fit(X, y)
joblib.dump(regressor, "linear_regression_model.joblib")