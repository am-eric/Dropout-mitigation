from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from website.choices import encoded_choices
import pandas as pd
# import joblib
import pickle

views = Blueprint('views', __name__)

# Load your XGBoost model
# loading the pre-trained model
model = pickle.load(open('XGBOOST.pkl',  "rb"))

# Function to convert grade to Portuguese scale
def convert_grade_to_portuguese_scale(grade, min_grade, max_grade):
    return ((grade - min_grade) / (max_grade - min_grade)) * 10 + 10

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)




@views.route('/get-started', methods=['GET', 'POST'])
@login_required
def get_started():
    data = {}

    if request.method == 'POST':
        data['Marital status'] = int(request.form.get('Marital status', ))
        data['Application order'] = int(request.form.get('Application order', ))
        data['Course'] = int(request.form.get('Course', ))
        data['Daytime/evening attendance'] = int(request.form.get('Daytime/evening attendance', 0))
        data['Previous qualification'] = int(request.form.get('Previous qualification', ))
        data["Mother's occupation"] = int(request.form.get("Mother's occupation", ))
        data["Father's occupation"] = int(request.form.get("Father's occupation", ))
        data['Displaced'] = int(request.form.get('Displaced', ))
        data['Debtor'] = int(request.form.get('Debtor', ))
        data['Tuition fees upto date'] = int(request.form.get('Tuition fees upto date', 0))
        data['Gender'] = int(request.form.get('Gender', ))
        data['Scholarship holder'] = int(request.form.get('Scholarship holder', ))
        data['Age'] = int(request.form.get('Age', ))
        data['Curricular units 1st sem (credited)'] = int(request.form.get('Curricular units 1st sem (credited)', ))
        data['Curricular units 1nd sem (enrolled)'] = int(request.form.get('Curricular units 1nd sem (enrolled)', ))
        data['Curricular units 1nd sem (evaluations)'] = int(request.form.get('Curricular units 1nd sem (evaluations)', ))
        data['Curricular units 1nd sem (approved)'] = int(request.form.get('Curricular units 1nd sem (approved)', ))
        # Convert grade to Portuguese scale
        grade = float(request.form.get('Curricular units 1nd sem (grade)', 0))
        min_grade = 0  # Minimum passing grade in the foreign classification scale
        max_grade = 100  # Highest mark in the foreign classification scale

        converted_grade = convert_grade_to_portuguese_scale(grade, min_grade, max_grade)
        data['Curricular units 1nd sem (grade)'] = converted_grade

        data['Curricular units 2st sem (credited)'] = int(request.form.get('Curricular units 2st sem (credited)', ))
        data['Curricular units 2nd sem (enrolled)'] = int(request.form.get('Curricular units 2nd sem (enrolled)', ))
        data['Curricular units 2nd sem (evaluations)'] = int(request.form.get('Curricular units 2nd sem (evaluations)', ))
        data['Curricular units 2nd sem (approved)'] = int(request.form.get('Curricular units 2nd sem (approved)', ))
        grade = float(request.form.get('Curricular units 2nd sem (grade)', ))
        min_grade = 0  # Minimum passing grade in the foreign classification scale
        max_grade = 100  # Highest mark in the foreign classification scale

        converted_grade = convert_grade_to_portuguese_scale(grade, min_grade, max_grade)
        data['Curricular units 2nd sem (grade)'] = converted_grade
        data['Curricular units 2nd sem (without evalutions)'] = int(request.form.get('Curricular units 2nd sem (without evalutions)', ))

        #print(data)
        # Prepare the input data for prediction
        input_data = pd.DataFrame(data, index=[0])
        # Print individual column types
        for col in input_data.columns:  
            print(f'{col}: {input_data[col].dtype}')

        #print(input_data.columns)
        #print(input_data.dtypes)



    
        #get columns from model used in training.  
        input_data.columns = model.feature_names_in_

        #Make predictions
        predictions = model.predict(input_data)
        # Map the predicted values back to the original classes
        predicted_class = ['Dropout', 'Enrolled', 'Graduate'][int(predictions[0])]
        flash(f"Predicted class: {predicted_class}")
    #predictions = model.predict(input_data)
    
        
    return render_template("get_started.html", user=current_user, encoded_choices=encoded_choices, )


@views.route('/support')
@login_required
def support():
    return render_template("support.html", user=current_user)

