from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

import pickle
import pandas as pd
import os
import numpy as np
from sklearn.externals import joblib

# Preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = joblib.load(os.path.join(cur_dir,
            'pkl_objects/heart_classifier.pkl'))

clf1 = joblib.load(os.path.join(cur_dir,
            'pkl_objects/disease_classifier.pkl'))
 

app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('select.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/results')
def do_something1():
    return render_template('index.html')
@app.route('/results1')
def do_something2():
    return render_template('index2.html')
@app.route('/results2')
def do_something3():
    return render_template('index1.html')


@app.route('/heart', methods=['POST'])
def predict():

    Age = int(request.form['Age'])
    Sex = int(request.form['Sex'])
    Chest = int(request.form['Chest'])
    BP = int(request.form['BP'])
    Serum = int(request.form['Serum'])
    FBP = int(request.form['FBP'])
    ECG = int(request.form['ECG'])
    heartrate = int(request.form['heartrate'])
    induced = int(request.form['induced'])
    depression = int(request.form['depression'])
    vessels = int(request.form['vessels'])
    segmen = int(request.form['segmen'])
    thallium = int(request.form['thallium'])
    
    input_data = [{'Age': Age, 'Sex': Sex, 'Chest': Chest, 'BP': BP, 'Serum': Serum, 'FBP': FBP, 'ECG': ECG ,'heartrate': heartrate, 'induced': induced,'depression':depression,'vessels':vessels,'segmen':segmen,'thallium':thallium}]
    data = pd.DataFrame(input_data)
    label = {0: 'No heart Disease', 1: 'Heart Disease'}
    logreg = clf.predict(data)[0]
    resfinal = label[logreg]
    return render_template('heart.html', res=resfinal)
    
@app.route('/symptom', methods=['POST'])
def predict2():

    Abdomen_acute = int(request.form['Abdomen_acute'])
    Abdominal_tenderness = int(request.form['Abdominal_tenderness'])
    Abnormally_hard_consistency = int(request.form['Abnormally_hard_consistency'])
    Abortion= int(request.form['Abortion'])
    Abscess_bacterial = int(request.form['Abscess_bacterial'])
    Absences_finding = int(request.form['Absences_finding'])
    Achalasia = int(request.form['Achalasia'])
    Agitation = int(request.form['Agitation'])
    Air_fluid_level = int(request.form['Air_fluid_level'])
    
    input_data = [{'Abdomen acute': Abdomen_acute, 'Abdominal tenderness': Abdominal_tenderness, 'Abnormally hard consistency':Abnormally_hard_consistency, 'Abortion': Abortion, 'Abscess bacterial':Abscess_bacterial, 'Absences finding':Absences_finding, 'Achalasia':Achalasia, 'Agitation': Agitation, 'Air fluid level': Air_fluid_level}]
    data = pd.DataFrame(input_data)
    print(data)
    logreg = clf1.predict(data)[0]
    print(logreg)
    resfinal = logreg
    return render_template('symptom.html', result=resfinal)
    
@app.route('/diet', methods=['POST'])
def predict1():
    Height_feet = int(request.form.get('Height1'))
    Height_inches = int(request.form.get('Height2'))
    Weight = int(request.form.get('Weight'))
    totalHeight = (12 * Height_feet) + Height_inches
    bmi = Weight * 703 / (totalHeight * totalHeight)

    if bmi < 18.5:
        BMIStatus = """You are Underweight. Foods that should be included every day:
1. Full-cream milk: 750 - 1000 ml (3 to 4 cups)\n
2. Meat, fish, eggs and other protein foods: 3-5 servings (90 to 150 g)\n
3. Bread and cereals: 8-12 servings (e.g. up to 6 cups of starch a day)\n
4. Fruit and vegetables: 3-5 servings\n
5. Fats and oils: 90 g (6 tablespoons)\n
6. Healthy desserts: 1-2 servings\n"""
    elif bmi < 24.9:
        BMIStatus= """You are Normal. Current diet plan is ok."""
    elif bmi < 29.9:
        BMIStatus = """You are Overweight.\n
1. Increase The Consumption Of Fruits And Vegetables\n
2. Limit The Intake Of Stimulants such as caffeine, alcohol, and refined sugar.\n
3. Do Not Skip Breakfast as is the most important meal of the day\n
4. Drink Plenty Of Water\n
5. Have Smaller Gaps Between The Meals\n
6. Do Not Starve\n
7. Restrict Your Calorie Intake\n
8. Remove Fat From Your Food\n
9. Eat Healthy Snacks\n"""
    else:
        BMIStatus = """You are Obese. Diet plan as follows:\n
            1. Cut your caloric intake by about 500 to 1,000 calories a day.\n
            2. Restrict carbohydrates -- particularly high-glycemic varieties that affect your blood sugar\n
            3. Cut back on portions to eat less food and balance your caloric intake.\n
            4. Combine Diet with Exercise\n"""
    
    print(BMIStatus)

    return render_template('diet.html', rs=BMIStatus)

    
	
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)