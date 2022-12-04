
from database_Manager import Database_Verify
from database_Manager import Table_Verify
from database_Manager import execute_Query 
from database_Manager import Fetch_Query
from flask import session
import datetime


class My_Database:
    def __init__(self):
        self.my_DB="mbnselty_macquarie_field_database"
        self.admin_table="CREATE TABLE admin_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),email VARCHAR(255),phone VARCHAR(255), user_name VARCHAR(255), user_password VARCHAR(255))"
        self.user_table="CREATE TABLE user_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), user_name VARCHAR(255), user_password VARCHAR(255))"
        self.macquarie="CREATE TABLE `macquarie` ( `Id` INT NOT NULL AUTO_INCREMENT , `Date` VARCHAR(50) NOT NULL DEFAULT '' , `Time` VARCHAR(50) NOT NULL DEFAULT '' , `Registration` VARCHAR(50) NOT NULL DEFAULT '' , `Vehicle_Type` VARCHAR(50) NOT NULL DEFAULT '' , `Visitor_Type` VARCHAR(50) NOT NULL DEFAULT '' , `Destination` VARCHAR(50) NOT NULL DEFAULT '' , `Add_TimeStamp` VARCHAR(50) NOT NULL DEFAULT '' , `Update_TimeStamp` VARCHAR(50) NOT NULL DEFAULT '' , `Updater_Name` VARCHAR(50) NOT NULL DEFAULT '' , PRIMARY KEY (`Id`));"

        Database_Verify(self.my_DB)
        Table_Verify(self.my_DB,'admin_table',self.admin_table)
        Table_Verify(self.my_DB,'user_table',self.user_table)
        Table_Verify(self.my_DB,'macquarie',self.macquarie)


    def Save(self,Query,params):
        execute_Query(self.my_DB,Query,params)
    
    def Records(self,Query):
        return Fetch_Query(self.my_DB,Query)

my_Db=My_Database()


