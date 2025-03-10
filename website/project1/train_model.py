import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os


#Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load your dataset
data = pd.read_csv(os.path.join(current_dir, 'water_intake_data.csv'))

# Features and target variable
X = data[['weight', 'activity_level', 'temperature', 'age', 'gender']]
y = data['recommended_intake'] 

# Convert categorical variables to numeric
X = pd.get_dummies(X, columns=['activity_level', 'gender'], drop_first=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'water_intake_model.pkl')