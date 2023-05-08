import mysql.connector
from django.shortcuts import render_to_response
import MySQLdb 


conection= mysql.connector.connect(user='root', 
host='localhost', port='3306', password='12345678')
myquery=conection.cursor()
myquery.execute("select something from data.table")

#for q in myquery:
    #results += q