class Macquarie:
    def __init__(self,json_data):
        datetime_object = datetime.datetime.now()
        self.Date =str(datetime_object.date())
        self.Time=str(datetime_object.time()).split('.')[0]
        self.Add_TimeStamp=""
        self.Update_TimeStamp=""
        if "Updater_Name" in json_data:
            self.Updater_Name=json_data["Updater_Name"]
        else:
            self.Updater_Name=""
        if "Id" in json_data:
            self.Id=json_data["Id"]
        else:
            self.Id=0
        if "Registration" in json_data:
            self.Registration=json_data["Registration"]
        else:
            self.Registration=""
        if "Vehicle_Type" in json_data:
            self.Vehicle_Type=json_data["Vehicle_Type"]
        else:
            self.Vehicle_Type=""
        if "Visitor_Type" in json_data:
            self.Visitor_Type=json_data["Visitor_Type"]
        else:
            self.Visitor_Type=""
        if "Destination" in json_data:
            self.Destination=json_data["Destination"]
        else:
            self.Destination=""
            
            
            
        

    def Save(self):
        if(self.Check_Id()):
            return self.Update()
        else:
            return self.Insert()

    def Insert(self):
        if self.Registration=="" or self.Vehicle_Type=="" or self.Visitor_Type=="" or self.Destination=="":
            return {
                "OK":False,
                "msg":"Fields Can't Empity"
            }
        else:
            my_Db.Save(f"INSERT INTO `macquarie`(`Date`, `Time`, `Registration`, `Vehicle_Type`, `Visitor_Type`, `Destination`, `Updater_Name`,`Update_TimeStamp`,`Add_TimeStamp`) VALUES (%s,%s,%s,%s,%s,%s,%s,current_timestamp(),current_timestamp())",(self.Date,self.Time,self.Registration,self.Vehicle_Type,self.Visitor_Type,self.Destination,self.Updater_Name))
            return {
                "OK":False,
                "msg":"Data Inserted Successfully !!!"
            }
    
    def Update(self):
        if self.Registration=="" or self.Vehicle_Type=="" or self.Visitor_Type=="" or self.Destination=="":
            return {
                "OK":False,
                "msg":"Fields Can't Empity"
            }
        else:
            my_Db.Save(f"UPDATE `macquarie` SET `Date`=%s,`Time`=%s,`Registration`=%s,`Vehicle_Type`=%s,`Visitor_Type`=%s,`Destination`=%s,`Updater_Name`=%s,`Update_TimeStamp`=current_timestamp() WHERE `Id`={self.Id}",(self.Date,self.Time,self.Registration,self.Vehicle_Type,self.Visitor_Type,self.Destination,self.Updater_Name))
            self.age=2
            return {
                "OK":False,
                "msg":"Data Updated Successfully !!!"
            }

    def Delete(self):
        if self.Id=="" or self.Id==0:
            return {
                "OK":False,
                "msg":"Please Select ID"
            }
        else:
            my_Db.Save(f"DELETE FROM `macquarie` WHERE `Id`={self.Id};",(self.Id))
            return {
                "OK":False,
                "msg":"Data Deleted Successfully !!!"
            }

    def Fetch_Data(self):
        datetime_object = datetime.datetime.now()
        data = my_Db.Records("SELECT `Id`, `Date`, `Time`, `Registration`, `Vehicle_Type`, `Visitor_Type`, `Destination`, `Add_TimeStamp`, `Update_TimeStamp`, `Updater_Name` FROM `macquarie` WHERE `Date`='"+str(datetime_object.date())+"'")
        list=[]
        for x in data:
            _Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name=x
            list.append(self.Create_Json(_Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name))
        return list
    
    def Fetch_Data_Registration(self):
        data = my_Db.Records("SELECT `Id`, `Date`, `Time`, `Registration`, `Vehicle_Type`, `Visitor_Type`, `Destination`, `Add_TimeStamp`, `Update_TimeStamp`, `Updater_Name` FROM `macquarie`")
        list=[]
        for x in data:
            _Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name=x
            if str(_Registration).lower() == str(self.Registration).lower():
                list.append(self.Create_Json(_Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name))
        if len(list) == 0:
            return 0
        else:
            return list[-1]
    
    def Check_Id(self):
        if self.Id=="":
            return False
        data = my_Db.Records(f"SELECT `Id`, `Date`, `Time`, `Registration`, `Vehicle_Type`, `Visitor_Type`, `Destination`, `Add_TimeStamp`, `Update_TimeStamp`, `Updater_Name` FROM `macquarie` WHERE `Id`={self.Id};")
        list=[]
        for x in data:
            _Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name=x
            list.append(self.Create_Json(_Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name))
        if list==[]:
            return False
        else:
            return True
    
    def Create_Json(self,_Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name):
        return {
            "Id":_Id,
            "Date":_Date,
            "Time":_Time,
            "Registration":_Registration,
            "Vehicle_Type":_Vehicle_Type,
            "Visitor_Type":_Visitor_Type,
            "Destination":_Destination,
            "Add_TimeStamp":_Add_TimeStamp,
            "Update_TimeStamp":_Update_TimeStamp,
            "Updater_Name":_Updater_Name
        }

    def Fetch_Data_Search(self,search):
        data = my_Db.Records("SELECT `Id`, `Date`, `Time`, `Registration`, `Vehicle_Type`, `Visitor_Type`, `Destination`, `Add_TimeStamp`, `Update_TimeStamp`, `Updater_Name` FROM `macquarie`")
        list=[]
        for x in data:
            if self.search_(x,search):
                _Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name=x
                list.append(self.Create_Json(_Id,_Date,_Time,_Registration,_Vehicle_Type,_Visitor_Type,_Destination,_Add_TimeStamp,_Update_TimeStamp,_Updater_Name))
        return list
    
    def search_(self,x,search):
        for item in x:
            if str(item).lower().__contains__(str(search).lower()):
                return True
        return False



