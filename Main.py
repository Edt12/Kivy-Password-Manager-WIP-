import sqlite3
import hashlib
from cryptography.fernet import Fernet
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

#Creating Sqlite Database
conn=sqlite3.connect("UsersAndPasswords.db")#connects to database 
cursor=conn.cursor()#adds connection to cursor

key=Fernet.generate_key()#makes encryption key
Key=Fernet(key)#makes it object which can be called
print(Key)
message="ryan is toes"
correct=message.encode()#In order to be encrypted a the thing your trying to encrypt has to be encoded
Encrypted=Key.encrypt(correct)#Next encrypted
Decrypted=Key.decrypt(Encrypted)#Then decrypt
print(Encrypted)
print(Decrypted.decode())#then decode to get original value
sm=ScreenManager(transition=NoTransition())
 
PasswordNumberTracker=[]
WidgetTracker=[]
Quantity=[]
Widgets=[]
def PasswordViewButtonClick(self):
    sm.current="PasswordView"
    PasswordViewScreen=sm.get_screen(sm.current)

    PasswordName=self.text
    EncodedPasswordName=PasswordName.encode()
    EncryptedPasswordName=Key.encrypt(EncodedPasswordName)
    cursor.execute("SELECT * from UserPasswords WHERE PasswordTitle = (?)",(EncryptedPasswordName,))
    DisplayPassword=cursor.fetchone()
    print(DisplayPassword)

    EncryptedPasswordTitle=DisplayPassword[0]
    DecryptedPasswordTitle=Key.decrypt(EncryptedPasswordTitle)
    PasswordTitle=DecryptedPasswordTitle.decode()
 
    EncryptedUsername=DisplayPassword[1]
    DecryptedUsername=Key.decrypt(EncryptedUsername)   
    Username=DecryptedPasswordTitle.decode()  

    EncryptedPassword=DisplayPassword[2]
    DecryptedPassword=Key.decrypt(EncryptedPassword)     
    Password=DecryptedPassword.decode()

    PasswordViewScreen.clear_widgets()

    ViewPasswordTitle=Label(size_hint=(0.3,0.1),pos_hint={'x':0.35,'y':0.7},text=str(PasswordTitle),color=Black)

    Username=Label(size_hint=(0.3,0.1),pos_hint={'x':0.35,'y':0.6},text=str(Username),color=Black)

    ViewPassword=Label(size_hint=(0.3,0.1),pos_hint={'x':0.35,'y':0.5},text=str(Password),color=Black)                            
                         
    PasswordViewTitle=Label(text="Password Viewing Screen",size_hint=(0.1,0.05),pos_hint={'x':0.49,'y':0.9},color=Black)
    PasswordViewScreen.add_widget(PasswordViewTitle)

    def BackClick(self):
        sm.current="PasswordMenu"

    PasswordViewBackButton=Button(text="Back" ,size_hint=(0.25,0.1),pos_hint={"x":0.0,"y":0.9},color=Black) 
    PasswordViewBackButton.bind(on_release=BackClick)
    PasswordViewScreen.add_widget(PasswordViewBackButton)
                       
                        
    PasswordViewScreen.add_widget(ViewPasswordTitle)
    PasswordViewScreen.add_widget(Username)
    PasswordViewScreen.add_widget(ViewPassword)

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

        CreateNewUser=Button(size_hint=(0.1,0.05),pos_hint={'x':0.7,'y':0.4},text="Create New User",background_color=green)
        def CreateNewUserClick(self):
            cursor.execute("SELECT * From UsersAndPasswords")
            UsersAndPasswords=cursor.fetchall()

            UserName=Username.text#takes text from input boxes
            PassWord=Password.text

            EncodedUsername=UserName.encode()#before hashed strings have to be encoded
            EncodedPassword=PassWord.encode()

            HashedUsername=hashlib.sha3_512(EncodedUsername)
            print(str(HashedUsername))

            HashedPassword=hashlib.sha3_512(EncodedPassword)#hashes password with SHa3_512
            print(UsersAndPasswords)

            if UsersAndPasswords==[]:#uses hex digest so it can be supported by sqlite3 and able to be inserted
                cursor.execute("Insert into UsersAndPasswords (Username,Password) VALUES(?,?)",(HashedUsername.hexdigest(),HashedPassword.hexdigest()))
                conn.commit()
                print("New User Added 1")

            for row in UsersAndPasswords:
                if row[0]!=HashedUsername.hexdigest():
                    cursor.execute("Insert into UsersAndPasswords (Username,Password) VALUES(?,?)",(HashedUsername.hexdigest(),HashedPassword.hexdigest()))
                    conn.commit()
                    print("New User Added")
            

        CreateNewUser.bind(on_press=CreateNewUserClick)
        self.add_widget(CreateNewUser)

        def GeneratePasswords(self):
            cursor.execute("SELECT * From UsersAndPasswords")
            Table=cursor.fetchall()
            UserName=Username.text
            PassWord=Password.text
            EncodedUsername=UserName.encode()#before hashed strings have to be encoded
            EncodedPassword=PassWord.encode()
            HashedUsername=hashlib.sha3_512(EncodedUsername)
            print(str(HashedUsername))
            HashedPassword=hashlib.sha3_512(EncodedPassword)#hashes passwod with SHa3_512

            
            for row in Table:#goes through every row in UsersAndPasswords
                print(row[0])
                print(row[1])
                print(UserName)
                print(PassWord)
                if row[0]==HashedUsername.hexdigest() and row[1]== HashedPassword.hexdigest():
                   
                    print("Both Correct")
                  
                    sm.current="PasswordMenu"
                    UserTracker=open("UserLoggedin","w")
                    UserTracker.write(HashedUsername.hexdigest())
    
                    UserTracker=open("UserLoggedin","r")#reads from Text file which has been written to to find who is logged in
                    User=UserTracker.read()
                    print(User)
                    cursor.execute("SELECT * from UserPasswords WHERE User = (?)",(User,))
                    Table=cursor.fetchall()
                    print(Table)
                    PasswordPos_hintX=0.0
                    PasswordPos_hintY=0.0
                    for row in Table:
                        EncryptedPasswordTitle=row[0]
                        DecryptedPasswordTitle=Key.decrypt(EncryptedPasswordTitle)
                        PasswordTitle=DecryptedPasswordTitle.decode()

                        PasswordMenuScreen=sm.get_screen("PasswordMenu")
                        sm.current="PasswordMenu"

                        IndividualPassword=Button(size_hint=(0.2,0.1),pos_hint={'x':PasswordPos_hintX,'y':PasswordPos_hintY},text=str(PasswordTitle),background_color=green,color=Black,)
                        IndividualPassword.bind(on_press=PasswordViewButtonClick)

                        PasswordMenuScreen.add_widget(IndividualPassword)#Adds Individual Password to Password Menu
                        PasswordPos_hintX+=0.2
                        PasswordNumberTracker.append("1")
                        PasswordNumber=len(PasswordNumberTracker)
                        print(len(PasswordNumberTracker))
                        PasswordNumber_DividedBy5=PasswordNumber/5
                        if PasswordNumber_DividedBy5.is_integer():#is integer checks whether something is integer
                            PasswordPos_hintX=0
                            PasswordPos_hintY+=0.1
                            
                       
           
                        if row[0]== HashedUsername.hexdigest() and row[1]!= HashedPassword.hexdigest():
                            Password.text==""
                            print("incorrect Username or Password")

                        if row[0]!=HashedUsername and row[1]== HashedPassword:
                            Username.text==""
                            print("incorrect Username or Password")
                
            

        EnterUsernameandPassword.bind(on_press=GeneratePasswords)
        self.add_widget(EnterUsernameandPassword)

        LoginTitle=Label(text="Please Enter Your Username and Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.6},color=Black)
        self.add_widget(LoginTitle)
        

        


class PasswordCreation(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self,**kwargs)
        self.layout=FloatLayout()
        #input boxes
        NewPasswordTitleInput=TextInput(size_hint=(0.3,0.1),pos_hint={'x':0.4,'y': 0.6})
        self.add_widget(NewPasswordTitleInput)
        NewUsername=TextInput(size_hint=(0.3,0.1),pos_hint={'x':0.4,'y': 0.4})
        self.add_widget(NewUsername)
        NewPassword=TextInput(size_hint=(0.3,0.1),pos_hint={'x':0.4,'y': 0.2})
        self.add_widget(NewPassword)
        #labels
        PasswordCreationTitle=Label(text="Password Creation Screen",size_hint=(0.1,0.05),pos_hint={'x':0.49,'y':0.9},color=Black)
        self.add_widget(PasswordCreationTitle)
        
        NewPasswordTitleLabel=Label(text="Please enter your Password Title",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.7},color=Black)
        self.add_widget(NewPasswordTitleLabel)

        NewUsernameTitle=Label(text="Please Enter Your New Username",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.5},color=Black)
        self.add_widget(NewUsernameTitle)
        
        NewPasswordTitle=Label(text="Please Enter Your New Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.3},color=Black)
        self.add_widget(NewPasswordTitle)
        #buttons
        def AddPassword(self):

            Password=NewPassword.text
            EncodedPassword=Password.encode()
            EncryptedPassword=Key.encrypt(EncodedPassword)

            Username=NewUsername.text
            EncodedUsername=Username.encode()
            EncryptedUsername=Key.encrypt(EncodedPassword)

            PasswordTitle=NewPasswordTitleInput.text
            EncodedPasswordTitle=PasswordTitle.encode()
            EncryptedPassworditle=Key.encrypt(EncodedPasswordTitle)

            UserTracker=open("UserLoggedin","r")#reads from Text file which has been written to to find who is logged in
            User=UserTracker.read()
            UserTracker.close()
            
            cursor.execute("INSERT INTO UserPasswords (PasswordTitle,Username,Password,User) VALUES(?,?,?,?)",(EncryptedPassworditle,EncryptedUsername,EncryptedPassword,User))
            conn.commit()
         
            print(len(PasswordNumberTracker))
            
    
            PasswordNumber=len(PasswordNumberTracker)
            
       

            PasswordNumberDividedBy5=PasswordNumber/5
            XandYSplit=str(PasswordNumberDividedBy5).split(".")
          
            PasswordX=int(XandYSplit[1])
            PasswordY=int(XandYSplit[0])
            
            PasswordPos_hintX=PasswordX/10
           
            PasswordPos_hintY=PasswordY/10
                    
            IndividualPassword=Button(size_hint=(0.2,0.1),pos_hint={'x':PasswordPos_hintX,'y':PasswordPos_hintY},text=str(PasswordTitle),background_color=green,color=Black,)
            IndividualPassword.bind(on_press=PasswordViewButtonClick)
            
            PasswordMenuScreen=sm.get_screen("PasswordMenu")
            PasswordMenuScreen.add_widget(IndividualPassword)#Adds Individual Password to Password Menu
            #add 1 to password number 
            PasswordNumberTracker.append("1")
            #deletes text in input boxes after new password is made
            NewPassword.text=""
            NewUsername.text=""
            NewPasswordTitleInput.text=""
          

        AddUsernameAndPassword=Button(size_hint=(0.25,0.1),pos_hint={'x':0.7,'y':0.6},text="Add username and password",background_color=green,color=Black)
        AddUsernameAndPassword.bind(on_press=AddPassword)
        self.add_widget(AddUsernameAndPassword)

        def BackButtonClick(self):
            sm.current="PasswordMenu"
            
        Backbutton=Button(size_hint=(0.25,0.1),pos_hint={'x':0.0,'y':0.9},text="back",background_color=green,color=Black)
        Backbutton.bind(on_press=BackButtonClick)
        self.add_widget(Backbutton)

class PasswordView(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self,**kwargs)
        self.layout=FloatLayout
        
        
        

class PasswordMenu(Screen):
      def __init__(self,**kwargs):#Instead of using build to intialise use init 
        Screen.__init__(self,**kwargs) 
        self.layout=FloatLayout

        Title=Label(size_hint=(0.3,0.1),pos_hint={'x':0.35,'y':0.9},text="Password Screen",color=Black)
        self.add_widget(Title)

        def CreatePasswordClick(self):
           sm.current="PasswordCreation" #Changes current screen to Password Creation Screen

        CreatePassword=Button(size_hint=(0.15,0.1),pos_hint={'x':0.0,'y':0.9},text="Create Password",background_color=green,color=Black)
        CreatePassword.bind(on_press=CreatePasswordClick)
        self.add_widget(CreatePassword)

def main():
    #creates SQlite Database
    cursor.execute("""create table IF NOT EXISTS UsersAndPasswords 
    (Username blob
    ,Password blob
    )""")#inside are columns/categorys
    cursor.execute("""create table IF NOT EXISTS UserPasswords
    (PasswordTitle blob,
    Username blob
    ,Password blob
    ,User blob )""") #inside are columns/categorys  

    sm.add_widget(PasswordView(name="PasswordView"))
    sm.add_widget(Login(name="Login"))
    sm.add_widget(PasswordMenu(name="PasswordMenu"))
    sm.add_widget(PasswordCreation(name="PasswordCreation"))

    class PasswordManager(App):
        def build(self):

            sm.current="Login"
            return sm
    
    PasswordManager().run()
    UserTracker=open("UserLoggedin","w")
    UserTracker.write("")   
    UserTracker.close()
main()