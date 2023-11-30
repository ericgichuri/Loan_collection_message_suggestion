from flask import Flask,render_template,redirect,url_for,request,jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn import preprocessing
import random

app=Flask(__name__)

# load model
with open('model_pickle','rb') as f:
    model=pickle.load(f)

# function predict status
def predict(overdue_days,paid_percentage,times_borrowed):
    new_data={'overdue_days':[int(overdue_days)],
          'paid_percentage':[float(paid_percentage)],
          'no_of_times_borrowed':[int(times_borrowed)]}
    new_df=pd.DataFrame(new_data)
    new_df_norm=preprocessing.normalize(new_df,norm='l1')
    pred=model.predict(new_df_norm)
    return pred[0]

# function select messages
def suggest_messages(status):
    all_messages=[
        "Hello [Client], a gentle reminder about your pending payment. If settling the full amount is challenging, consider making a partial payment to keep your account in good standing. Thank you.",
        "Dear [Client], we understand financial challenges. To ease the burden, you can make a partial payment now. Log in to your account or contact us for assistance. Appreciate your cooperation.",
        "Hi [Client], facing difficulty with the full payment? You have the option to make a partial payment now. Visit our website or call our support team for a personalized solution. Thank you.",
        "Dear borrower, we acknowledge your efforts. If the full payment is not feasible, consider a partial payment to keep your account on track. Visit our website or contact us for guidance.",
        "Hello [Client], considering a partial payment? It's a step toward resolving your outstanding balance. Log in to your account or contact us to discuss a partial payment plan. Thank you.",
        "Dear [Client], if the full payment is challenging, you can still take a positive step by making a partial payment today. Explore options on our website or call us for assistance. Thank you.",
        "Hi [Client], struggling with the full amount? Making a partial payment now is a positive move. Log in to your account or contact us to discuss available options. Appreciate your cooperation.",
        "Dear borrower, we recognize your effort to address your payment. Consider making a partial payment today to ease the financial burden. Visit our website or call for assistance. Thank you.",
        "Hello [Client], we're here to help. If a full payment is not possible, making a partial payment is a positive step. Log in to your account or contact us for guidance. Appreciate your cooperation.",
        "Dear [Client], we appreciate your willingness to address your payment. If the full amount is challenging, consider making a partial payment today. Visit our website or call for assistance. Thank you.",
    ]
    partial_messages=[
        "Hello [Client], a gentle reminder about your pending payment. If settling the full amount is challenging, consider making a partial payment to keep your account in good standing. Thank you.",
        "Dear [Client], we understand financial challenges. To ease the burden, you can make a partial payment now. Log in to your account or contact us for assistance. Appreciate your cooperation.",
        "Hi [Client], facing difficulty with the full payment? You have the option to make a partial payment now. Visit our website or call our support team for a personalized solution. Thank you.",
        "Dear borrower, we acknowledge your efforts. If the full payment is not feasible, consider a partial payment to keep your account on track. Visit our website or contact us for guidance.",
        "Hello [Client], considering a partial payment? It's a step toward resolving your outstanding balance. Log in to your account or contact us to discuss a partial payment plan. Thank you.",
        "Dear [Client], if the full payment is challenging, you can still take a positive step by making a partial payment today. Explore options on our website or call us for assistance. Thank you.",
        "Hi [Client], struggling with the full amount? Making a partial payment now is a positive move. Log in to your account or contact us to discuss available options. Appreciate your cooperation.",
        "Dear borrower, we recognize your effort to address your payment. Consider making a partial payment today to ease the financial burden. Visit our website or call for assistance. Thank you.",
        "Hello [Client], we're here to help. If a full payment is not possible, making a partial payment is a positive step. Log in to your account or contact us for guidance. Appreciate your cooperation.",
        "Dear [Client], we appreciate your willingness to address your payment. If the full amount is challenging, consider making a partial payment today. Visit our website or call for assistance. Thank you."
    ]
    not_paid_messages=[
        "Dear [Client], it has come to our attention that your account reflects no payments. Let's work together to address this. Contact us to discuss a plan tailored to your situation. Thank you.",
        "Hello [Client], we've noticed no payments on your account. Your commitment to resolving this matter is crucial. Please call us or visit our office to discuss a repayment plan. Thank you.",
        "Dear [Client], it appears there have been no payments on your account. We're here to assist. Contact us to explore options for settling your overdue balance. Thank you.",
        "Hi [Client], your account shows no payments. Resolving this is important. Please reach out to us to discuss a suitable plan and avoid further consequences. Thank you.",
        "Dear borrower, our records indicate no payments on your account. Let's work together to find a resolution. Contact us to discuss a plan tailored to your current situation. Thank you.",
        "Hello [Client], it's been a while since we received any payments on your account. Your prompt attention to this matter is appreciated. Contact us to discuss repayment options. Thank you.",
        "Dear [Client], your account reflects no payments. We're here to help you address this situation. Please contact us to discuss a plan that suits your current circumstances. Thank you.",
        "Hi [Client], it's important to address the absence of payments on your account. Contact us to explore options for settling your overdue balance. We're here to assist. Thank you.",
        "Dear [Client], no payments have been recorded on your account. Let's work together to find a resolution. Please reach out to discuss a repayment plan. Thank you.",
        "Hello [Client], it's concerning that there have been no payments on your account. We're committed to helping you resolve this. Contact us to discuss a plan tailored to your situation. Thank you."
    ]
    default_messages=[
        "Dear [Client], your account reflects a significant overdue balance of all those days. We understand challenges may arise. Let's discuss a resolution. Please call or visit our office. Thank you.",
        "Hello [Client], your account is now [write days] days overdue. We're here to assist in finding a solution. Contact us to discuss a repayment plan tailored to your situation. Thank you.",
        "Dear [Client], it has been [write days] days since your last payment. We're eager to help you resolve this matter. Please reach out to our team to discuss a suitable plan. Thank you.",
        "Hi [Client], we've noticed your account is severely overdue, with [write days] days unpaid. Let's work together to find a resolution. Contact us today to discuss your options. Thank you.",
        "Dear borrower, your account shows a prolonged default of some days. We're committed to assisting you. Contact us to explore options for settling your overdue balance. Thank you.",
        "Hello [Client], your account has been overdue for [write days] days. It's essential to address this promptly. Please contact us to discuss repayment options and avoid further escalation. Thank you.",
        "Dear [Client], your account is in significant arrears, with [write days] days overdue. We're here to help you find a resolution. Kindly get in touch with our team at your earliest convenience. Thank you.",
        "Hi [Client], it's been [write days] days since your last payment. We understand challenges may arise. Let's work together to find a solution. Please contact us to discuss repayment options. Thank you.",
        "Dear [Client], your account is seriously overdue, with [write days] days unpaid. We're committed to resolving this matter. Contact us to discuss a plan that suits your current situation. Thank you.",
        "Hello [Client], your account is [write days] days overdue. We're here to assist you in resolving this matter. Please contact us to discuss a customized repayment plan. Thank you."
    ]
    # message wrapper
    data=[]

    # message 1    
    message1=random.choice(all_messages)

    #message 2
    if status.lower()=="partial":
        message2=random.choice(partial_messages)
    elif status.lower()=="not_paid":
        message2=random.choice(not_paid_messages)
    elif status.lower()=="defualt":
        message2=random.choice(default_messages)
    else:
        message2=random.choice(not_paid_messages)
    
    # append in data
    data.append(message1)
    data.append(message2)

    return jsonify({"msg":"1","data":data})

# route index
@app.route("/")
@app.route("/home")
def func():
    return render_template("index.html")

# route suggest
@app.route("/suggest",methods=["POST"])
def suggest_message():
    if request.method=="POST":
        data=[]
        msg=""
        overdue_days=request.form['overdue_days']
        paid_amount=request.form['paid_amount']
        loan_balance=request.form['loan_balance']
        times_borrowed=request.form['no_of_times_borrowed']
        if overdue_days=="" or paid_amount=="" or loan_balance=="" or times_borrowed=="":
            msg="Every field must be filled"
        else:
            try:
                paid_percentage=(((int(paid_amount)+int(loan_balance))-int(loan_balance))/(int(paid_amount)+int(loan_balance)))*100
                predicted_status=predict(overdue_days,paid_percentage,times_borrowed)
                data=suggest_messages(predicted_status)
                return data
            except Exception as e:
                msg=str(e)

        return jsonify({"msg":msg,"data":data})

if '__main__'==__name__:
    app.run(debug=True)