import os
import patoolib
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nalam !@#!",
    database="database"
)

mycursor = mydb.cursor()
mycursor.execute("INSERT INTO `inaequo.teacher_board` (`name`, created_on)")
print("Success")