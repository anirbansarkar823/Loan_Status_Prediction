# -*- coding: utf-8 -*-
"""LoanStatusPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jJm9-YsbuVlo7KosFCrxl-U99zY7mVNl
"""

# importing all the libraries
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

# Data collection and processing
loan_dataset = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/train_u6lujuX_CVtuZ9i (1).csv')
loan_dataset.head()

# Credit_History --> 1 means good credit history; 0 means poor credit history

loan_dataset.shape

# descriptive data
loan_dataset.describe()

loan_dataset.describe(include=['O'])

# to find if there is null values
loan_dataset.info()

loan_dataset.isnull().sum()

# filling the missing values for numerical terms with respective column 'mean'
loan_dataset['LoanAmount'] = loan_dataset['LoanAmount'].fillna(loan_dataset['LoanAmount'].mean())
loan_dataset['Loan_Amount_Term'] = loan_dataset['Loan_Amount_Term'].fillna(loan_dataset['Loan_Amount_Term'].mean())
loan_dataset['Credit_History'] = loan_dataset['Credit_History'].fillna(loan_dataset['Credit_History'].mode()[0]) # as only 0 and 1 values are there

loan_dataset['Gender'] = loan_dataset['Gender'].fillna(loan_dataset['Gender'].mode()[0])
loan_dataset['Married'] = loan_dataset['Married'].fillna(loan_dataset['Married'].mode()[0])
loan_dataset['Dependents'] = loan_dataset['Dependents'].fillna(loan_dataset['Dependents'].mode()[0])
loan_dataset['Self_Employed'] = loan_dataset['Self_Employed'].fillna(loan_dataset['Self_Employed'].mode()[0])

loan_dataset.isnull().sum()

loan_dataset.Loan_Status.unique()

# label encoding
loan_dataset.Loan_Status.replace({'N':0,'Y':1}, inplace=True)

loan_dataset.Loan_Status.unique()

# dependant column values
loan_dataset['Dependents'].value_counts()

# replacing the values of 3+ to a value higher than 3, to tranform the datatype of column "Dependents"
loan_dataset.Dependents = loan_dataset.Dependents.replace({'3+':4})
# loan_dataset = loan_dataset.replace(to_replace='3+', value=4)

# checking if the changes has taken place
loan_dataset['Dependents'].value_counts()

loan_dataset.Dependents = loan_dataset.Dependents.astype('int64')
loan_dataset.info()

"""### Data Visualization"""

# Education vs Loan_Status
import seaborn as sns
sns.countplot(x='Education', hue='Loan_Status', data=loan_dataset)
# 0 - loan didn't got approved
# 1 - loan approved

# more loan approvals for graduated people

# Marital status vs loan status
sns.countplot(x='Married', hue='Loan_Status', data=loan_dataset)

# Inference: Married people are getting more loan approvals

# Gender vs loan status
sns.countplot(x='Gender', hue='Loan_Status', data=loan_dataset)

# Inference: Male people are getting more loan approvals

# Self_Employed vs loan status
sns.countplot(x='Self_Employed', hue='Loan_Status', data=loan_dataset)

# Inference: Employed (not Self_Employed) people are getting more loan approvals

# Property_Area vs loan status
sns.countplot(x='Property_Area', hue='Loan_Status', data=loan_dataset)

# Inference: all categories are getting almost equal oppurtunities

"""### Converting Categorical columns to Numerical Values"""

# we will use label encoding, as from above visualisation we can see one category has got more preference compared to the other for few columns
loan_dataset.replace({'Married':{'No':0,'Yes':1},'Gender':{'Male':1,'Female':0},'Self_Employed':{'No':1,'Yes':0},
                      'Property_Area':{'Rural':0,'Semiurban':1,'Urban':2},'Education':{'Graduate':1,'Not Graduate':0}},inplace=True)

loan_dataset.head()

loan_dataset.info()

X = loan_dataset.drop(columns=['Loan_ID', 'Loan_Status'], axis=1)
y = loan_dataset.Loan_Status

X.head()

# splitting the dataset into train and test data
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)
# stratified sampling, to distribute data proportionally

print(x_train.shape, x_test.shape, X.shape)

# we will use SVM classifier
classifier = svm.SVC(kernel='linear')

# training the SVM model
classifier.fit(x_train, y_train)

"""### Model Evaluation"""

# accuracy score on training data
x_train_prediction = classifier.predict(x_train)
train_data_accuracy = accuracy_score(x_train_prediction, y_train)
print(f"Accuracy on training data: {train_data_accuracy}")

# accuracy on train data
x_test_prediction = classifier.predict(x_test)
test_data_accuracy = accuracy_score(x_test_prediction, y_test)

print(f"Accuracy on test data: {test_data_accuracy}")

# as accuracy is high on both test and training data, so no overfitting