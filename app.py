
from flask import Flask,render_template,request,session



import Handler
import My_Functions



#mq=Handler.Macquarie(6,"13-04-13","13:12","12345","Sohail","No","BUR","","","Ali")
#mq.Insert()
#mq.Delete()
#mq.Update()



app=Flask(__name__)

app.secret_key = '18D1D6E8AFC81ED518DE9D69A953'


@app.route("/",methods=['GET'])
def index():
    try:
        print(session["Logged_In"])
    except:
        session["Logged_In"]=False
        session["data"]={
            "message":"",
            "user":{
                "Id":0,
                "name":"",
                "user_name":"",
                "user_password":""
            }
            
        }
    
    session["data"]["message"]=""
    if(session["Logged_In"]):
        session["data"]["form_data"]={
        "registration":"",
        "vehicle":"",
        "visitor":"",
        "destination":""
        }
        session["data"]["data"]=Handler.Macquarie({}).Fetch_Data()
        return render_template("macquarie.html",data=session["data"])
    return render_template("index.html",data=session["data"])

@app.route("/",methods=['POST'])
def index_Post():
    session["data"]["form_data"]={
        "registration":"",
        "vehicle":"",
        "visitor":"",
        "destination":""
    }
    if "login_page" in request.form:
        return My_Functions.User_Login(request)
    elif "logout_page" in request.form:
        return My_Functions.User_Logout(request)
    elif "logout_refresh_page" in request.form:
        return My_Functions.Macquarie_Refresh(request)
    elif "management_page" in request.form:
        return My_Functions.Management_Page(request)
    return render_template("index.html",data=session["data"])

@app.route("/admin")
def admin():
    user=Handler.User(-1,"","","")
    data=user.Fetch_Data()
    return render_template("admin.html",data=data)

@app.route("/user")
def user():
    return render_template("user.html")

@app.route('/user/api',methods=['GET'])
def get_User_login():
    user_name=""
    user_password=""
    if 'user_name' and 'user_password' in request.args:
        user_name = request.args['user_name']
        user_password = request.args['user_password']
    else:
        return "null"
    user=Handler.User(-1,"",user_name,user_password)
    return user.search()



@app.route('/user/insert/api',methods=['GET'])
def Insert_User():
    _name=""
    _user_name=""
    _user_password=""
    if 'name' and 'user_name' and 'user_password' in request.args:
        _name = request.args['name']
        _user_name = request.args['user_name']
        _user_password = request.args['user_password']
    else:
        return {"Response":"Incorrect Data"}
    user=Handler.User(-1,_name,_user_name,_user_password)
    return user.Insert()






@app.route('/user/update/api',methods=['GET'])
def Update_User():
    _id=-1
    _name=""
    _user_name=""
    _user_password=""
    if 'id' and 'name' and 'user_name' and 'user_password' in request.args:
        _id = request.args['id']
        _name = request.args['name']
        _user_name = request.args['user_name']
        _user_password = request.args['user_password']
    else:
        return {"Response":"Incorrect Data"}
    user=Handler.User(_id,_name,_user_name,_user_password)
    return user.Update()







@app.route('/user/delete/api',methods=['GET'])
def Delete_User():
    _id=-1
    if 'id' in request.args:
        _id = request.args['id']
    else:
        return {"Response":"Incorrect Data"}
    user=Handler.User(_id,"","","")
    return user.Delete()







    

@app.route('/admin/api',methods=['GET'])
def get_Admin_login():
    user_name=""
    user_password=""
    if 'user_name' and 'user_password' in request.args:
        user_name = request.args['user_name']
        user_password = request.args['user_password']
    else:
        return "null"
    admin=Handler.Admin(-1,"","","",user_name,user_password)
    return admin.search()







if __name__ == "__main__":
    
    app.run(debug=False,host='0.0.0.0')