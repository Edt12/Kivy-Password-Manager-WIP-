import sqlite3
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition #Kivy has screens not pop up windows so screen manage manager different screens think of like switching between virtual desktops
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label#import widgets such as buttons and labels 
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
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
sm=ScreenManager(transition=NoTransition())

class PasswordCreation(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self,**kwargs)
        self.layout=FloatLayout
        #input boxes
        NewUsername=TextInput(size_hint=(0.3,0.1),pos_hint={'x':0.4,'y': 0.6})
        self.add_widget(NewUsername)
        NewPassword=TextInput(size_hint=(0.3,0.1),pos_hint={'x':0.4,'y': 0.4})
        self.add_widget(NewPassword)
        #labels
        PasswordCreationTitle=Label(text="Password Creation Screen",size_hint=(0.1,0.05),pos_hint={'x':0.35,'y':0.9},color=Black)
        self.add_widget(PasswordCreationTitle)
        NewUsernameTitle=Label(text="Please Enter Your New Username",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.7},color=Black)
        self.add_widget(NewUsernameTitle)
        NewPasswordTitle=Label(text="Please Enter Your New Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.5},color=Black)
        self.add_widget(NewPasswordTitle)
        #buttons
        AddUsernameAndPassword=Button(size_hint=(0.25,0.1),pos_hint={'x':0.7,'y':0.6},text="Add username and password",background_color=green,color=Black)
        self.add_widget(AddUsernameAndPassword)


sm.add_widget(PasswordCreation(name="PasswordCreation"))
class PasswordMenu(Screen):
      def __init__(self,**kwargs):#Instead of using build to intialise use init 
        Screen.__init__(self,**kwargs)
        self.layout=StackLayout
        Title=Label(size_hint=(0.3,0.1),pos_hint={'x':0.35,'y':0.9},text="Password Screen",color=Black)
        self.add_widget(Title)
        def Callback(self):
           sm.current="PasswordCreation"
        CreatePassword=Button(size_hint=(0.15,0.1),pos_hint={'x':0.0,'y':0.9},text="Create Password",background_color=green)
        CreatePassword.bind(on_press=Callback)
        self.add_widget(CreatePassword)





#Made ScreenManger(controls all different screens) here so i can add in the Password Menu before Login window so i can switch to it on a button press       

sm.add_widget(PasswordMenu(name="PasswordMenu"))


class Login(Screen):#Create different windows class
    
    def __init__(self,**kwargs):#Instead of using build to intialise use init as build does not work with screen class
        Screen.__init__(self,**kwargs)
    
        Window.clearcolor =(Grey)#sets background color for window to get value take each rgb value and divide by 255

        self.layout=FloatLayout()#float layout allows you to place widgets anywhere

        Username=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.5})#creates Input box called username,on size_hint first value is length second is width
        self.add_widget(Username)

        Password=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.4})#creates Input box called username,on size_hint first value is length second is width
        self.add_widget(Password)

        EnterUsernameandPassword=Button(size_hint=(0.1,0.05),pos_hint={'x':0.7,'y':0.5},text="Enter",background_color=green)

   
        def Callback(self):
            cursor.execute("SELECT * From UsersAndPasswords")
            Table=cursor.fetchall()
            username=cursor.execute("SELECT Username From UsersAndPasswords")

            for row in Table:#goes through every column in UserAndPasswords
                if row[0]== Username.text and row[1]== Password.text:
                    print("Both Correct")
                    sm.current="PasswordMenu"

                if row[0]== Username.text and row[1]!= Password.text:
                    Password.text==""
                    print("incorrect password")

                if row[0]!= Username.text and row[1]== Password.text:
                    Username.text==""
                    print("incorrect username")
                    
            

        EnterUsernameandPassword.bind(on_press=Callback)
        self.add_widget(EnterUsernameandPassword)

        LoginTitle=Label(text="Please Enter Your Username and Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.6},color=Black)
        self.add_widget(LoginTitle)




class PasswordManager(App):
    def build(self):
        sm.add_widget(Login(name="Login"))
        sm.current="Login"
        return sm
    
PasswordManager().run()