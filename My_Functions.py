from flask import Flask,render_template,request,session
import datetime

import Handler


def User_Login(request):
    session["data"]={

    }

    user_name=request.form["user_name"]
    user_password=request.form["user_password"]
    user=Handler.User(-1,"",user_name,user_password)

    session["data"]["message"]="Invalid Username Password"

    users=user.search()
    if (users["Data"]==[]):
        return render_template("index.html",data=session["data"])
    temp_user=users["Data"][0]
    session["data"]["user"]={"id":temp_user["id"],"name":temp_user["name"],"user_name":temp_user["user_name"],"user_password":temp_user["user_password"]}
    session["data"]["data"]=Handler.Macquarie({}).Fetch_Data()

    if "save_password" in request.form:
        session["Logged_In"]=True
    session["data"]["message"]=""
    session["data"]["form_data"]={
        "id":0,
        "registration":"",
        "vehicle":"",
        "visitor":"",
        "destination":""
    }
    return render_template("macquarie.html",data=session["data"])

def User_Logout(request):
    session["data"]["message"]=""
    session["Logged_In"]=False
    return render_template("index.html",data=session["data"])


def Macquarie_Refresh(request):
    if request.form["search"]=="":
        session["data"]["data"]=Handler.Macquarie({}).Fetch_Data()
    else:
        session["data"]["data"]=Handler.Macquarie({}).Fetch_Data_Search(request.form["search"])
    session["data"]["search"]=request.form["search"]
    
    return render_template("macquarie.html",data=session["data"])

def Management_Page(request):
    form_data_=request.form.to_dict()
    form_data_["Updater_Name"]=session["data"]["user"]["name"]
    mac=Handler.Macquarie(form_data_)
    session["data"]["message"]=""
    session["data"]["search"]=""
    if "Save" in request.form:
        response=mac.Save()
        if(response["OK"]==True):
            session["data"]["message"] = response["msg"]
            session["data"]["form_data"]={
                    "id":0,
                    "registration":"",
                    "vehicle":"",
                    "visitor":"",
                    "destination":""
                }
        else:
            session["data"]["form_data"]={
                    "id":0,
                    "registration":request.form["Registration"],
                    "vehicle":request.form["Vehicle_Type"],
                    "visitor":request.form["Visitor_Type"],
                    "destination":request.form["Destination"]
                }
        session["data"]["message"] = response["msg"]
        session["data"]["data"]=Handler.Macquarie({}).Fetch_Data()
            
    elif "Delete" in request.form:
        response=mac.Delete()
        if(response["OK"]==True):
            session["data"]["message"] = response["msg"]
            session["data"]["form_data"]={
                    "id":0,
                    "registration":"",
                    "vehicle":"",
                    "visitor":"",
                    "destination":""
                }
        else:
            session["data"]["form_data"]={
                    "id":0,
                    "registration":request.form["Registration"],
                    "vehicle":request.form["Vehicle_Type"],
                    "visitor":request.form["Visitor_Type"],
                    "destination":request.form["Destination"]
                }
        session["data"]["message"] = response["msg"]
        session["data"]["data"]=Handler.Macquarie({}).Fetch_Data()
        
    elif "Clear" in request.form:
        session["data"]["message"]=""
        session["data"]["data"]=Handler.Macquarie({}).Fetch_Data()
    elif "Find" in request.form:
        if request.form["Registration"] == "":
            session["data"]["message"]="Please Enter Registration"
            session["data"]["form_data"]={
                    "id":0,
                    "Registration":"",
                    "Vehicle_Type":"",
                    "Visitor_Type":"",
                    "Destination":""
                }
        else:
            find_data=mac.Fetch_Data_Registration()
            if find_data == 0:
                print("Not Found")
                session["data"]["form_data"]={
                    "id":0,
                    "registration":request.form["Registration"],
                    "vehicle":"",
                    "visitor":"",
                    "destination":""
                }
            else:
                session["data"]["form_data"]={
                    "id":0,
                    "registration":find_data["Registration"],
                    "vehicle":find_data["Vehicle_Type"],
                    "visitor":find_data["Visitor_Type"],
                    "destination":find_data["Destination"]
                }
        session["data"]["message"]=""
        session["data"]["data"]=mac.Fetch_Data()
    return render_template("macquarie.html",data=session["data"])