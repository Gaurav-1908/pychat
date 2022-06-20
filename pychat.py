import os
from email import message
from django.dispatch import receiver
import mysql.connector
from datetime import date
from operator import add
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('PYCHAT_HOST'),
  user=os.getenv('PYCHAT_USER'),
  password=os.getenv('PYCHAT_PASSWORD'),
  database=os.getenv('PYCHAT_DATABASE')
)

def create(username,name):
    mycursor = mydb.cursor()
    sql = 'insert into users (username,name) values(%s, %s)'
    values = (username,name)
    mycursor.execute(sql,values)
    mydb.commit()
    mycursor.close()

def send(sender):
    mycursor = mydb.cursor()
    sql = 'select receiver from messages where sender = %s'
    values = (sender,)
    mycursor.execute(sql,values)
    users = mycursor.fetchall()
    sent = [row[0] for row in users]
    #print(sent)
    
    sql = 'select sender from messages where receiver = %s'
    values = (sender,)
    mycursor.execute(sql,values)
    users = mycursor.fetchall()
    received = [row[0] for row in users]
    #print(received)

    chats = sent + received
    print(chats)
    chat(sender)
    
    mycursor.close()

def chat(sender):
    
    receiver = input("Select Username to send message:")
    try:
        while(1):
            mycursor = mydb.cursor()
            sql = 'select sender,message_body from messages where sender in (%s,%s)'
            values = (sender,receiver)
            mycursor.execute(sql,values)
            messages = mycursor.fetchall()

            sender_list = [row[0] for row in messages]
            messages_list = [row[1] for row in messages]
            for i in range (len(sender_list)):
                print(sender_list[i], ":" ,messages_list[i])
            message = input("Enter message:")
            today = date.today()
            sql = 'insert into messages (sender,receiver,message_body,date_time) values(%s,%s,%s,%s)'
            values = (sender,receiver,message,today)
            mycursor.execute(sql,values)
            mydb.commit()
            mycursor.close()
    except KeyboardInterrupt:
        mycursor.close()
        send(sender)
    


def main():
    print("Select Operation\n1.Create Account\n2.Chat\n")
    choice = int(input())
    #choice =1
    if choice == 1:
        username = input("Enter username:")
        name = input("Enter Name:")
        create(username,name)
    elif choice == 2:
        username = input("Enter your username:")
        send(username)
    else:
        main()

main()