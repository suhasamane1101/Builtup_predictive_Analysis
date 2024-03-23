import pickle
from flask import Flask,request,jsonify,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

## import ridge regressor model and standard scaler pickle file
ridge_model=pickle.load(open('/config/workspace/prediction_maintainance_ml/rf_model.pkl','rb'))
standard_scaler=pickle.load(open('/config/workspace/prediction_maintainance_ml/st_scaler.pkl','rb'))

##Route for home page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predictdata',methods=['GET','POST'])
def predictdata():
    if request.method=='POST':
        UDI	=float(request.form.get('UDI'))
        Air_Temp= float(request.form.get('Air_Temp'))
        Process_temperature= float(request.form.get('Process_temperature'))
        Ratational_speed= float(request.form.get('Ratational_speed'))
        Torque = float(request.form.get('Torque'))
        Tool_wear = float(request.form.get('Tool_wear'))

        new_data_scaled=standard_scaler.transform([[UDI,Air_Temp,Process_temperature,Ratational_speed,Torque,Tool_wear]])
        result=ridge_model.predict(new_data_scaled)
        if(result>0.00 and result<=0.25):
            text="The Condition of Equipment is Best Check after 10 days."
        elif(result>0.25 and result<=0.50):
            text="The Condition of Equipment is good Check after 5 days."
        elif(result>0.50 and result<=0.75):
            text="The Condition of Equipment is not good need to maintainance."
        elif(result>0.75 and result<=1.00):
            text="The Condition of Equipment is not good need to maintainance."
            
        return render_template('index.html',result=result[0],text=text)
    else:
        return render_template('index.html')

@ app.route('/view_one')
def view_one():
    title = 'Motor'
    return render_template('view.html', title=title)

@ app.route('/view_two')
def view_two():
    title = 'Pump'
    return render_template('view2.html', title=title)

@ app.route('/view_three')
def view_three():
    title = 'Turbine'
    return render_template('view3.html', title=title)


@ app.route('/Maintenance_scheduler')
def Maintenance_scheduler():
    title = 'Maintenance_scheduler'
    return render_template('maintaince.html', title=title)

@ app.route('/help')
def help():
    title = 'Help'
    return render_template('https://bot.dialogflow.com/bee4be66-a4c0-417f-90f8-3a96f51ca69f', title=title)

@ app.route('/feedback')
def feedback():
    title = 'Feedback'
    return render_template('feedback.html', title=title)




if __name__=="__main__":
    app.run(host="0.0.0.0")
