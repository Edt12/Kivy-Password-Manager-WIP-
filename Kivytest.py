
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

class Login(App):#Create different windows class
   
    def build(self):
 
        Window.clearcolor =(Grey)#sets background color for window to get value take each rgb value and divide by 255

        LoginLayout =FloatLayout()#float layout allows you to place widgets anywhere

        Username=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.5})#creates Input box called username,on size_hint first value is length second is width
        LoginLayout.add_widget(Username)

        Password=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.4})#creates Input box called username,on size_hint first value is length second is width
        LoginLayout.add_widget(Password)

        EnterUsernameandPassword=Button(size_hint=(0.1,0.05),pos_hint={'x':0.7,'y':0.5},text="Enter",background_color=green)
        
   
        def Callback(self):
            cursor.execute("SELECT * From UsersAndPasswords")
            Table=cursor.fetchall()
            username=cursor.execute("SELECT Username From UsersAndPasswords")

            for row in Table:#goes through every column in UserAndPasswords
                if row[0]== Username.text and row[1]== Password.text:
                    print("yaayayayayayayay")
                
                if row[0]== Username.text and row[1]!= Password.text:
                    Password.text==""
                    print("incorrect password")

                if row[0]!= Username.text and row[1]== Password.text:
                    Username.text==""
                    print("incorrect username")

               
 
            

        EnterUsernameandPassword.bind(on_press=Callback)
        LoginLayout.add_widget(EnterUsernameandPassword)

        LoginTitle=Label(text="Please Enter Your Username and Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.6},color=Black)
        LoginLayout.add_widget(LoginTitle)

        return LoginLayout
    class KeyboardListener(Widget):
        def __init__(self, **kwargs):
            super(KeyboardListener, self).__init__(**kwargs)
            self._keyboard = Window.request_keyboard(
            self.k,self, 'tet')#requested a keyboard first function is what will be triggered when release is pressed 2nd is give keyboard attribute sef third is name of keyboard
            if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
                pass
                self._keyboard.bind(on_key_down=self._on_keyboard_down)#Gives keydown variable
  
        def k(self):
            print('My keyboard have been closed!')
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

        def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
            if keycode[40]=='enter':
                keyboard.release() #calls first function in request command

            # Return True to accept the key. Otherwise, it will be used by
            # the system.
            return True
Login().run()
cursor.execute("SELECT Username FROM UsersAndPasswords")#selects a table in database
results=cursor.fetchall()#selects everything within that table
print(results)
conn.close()
