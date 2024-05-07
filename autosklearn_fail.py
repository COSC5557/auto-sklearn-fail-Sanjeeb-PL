# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HbgxA3ey6f2qxnccM5gtWnCOotIYo3gV
"""

# this code was done in google colab. So following lines of code used for installting libraries
!pip install scikit-learn==0.24.2 --no-build-isolation
!pip install auto-sklearn

# importing necessary libraries
import autosklearn.classification
from autosklearn.metrics import accuracy, f1, roc_auc, precision, average_precision, recall, log_loss
import sklearn.model_selection
from sklearn.datasets import fetch_openml
import sklearn.metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_predict

# Fetching data from data_id, as dataframe and store input data in X and target in y
X, y = fetch_openml(data_id=40691, as_frame=True, return_X_y=True)

enc = OneHotEncoder(handle_unknown='ignore')
X = enc.fit_transform(X)

# splitting the data fetched using train_test_split into training and test data sets
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, random_state=42)

# defining classifier for RandomForestClassifier and training the model
classifier = RandomForestClassifier(random_state=42)
classifier .fit(X_train, y_train)

# predicting the target value for RF
y_pred_rf = classifier .predict(X_test)
rf_accuracy = sklearn.metrics.accuracy_score(y_test, y_pred_rf)
print("RF Accuracy:", rf_accuracy)

# importing autosklearn classifier
from autosklearn.classification import AutoSklearnClassifier

automl = AutoSklearnClassifier(time_left_for_this_task=200)
automl.fit(X_train, y_train)

# predicting the target value for training and test to check the accuracy score
y_train_pred_automl = automl.predict(X_train)
y_test_pred_automl = automl.predict(X_test)

print("Training Accuracy of automl without CV:", sklearn.metrics.accuracy_score(y_train, y_train_pred_automl))
print("Test Accuracy of automl without CV:", sklearn.metrics.accuracy_score(y_test, y_test_pred_automl))

# defining the classifier now with time for 200 and cv = 2
automl = AutoSklearnClassifier(time_left_for_this_task=200, resampling_strategy='cv', resampling_strategy_arguments={'folds': 2})
automl.fit(X_train, y_train)

y_pred_automl = automl.predict(X_test)
y_train_automl = cross_val_predict(automl, X_train, y_train, cv=3)
automl_train_accuracy = sklearn.metrics.accuracy_score(y_train, y_train_automl)

print("AutoML Training Accuracy with CV:", automl_train_accuracy)
print("AutoML Accuracy with CV:", sklearn.metrics.accuracy_score(y_test, y_pred_automl))

print(automl.show_models())