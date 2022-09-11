import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label#import widgets such as buttons and labels 
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window


green = [0, 1, 0, 1] #RGBA values /255
Grey=[0.8,0.8,0.8,1]
Black=[0,0,0,1]
#designates kv design file
Builder.load_file('App design file.kv')

#Creating Sqlite Database
conn=sqlite3.connect("UsersAndPasswords.db")#connects to database 
cursor=conn.cursor()#adds connection to cursor
#creates SQlite Database
cursor.execute("""create table IF NOT EXISTS UsersAndPasswords 
(Username text
,Password text 
)""")#inside are columns/categorys
cursor.execute("INSERT INTO UsersAndPasswords VALUES ('kpop','fafa')")
class Login(App):#Create different windows class
    def build(self):
        Window.clearcolor =(Grey)#sets background color for window to get value take each rgb value and divide by 255

        LoginLayout =FloatLayout()#float layout allows you to place widgets anywhere

        Username=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.5})#creates Input box called username,on size_hint first value is length second is width
        LoginLayout.add_widget(Username)

        Password=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.4})#creates Input box called username,on size_hint first value is length second is width
        LoginLayout.add_widget(Password)

        EnterUsername=Button(size_hint=(0.1,0.05),pos_hint={'x':0.6,'y':0.5},text="Enter",background_color=green)
        def Callback(self):
            cursor.execute("SELECT * From UsersAndPasswords")
            Table=cursor.fetchall()
            username=cursor.execute("SELECT Username From UsersAndPasswords")

            for row in Table:#goes through every column in UserAndPasswords
                if username == Username.text:
                    print("yaayayayayayayay")

               

            
            

        EnterUsername.bind(on_press=Callback)
        LoginLayout.add_widget(EnterUsername)

        EnterPassword=Button(size_hint=(0.1,0.05),pos_hint={'x':0.6,'y':0.4},text="Enter",background_color=green)
        def Callback(self):#Define what happens when button is pressed for each button redefine Callback each time you are calling a class  
            Password.text=""

        EnterPassword.bind(on_press=Callback)#To make a button do something when pressed make a variable then bind the button to it
        LoginLayout.add_widget(EnterPassword)
        
        LoginTitle=Label(text="Please Enter Your Username and Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.6},color=Black)
        LoginLayout.add_widget(LoginTitle)

        return LoginLayout
        
Login().run()
cursor.execute("SELECT Username FROM UsersAndPasswords")#selects a table in database
results=cursor.fetchall()#selects everything within that table
print(results)
conn.close()