class Admin:
    def __init__(self,_id,_name,_email,_phone,_user_name,_user_password):
        self.id=_id
        self.name=_name
        self.email=_email
        self.phone=_phone
        self.user_name=_user_name
        self.user_password=_user_password
    
    def Insert(self):
        #my_Db.Save(f"INSERT INTO admin_table (name,email,phone,user_name,user_password) VALUES ('{self.name}','{self.email}','{self.phone}','{self.user_name}','{self.user_password}');")
        self.age=2
    
    
    def Delete(self):
        #my_Db.Save(f"DELETe FROM admin_table WHERE id={self.id}")
        self.age=2
    
    
    def Update(self):
        #my_Db.Save(f"UPDATE admin_table set name='{self.name}', email='{self.email}', phone='{self.phone}', user_name='{self.user_name}', user_password='{self.user_password}' WHERE id={self.id}")
        self.age=2
    
    
    def Fetch_Data(self):
        data = my_Db.Records("SELECT id,name,email,phone,user_name,user_password FROM admin_table")
        list=[]
        for x in data:
            _id,_name,_email,_phone,_user_name,_user_password=x
            list.append(Admin(_id,_name,_email,_phone,_user_name,_user_password))
        return list




    def search(self):
        data = my_Db.Records(f"SELECT id,name,email,phone,user_name,user_password FROM admin_table WHERE user_name='{self.user_name}' and user_password='{self.user_password}'")
        lst=[]
        for x in data:
            _id,_name,_email,_phone,_user_name,_user_password=x
            lst.append({"id":_id,"name":_name,"email":_email,"phone":_phone,"user_name":_user_name,"user_password":_user_password})
        return {"Data":lst}





class User:
    def __init__(self,_id,_name,_user_name,_user_password):
        self.id=_id
        self.name=_name
        self.user_name=_user_name
        self.user_password=_user_password




    def Insert(self):
        data = my_Db.Records(f"SELECT * FROM user_table WHERE name='{self.name}'")
        if len(data) != 0:
            return {"Response":"Name Already Exist"}
        data = my_Db.Records(f"SELECT * FROM user_table WHERE user_name='{self.user_name}'")
        if len(data) != 0:
            return {"Response":"User Name Already Exist"}
        data = my_Db.Records(f"SELECT * FROM user_table WHERE user_password='{self.user_password}'")
        if len(data) != 0:
            return {"Response":"User Password Already Exist"}
        my_Db.Save(f"INSERT INTO user_table (name,user_name,user_password) VALUES ('{self.name}','{self.user_name}','{self.user_password}')",())
        return {"Response":"Done"}
        self.age=2
    def Delete(self):
        my_Db.Save(f"DELETE FROM user_table WHERE id={self.id}")
        return {"Response":"Done"}





    def Update(self):
        data = my_Db.Records(f"SELECT * FROM user_table WHERE name='{self.name}' and id != {self.id}")
        if len(data) != 0:
            return {"Response":"Name Already Exist"}
        data = my_Db.Records(f"SELECT * FROM user_table WHERE user_name='{self.user_name}' and id != {self.id}")
        if len(data) != 0:
            return {"Response":"User Name Already Exist"}
        data = my_Db.Records(f"SELECT * FROM user_table WHERE user_password='{self.user_password}' and id != {self.id}")
        if len(data) != 0:
            return {"Response":"User Password Already Exist"}
        #my_Db.Save(f"UPDATE user_table set name='{self.name}', user_name='{self.user_name}', user_password='{self.user_password}' WHERE id={self.id}")
        return {"Response":"Done"}
    
    
    
    def Fetch_Data(self):
        data = my_Db.Records("SELECT id,name,user_name,user_password FROM user_table")
        lst=[]
        for x in data:
            _id,_name,_user_name,_user_password=x
            lst.append({"id":_id,"name":_name,"user_name":_user_name,"user_password":_user_password})
        return lst



    def search(self):
        data = my_Db.Records(f"SELECT id,name,user_name,user_password FROM user_table WHERE user_name='{self.user_name}' and user_password='{self.user_password}'")
        lst=[]
        for x in data:
            _id,_name,_user_name,_user_password=x
            lst.append({"id":_id,"name":_name,"user_name":_user_name,"user_password":_user_password})
        return {"Data":lst}
        






