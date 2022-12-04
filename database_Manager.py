import mysql.connector


database_host="162.241.148.163"
database_user="mbnselty_macquire_fields"
database_password="-9MgO8skHu57"

def Database_Verify(name):
    mydb = mysql.connector.connect(
    host=database_host,
    user=database_user,
    password=database_password
    )

    mycursor=mydb.cursor()

    mycursor.execute("SHOW DATABASES")
    b=True
    for x in list(mycursor):
        if str(x[0]) == name:
            b=False
    if b == True:
        mycursor.execute(f"CREATE DATABASE {name}")
        
def Table_Verify(Database,name,Query):
    mydb = mysql.connector.connect(
    host=database_host,
    user=database_user,
    password=database_password,
    database=Database
    )

    mycursor=mydb.cursor()

    mycursor.execute("SHOW TABLES")


    b=True
    for x in mycursor:
        if str(x[0]) == name:
            b=False
    if b == True:
        mycursor.execute(Query)
    
def execute_Query(Database,Query,params):
    mydb = mysql.connector.connect(
    host=database_host,
    user=database_user,
    password=database_password,
    database=Database
    )

    mycursor=mydb.cursor()

    mycursor.execute(Query,params)
    mydb.commit()

def Fetch_Query(Database,Query):
    mydb = mysql.connector.connect(
    host=database_host,
    user=database_user,
    password=database_password,
    database=Database
    )

    mycursor=mydb.cursor()

    mycursor.execute(Query)
    return mycursor.fetchall()




