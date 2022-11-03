# -*-coding:utf-8-*-
#import os
import kivy
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from dianzu import Res,open_txt
import dianzu

#定义全局变量
global res_back,res_back_num  #输入的电阻值，输入电阻值的位数
global point_flag,zero_flag #小数点标志位,零标志位
global res_Category_flag #0805/1206标志位
global res_list #0805/1206电阻列表
global res_list1206 #1206电阻列表
global res_list0805 #1206电阻列表
global res_list_save #保存的时候所用的列表
global res_list_save_flag #保存的时候所用的列表
global res_input_flag #再次输入标志

##kivy.resources.resource_add_path("/usr/share/fonts/truetype/droid/")
res_Category_flag='0805'
res_back=''
res_back_num=0
point_flag=0
zero_flag=0
res_list={}
res_list0805={}
res_list1206={}
res_list_save=[]
res_list_save_flag=0
res_input_flag=0
class Res_fun(object):
    
    def __init__(self):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        # 设置属性
        pass
    #读取文件，加载到res_list,res_list0805,res_list1206三个列表中
    def read_text(self):
        #path1=os.path.abspath('.')
        global res_list,res_list0805,res_list1206
        res_list0805={}
        res_list1206={}
        res_list={}
        s=open_txt().open('1206')
        for i in range(len(s)):
           res_list1206[i]=s[i][1]
        s=open_txt().open('0805')
        for i in range(len(s)):
           res_list0805[i]=s[i][1]  
        Res_fun().res_changelist()
    #此函数用来显示电阻列表
    def res_show(self,number):
        global res_Category_flag,res_list0805,res_list1206         
        if(res_Category_flag=='0805'):
            if number<len(res_list0805):
                return str(res_list0805[number])
            else:
                return ''
        else:
            if number<len(res_list1206):
                return str(res_list1206[number])
            else:
                return ''
    #此函数用来切换列表，falg=1表示按键按下
    def res_change(self,flag):
        global res_Category_flag
        if(flag==1):
            if(res_Category_flag=='0805'):
               res_Category_flag='1206'
            else:
               res_Category_flag='0805'
        else:
            if (res_Category_flag=='1206'):
                return '1206'
            else:
                return '0805'
    def res_changelist(self):
        global res_Category_flag,res_list0805,res_list1206  
        if (res_Category_flag=='0805'):
            res_list=res_list0805.copy()
        else:
            res_list=res_list1206.copy()
    def button_state(self,flag):
        global res_Category_flag
        if(res_Category_flag=='0805'):
            if(flag==1):
                return 'down'
            else:
                return 'normal'   
        else:
            if(flag==1):
                return 'normal'
            else:
                return 'down'
    def res_save_onpress(self,number):
       global res_list_save,res_list_save_flag
       if(res_list_save_flag==0):
           res_list_save=[]
       res_list_save_flag+=1
       if(number!=''):
           if str(number).replace(".",'').isdigit():
               if (number.count(".")==0 or number.count(".")==1):
                   if(str(number) not in res_list_save):
                       res_list_save.append(float(number))
       if(res_list_save_flag>=76):
            res_list_save_flag=0
            try:
                   res_list_save.sort()
                   list1=[]
                   for i in res_list_save:
                       if i not in list1:
                           list1.append(i)
                   if(res_Category_flag=='0805'):
                       dianzu = open('./src/0805.txt', 'w')
                   else:
                       dianzu = open('./src/1206.txt', 'w')
                   for i in range(len(list1)):
                       dianzu.write('R'+str(i+1)+'\t'+str(list1[i])+'\n')
            finally:
                   dianzu.close()
            Res_fun().read_text()
    def clear(self):
        global res_back_num,point_flag,zero_flag,res_back
        res_back_num=0
        point_flag=0
        zero_flag=0
        res_back=''
class MyScreenManager(ScreenManager):
    pass
class FirstScreen(Screen):
    pass
class SecondScreen(Screen):
    pass
class ThirdScreen(Screen):
    pass
class RootWidget(FloatLayout):
    def __init__(self,**kwargs):
        super(RootWidget,self).__init__(**kwargs)
    def res_show(self,button_number,rev):
        global res_back_num,res_back,point_flag,zero_flag
        #rev 为输入标志，小数点+0~9的数字时rev=1，其余rev=0
        if rev and res_back_num<8:
            #小数点只能输入一次，再次输入无效；第一位为零,第二位不为小数点，再次输入0无效
            if(point_flag and str(button_number)=='.') or (zero_flag and str(button_number)=='0' and point_flag==0 ) :
                pass
            else:
                if str(button_number)=='.':
                    point_flag=1
                if str(button_number)=='0'and res_back_num==0:
                    zero_flag=1
                if(res_back_num==1):
                    #第一位为零，第二位不为小数点，清掉第一位的零
                    if zero_flag and  point_flag==0:
                      res_back=''
                      zero_flag=0
                res_back=str(res_back)+str(button_number)
                res_back_num+=rev
                if (res_back_num>=8):
                    res_back_numk=8
        elif(str(button_number)=='C'):
             Res_fun().clear()
        elif(str(button_number)=='X'):
            if(res_back_num>0):
                new_str=''
                for i in range(0, len(res_back)-1):
                    new_str = new_str + res_back[i]
                if(point_flag and ('.' not in new_str)):
                    point_flag=0
                if(zero_flag and ('0' not in new_str)):
                    zero_flag=0
                res_back_num-=1
                res_back=new_str
        else:
            pass
        return res_back+'k'
    def res_show_one(self):
        global res_back,res_Category_flag
        if (res_back==''):
            return''
        else:
            k=Res(float(res_back),res_Category_flag).Res_value_one()
            return str(k[0])+' k 误差:'+str(k[1])+' k'
    def res_show_two(self):
        global res_back,res_Category_flag
        if (res_back==''):
            return''
        else:
            k=Res(float(res_back),res_Category_flag).Res_value_two()
            if (k is not None):
                return str(k[0])+' k// '+ str(k[1])+ ' k 误差:'+str(k[2])+' k'
            else:
                return ''             
    def res_show_three(self):
        global res_back,res_Category_flag
        if (res_back==''):
            return''
        else:
            k=Res(float(res_back),res_Category_flag).Res_value_three()
            if(k is None):
                return ''
            else:
                return str(k[0])+' k// '+ str(k[1])+' k// '+ str(k[2])+ ' k 误差:'+str(k[3])+' k'
    def text_font(self):
        font1=kivy.resources.resource_find("./src/DroidSansFallback.ttf")
        return  font1
    #切换计算的电阻类型，flag=1表示电阻0805
    def res_Category(self,flag):
        global res_Category_flag,res_list0805,res_list1206
        if (flag==1):
            res_Category_flag='0805'
            res_list=res_list0805.copy()
        else:
            res_Category_flag='1206'
            res_list=res_list1206.copy() 
    def button_state(self,flag):
        ss=Res_fun().button_state(flag)
        return ss
    def res_Category2(self):
        global res_Category_flag
        return res_Category_flag
    def res_shown2(self,number):
        ss=Res_fun().res_show(number)
        return ss
    #flag=1,start按钮按下;flag=0,数字键按下
    def res_input_againt(self,flag):
        global res_input_flag
        if(flag==1):
            res_input_flag=1
        else:
            if(res_input_flag==1):
                res_input_flag=0
                Res_fun().clear()
class RootWidget2(FloatLayout):
    def __init__(self,**kwargs):
        super(RootWidget2,self).__init__(**kwargs)
    def res_shown2(self,number):
        ss=Res_fun().res_show(number)
        return ss         
    def res_change(self,flag):
        ss=Res_fun().res_change(flag)
        return ss
    def button_state(self,flag):
        ss=Res_fun().button_state(flag)
        return ss
    def res_Category2(self):
        global res_Category_flag
        return res_Category_flag
    def res_save_onpress(self,number):
        Res_fun().res_save_onpress(number)
class RootWidget3(FloatLayout):
    def __init__(self,**kwargs):
        super(RootWidget3,self).__init__(**kwargs)
    def res_shown1(self,number):
        pass
    def res_change(self,flag):
        ss=Res_fun().res_change(flag)
        return ss 
    def res_shown2(self,number):
        ss=Res_fun().res_show(number)
        return ss
    def button_state(self,flag):
        ss=Res_fun().button_state(flag)
        return ss
    def res_save_onpress(self,number):
        Res_fun().res_save_onpress(number)
class CustomLayout(GridLayout):

    background_image = ObjectProperty(
        Image(
            source='./src/2.jpg',
            anim_delay=.1))
class CustomLayout4(GridLayout):

    background_image = ObjectProperty(
        Image(
            source='./src/2.jpg',
            anim_delay=.1))
class CustomLayout6(GridLayout):

    background_image = ObjectProperty(
        Image(
            source='./src/2.jpg',
            anim_delay=.1))
class CustomLayout1(GridLayout):
    pass
class CustomLayout3(GridLayout):
    pass  
class CustomLayout2(GridLayout):
    pass
class CustomLayout5(GridLayout):
    pass
class CustomLayout7(GridLayout):
    pass
class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        return sm
               
Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MyScreenManager:
    id:screen_management
    transition: FadeTransition()
    FirstScreen:
        id:first
        name: 'first'
        manager:screen_management
    SecondScreen:
        id:second
        name: 'second'
        manager:screen_management
    ThirdScreen:
        id:third
        name: 'third'
        manager:screen_management
    
<FirstScreen>:
    CustomLayout:
    RootWidget:
        id:root1
<CustomLayout>:
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            texture: self.background_image.texture
            pos: self.pos
            size: self.size
<RootWidget>:
    CustomLayout:
        size_hint: 1.0, 1.0
        pos_hint: {'center_x': .5, 'center_y': .5}
        rows:3
        cols:1
        CustomLayout1:
            size_hint: .3, .3
            pos_hint: {'center_x': .5, 'center_y': .5}
            rows:1
            cols:3
            Button:
                id:res_0805
                text: '0805'
                state:'down'
                font_size:30
                #background_color:1.3,1.98,2.18,1
                disabled_color:0.95,0.95,.95,1
                on_press: root.res_Category(1)
                on_release: root.ids.res_1206.state=root.button_state(2)
                on_release: root.ids.res_0805.state=root.button_state(1)

            Button:
                id:res_1206
                text: '1206'
                state:
                font_size: 30
               # background_color:0.6,1.41,1.95,1
                disabled_color:0.8,.8,.8,1
                on_press: root.res_Category(2)
                on_release: root.ids.res_0805.state=root.button_state(1)
                on_release: root.ids.res_1206.state=root.button_state(2)

            Button:
                text: 'SET'
                font_size: 30
                disabled_color:0.8,.8,.8,1
                on_release: app.root.current = 'second'
                #更改第二个屏幕的显示
                on_release: app.root.get_screen("second").ids.root2.ids.res_2_button.text=root.res_Category2()
                on_release: app.root.get_screen("third").ids.root3.ids.res_3_button.text=root.res_Category2()
                on_release: app.root.get_screen("second").ids.root2.ids.R1.text=root.res_shown2(0)
                on_release: app.root.get_screen("second").ids.root2.ids.R2.text=root.res_shown2(1)
                on_release: app.root.get_screen("second").ids.root2.ids.R3.text=root.res_shown2(2)
                on_release: app.root.get_screen("second").ids.root2.ids.R4.text=root.res_shown2(3)
                on_release: app.root.get_screen("second").ids.root2.ids.R5.text=root.res_shown2(4)
                on_release: app.root.get_screen("second").ids.root2.ids.R6.text=root.res_shown2(5)
                on_release: app.root.get_screen("second").ids.root2.ids.R7.text=root.res_shown2(6)
                on_release: app.root.get_screen("second").ids.root2.ids.R8.text=root.res_shown2(7)
                on_release: app.root.get_screen("second").ids.root2.ids.R9.text=root.res_shown2(8)
                on_release: app.root.get_screen("second").ids.root2.ids.R10.text=root.res_shown2(9)
                on_release: app.root.get_screen("second").ids.root2.ids.R11.text=root.res_shown2(10)
                on_release: app.root.get_screen("second").ids.root2.ids.R12.text=root.res_shown2(11)
                on_release: app.root.get_screen("second").ids.root2.ids.R13.text=root.res_shown2(12)
                on_release: app.root.get_screen("second").ids.root2.ids.R14.text=root.res_shown2(13)
                on_release: app.root.get_screen("second").ids.root2.ids.R15.text=root.res_shown2(14)
                on_release: app.root.get_screen("second").ids.root2.ids.R16.text=root.res_shown2(15)
                on_release: app.root.get_screen("second").ids.root2.ids.R17.text=root.res_shown2(16)
                on_release: app.root.get_screen("second").ids.root2.ids.R18.text=root.res_shown2(17)
                on_release: app.root.get_screen("second").ids.root2.ids.R19.text=root.res_shown2(18)
                on_release: app.root.get_screen("second").ids.root2.ids.R20.text=root.res_shown2(19)
                on_release: app.root.get_screen("second").ids.root2.ids.R21.text=root.res_shown2(20)
                on_release: app.root.get_screen("second").ids.root2.ids.R22.text=root.res_shown2(21)
                on_release: app.root.get_screen("second").ids.root2.ids.R23.text=root.res_shown2(22)
                on_release: app.root.get_screen("second").ids.root2.ids.R24.text=root.res_shown2(23)
                on_release: app.root.get_screen("second").ids.root2.ids.R25.text=root.res_shown2(24)
                on_release: app.root.get_screen("second").ids.root2.ids.R26.text=root.res_shown2(25)
                on_release: app.root.get_screen("second").ids.root2.ids.R27.text=root.res_shown2(26)
                on_release: app.root.get_screen("second").ids.root2.ids.R28.text=root.res_shown2(27)
                on_release: app.root.get_screen("second").ids.root2.ids.R29.text=root.res_shown2(28)
                on_release: app.root.get_screen("second").ids.root2.ids.R30.text=root.res_shown2(29)
                on_release: app.root.get_screen("second").ids.root2.ids.R31.text=root.res_shown2(30)
                on_release: app.root.get_screen("second").ids.root2.ids.R32.text=root.res_shown2(31)
                on_release: app.root.get_screen("second").ids.root2.ids.R33.text=root.res_shown2(32)
                on_release: app.root.get_screen("second").ids.root2.ids.R34.text=root.res_shown2(33)
                on_release: app.root.get_screen("second").ids.root2.ids.R35.text=root.res_shown2(34)
                on_release: app.root.get_screen("second").ids.root2.ids.R36.text=root.res_shown2(35)
                on_release: app.root.get_screen("second").ids.root2.ids.R37.text=root.res_shown2(36)
                on_release: app.root.get_screen("second").ids.root2.ids.R38.text=root.res_shown2(37)
                on_release: app.root.get_screen("third").ids.root3.ids.R39.text=root.res_shown2(38)
                on_release: app.root.get_screen("third").ids.root3.ids.R40.text=root.res_shown2(39)
                on_release: app.root.get_screen("third").ids.root3.ids.R41.text=root.res_shown2(40)
                on_release: app.root.get_screen("third").ids.root3.ids.R42.text=root.res_shown2(41)
                on_release: app.root.get_screen("third").ids.root3.ids.R43.text=root.res_shown2(42)
                on_release: app.root.get_screen("third").ids.root3.ids.R44.text=root.res_shown2(43)
                on_release: app.root.get_screen("third").ids.root3.ids.R45.text=root.res_shown2(44)
                on_release: app.root.get_screen("third").ids.root3.ids.R46.text=root.res_shown2(45)
                on_release: app.root.get_screen("third").ids.root3.ids.R47.text=root.res_shown2(46)
                on_release: app.root.get_screen("third").ids.root3.ids.R48.text=root.res_shown2(47)
                on_release: app.root.get_screen("third").ids.root3.ids.R49.text=root.res_shown2(48)
                on_release: app.root.get_screen("third").ids.root3.ids.R50.text=root.res_shown2(49)
                on_release: app.root.get_screen("third").ids.root3.ids.R51.text=root.res_shown2(50)
                on_release: app.root.get_screen("third").ids.root3.ids.R52.text=root.res_shown2(51)
                on_release: app.root.get_screen("third").ids.root3.ids.R53.text=root.res_shown2(52)
                on_release: app.root.get_screen("third").ids.root3.ids.R54.text=root.res_shown2(53)
                on_release: app.root.get_screen("third").ids.root3.ids.R55.text=root.res_shown2(54)
                on_release: app.root.get_screen("third").ids.root3.ids.R56.text=root.res_shown2(55)
                on_release: app.root.get_screen("third").ids.root3.ids.R57.text=root.res_shown2(56)
                on_release: app.root.get_screen("third").ids.root3.ids.R58.text=root.res_shown2(57)
                on_release: app.root.get_screen("third").ids.root3.ids.R59.text=root.res_shown2(58)
                on_release: app.root.get_screen("third").ids.root3.ids.R60.text=root.res_shown2(59)
                on_release: app.root.get_screen("third").ids.root3.ids.R61.text=root.res_shown2(60)
                on_release: app.root.get_screen("third").ids.root3.ids.R62.text=root.res_shown2(61)
                on_release: app.root.get_screen("third").ids.root3.ids.R63.text=root.res_shown2(62)
                on_release: app.root.get_screen("third").ids.root3.ids.R64.text=root.res_shown2(63)
                on_release: app.root.get_screen("third").ids.root3.ids.R65.text=root.res_shown2(64)
                on_release: app.root.get_screen("third").ids.root3.ids.R66.text=root.res_shown2(65)
                on_release: app.root.get_screen("third").ids.root3.ids.R67.text=root.res_shown2(66)
                on_release: app.root.get_screen("third").ids.root3.ids.R68.text=root.res_shown2(67)
                on_release: app.root.get_screen("third").ids.root3.ids.R69.text=root.res_shown2(68)
                on_release: app.root.get_screen("third").ids.root3.ids.R70.text=root.res_shown2(69)
                on_release: app.root.get_screen("third").ids.root3.ids.R71.text=root.res_shown2(70)
                on_release: app.root.get_screen("third").ids.root3.ids.R72.text=root.res_shown2(71)
                on_release: app.root.get_screen("third").ids.root3.ids.R73.text=root.res_shown2(72)
                on_release: app.root.get_screen("third").ids.root3.ids.R74.text=root.res_shown2(73)
                on_release: app.root.get_screen("third").ids.root3.ids.R75.text=root.res_shown2(74)
                on_release: app.root.get_screen("third").ids.root3.ids.R76.text=root.res_shown2(75)
        CustomLayout2:
            size_hint: 0.5, 1.0
            pos_hint: {'center_x': .5, 'center_y': .5}
            rows:7
            cols:1
            Label:
                text_size: self.width-20, self.height
                font_size: 30
                font_name:root.text_font()
                text:'匹配电阻1个;'
                background_color:1.3,1.98,2.18,1
                halign: 'left'
            Label:
                id:one_input
                text_size: self.width-20, self.height
                font_size: 30
                font_name:root.text_font()
                text:
                halign: 'right'

            Label:
                text_size: self.width-20, self.height
                font_size: 30
                font_name:root.text_font()
                text:'匹配电阻2个:'
                background_color:1.3,1.98,2.18,1
                halign: 'left'
            Label:
                id:two_input
                text_size: self.width-20, self.height
                font_size: 30
                font_name:root.text_font()
                text:
                halign: 'right'
            Label:
                text_size: self.width-20, self.height
                font_size: 30
                font_name:root.text_font()
                text:'匹配电阻3个:'
                background_color:1.3,1.98,2.18,1
                halign: 'left'
            Label:
                id:three_input
                text_size: self.width-20, self.height
                font_size: 30
                font_name:root.text_font()
                text:
                halign: 'right'
            Label:
                id:res_input
                text_size: self.width-20, self.height
                font_size: 30
                text:'k'
                halign: 'right'
        CustomLayout3:
            size_hint: 1.0, 1.0
            pos_hint: {'center_x': .5, 'center_y': .5}
            rows:4
            cols:4
            Button:
                text: '7'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(7,1)
            Button:
                text: '8'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(8,1)
            Button:
                text: '9'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(9,1)
            Button:
                text:  'X'
                font_size: 30
                background_color:1.3,1.98,2.18,1
                on_release:root.ids.res_input.text=root.res_show('X',0)
            Button:
                text: '4'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(4,1)
            Button:
                text: '5'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(5,1)
            Button:
                text: '6'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(6,1)
            Button:
                text: 'C'
                font_size: 30
                background_color:1.3,1.98,2.18,1
                on_release:root.ids.res_input.text=''+root.res_show('C',0)
                on_release:root.ids.one_input.text=''
                on_release:root.ids.two_input.text=''
                on_release:root.ids.three_input.text=''
            Button:
                text: '1'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(1,1)
            Button:
                text: '2'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(2,1)
            Button:
                text: '3'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(3,1)
            Button:
                text: '+'
                font_size: 40
                background_color:1.3,1.98,2.18,1
            Button:
                text: 'EXIT'
                font_size: 30
                background_color:1.3,1.98,2.18,1
                on_release:exit()
            Button:
                text: '0'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show(0,1)
            Button:
                text: '.'
                font_size: 40
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(0)
                on_release:root.ids.res_input.text=root.res_show('.',1)
                
            Button:
                text: 'START'
                font_size: 30
                background_color:1.3,1.98,2.18,1
                on_press:root.res_input_againt(1)
                on_release:root.ids.one_input.text=root.res_show_one()
                on_release:root.ids.two_input.text=root.res_show_two()
                on_release:root.ids.three_input.text=root.res_show_three()
<SecondScreen>:

    CustomLayout4:
    RootWidget2:
        id:root2
<CustomLayout4>
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            texture: self.background_image.texture
            pos: self.pos
            size: self.size
<RootWidget2>:
    CustomLayout5:
        size_hint: 1.0, 1.0
        pos_hint: {'center_x': .5, 'center_y': .5}
        rows:20
        cols:4
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R1'
            halign: 'left'
        TextInput:
            id:R1
            multiline:False
            valign: 'bottom'
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R2'
            halign: 'left'
        TextInput:
            id:R2
            text:
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R3'
            halign: 'left'
        TextInput:
            id:R3
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R4'
            halign: 'left'
        TextInput:
            id:R4
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R5'
            halign: 'left'
        TextInput:
            id:R5
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R6'
            halign: 'left'
        TextInput:
            id:R6
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R7'
            halign: 'left'
        TextInput:
            id:R7
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R8'
            halign: 'left'
        TextInput:
            id:R8
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R9'
            halign: 'left'
        TextInput:
            id:R9
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R10'
            halign: 'left'
        TextInput:
            id:R10
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R11'
            halign: 'left'
        TextInput:
            id:R11
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R12'
            halign: 'left'
        TextInput:
            id:R12
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R13'
            halign: 'left'
        TextInput:
            id:R13
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R14'
            halign: 'left'
        TextInput:
            id:R14
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R15'
            halign: 'left'
        TextInput:
            id:R15
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R16'
            halign: 'left'
        TextInput:
            id:R16
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R17'
            halign: 'left'
        TextInput:
            id:R17
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R18'
            halign: 'left'
        TextInput:
            id:R18
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'

        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R19'
            halign: 'left'
        TextInput:
            id:R19
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R20'
            halign: 'left'
        TextInput:
            id:R20
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R21'
            halign: 'left'
        TextInput:
            id:R21
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R22'
            halign: 'left'
        TextInput:
            id:R22
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R23'
            halign: 'left'
        TextInput:
            id:R23
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R24'
            halign: 'left'
        TextInput:
            id:R24
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R25'
            halign: 'left'
        TextInput:
            id:R25
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R26'
            halign: 'left'
        TextInput:
            id:R26
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R27'
            halign: 'left'
        TextInput:
            id:R27
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R28'
            halign: 'left'
        TextInput:
            id:R28
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R29'
            halign: 'left'
        TextInput:
            id:R29
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R30'
            halign: 'left'
        TextInput:
            id:R30
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R31'
            halign: 'left'
        TextInput:
            id:R31
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R32'
            halign: 'left'
        TextInput:
            id:R32
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R33'
            halign: 'left'
        TextInput:
            id:R33
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R34'
            halign: 'left'
        TextInput:
            id:R34
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R35'
            halign: 'left'
        TextInput:
            id:R35
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R36'
            halign: 'left'
        TextInput:
            id:R36
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R37'
            halign: 'left'
        TextInput:
            id:R37
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R38'
            halign: 'left'
        TextInput:
            id:R38
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Button:
            text: 'HOME'
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_release: app.root.current ='first'
            on_release: app.root.get_screen("first").ids.root1.ids.res_1206.state=root.button_state(0)
            on_release: app.root.get_screen("first").ids.root1.ids.res_0805.state=root.button_state(1)
        Button:
            text: 'NEXT'
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_release: app.root.current ='third'
           # on_release: app.root.get_screen("third").ids.root3.ids.res_3_button.text=root.res_Category2()
            
            
        Button:
            text: 'SAVE'
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_press:root.res_save_onpress(root.ids.R1.text)
            on_press:root.res_save_onpress(root.ids.R2.text)
            on_press:root.res_save_onpress(root.ids.R3.text)
            on_press:root.res_save_onpress(root.ids.R4.text)
            on_press:root.res_save_onpress(root.ids.R5.text)
            on_press:root.res_save_onpress(root.ids.R6.text)
            on_press:root.res_save_onpress(root.ids.R7.text)
            on_press:root.res_save_onpress(root.ids.R8.text)
            on_press:root.res_save_onpress(root.ids.R9.text)
            on_press:root.res_save_onpress(root.ids.R10.text)
            on_press:root.res_save_onpress(root.ids.R11.text)
            on_press:root.res_save_onpress(root.ids.R12.text)
            on_press:root.res_save_onpress(root.ids.R13.text)
            on_press:root.res_save_onpress(root.ids.R14.text)
            on_press:root.res_save_onpress(root.ids.R15.text)
            on_press:root.res_save_onpress(root.ids.R16.text)
            on_press:root.res_save_onpress(root.ids.R17.text)
            on_press:root.res_save_onpress(root.ids.R18.text)
            on_press:root.res_save_onpress(root.ids.R19.text)
            on_press:root.res_save_onpress(root.ids.R20.text)
            on_press:root.res_save_onpress(root.ids.R21.text)
            on_press:root.res_save_onpress(root.ids.R22.text)
            on_press:root.res_save_onpress(root.ids.R23.text)
            on_press:root.res_save_onpress(root.ids.R24.text)
            on_press:root.res_save_onpress(root.ids.R25.text)
            on_press:root.res_save_onpress(root.ids.R26.text)
            on_press:root.res_save_onpress(root.ids.R27.text)
            on_press:root.res_save_onpress(root.ids.R28.text)
            on_press:root.res_save_onpress(root.ids.R29.text)
            on_press:root.res_save_onpress(root.ids.R30.text)
            on_press:root.res_save_onpress(root.ids.R31.text)
            on_press:root.res_save_onpress(root.ids.R32.text)
            on_press:root.res_save_onpress(root.ids.R33.text)
            on_press:root.res_save_onpress(root.ids.R34.text)
            on_press:root.res_save_onpress(root.ids.R35.text)
            on_press:root.res_save_onpress(root.ids.R36.text)
            on_press:root.res_save_onpress(root.ids.R37.text)
            on_press:root.res_save_onpress(root.ids.R38.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R39.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R40.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R41.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R42.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R43.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R44.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R45.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R46.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R47.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R48.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R49.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R50.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R51.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R52.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R53.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R54.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R55.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R56.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R57.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R58.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R59.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R60.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R61.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R62.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R63.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R64.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R65.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R66.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R67.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R68.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R69.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R70.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R71.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R72.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R73.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R74.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R75.text)
            on_press:root.res_save_onpress( app.root.get_screen("third").ids.root3.ids.R76.text)
            on_release: root.ids.R1.text=root.res_shown2(0)
            on_release: root.ids.R2.text=root.res_shown2(1)
            on_release: root.ids.R3.text=root.res_shown2(2)
            on_release: root.ids.R4.text=root.res_shown2(3)
            on_release: root.ids.R5.text=root.res_shown2(4)
            on_release: root.ids.R6.text=root.res_shown2(5)
            on_release: root.ids.R7.text=root.res_shown2(6)
            on_release: root.ids.R8.text=root.res_shown2(7)
            on_release: root.ids.R9.text=root.res_shown2(8)
            on_release: root.ids.R10.text=root.res_shown2(9)
            on_release: root.ids.R11.text=root.res_shown2(10)
            on_release: root.ids.R12.text=root.res_shown2(11)
            on_release: root.ids.R13.text=root.res_shown2(12)
            on_release: root.ids.R14.text=root.res_shown2(13)
            on_release: root.ids.R15.text=root.res_shown2(14)
            on_release: root.ids.R16.text=root.res_shown2(15)
            on_release: root.ids.R17.text=root.res_shown2(16)
            on_release: root.ids.R18.text=root.res_shown2(17)
            on_release: root.ids.R19.text=root.res_shown2(18)
            on_release: root.ids.R20.text=root.res_shown2(19)
            on_release: root.ids.R21.text=root.res_shown2(20)
            on_release: root.ids.R22.text=root.res_shown2(21)
            on_release: root.ids.R23.text=root.res_shown2(22)
            on_release: root.ids.R24.text=root.res_shown2(23)
            on_release: root.ids.R25.text=root.res_shown2(24)
            on_release: root.ids.R26.text=root.res_shown2(25)
            on_release: root.ids.R27.text=root.res_shown2(26)
            on_release: root.ids.R28.text=root.res_shown2(27)
            on_release: root.ids.R29.text=root.res_shown2(28)
            on_release: root.ids.R30.text=root.res_shown2(29)
            on_release: root.ids.R31.text=root.res_shown2(30)
            on_release: root.ids.R32.text=root.res_shown2(31)
            on_release: root.ids.R33.text=root.res_shown2(32)
            on_release: root.ids.R34.text=root.res_shown2(33)
            on_release: root.ids.R35.text=root.res_shown2(34)
            on_release: root.ids.R36.text=root.res_shown2(35)
            on_release: root.ids.R37.text=root.res_shown2(36)
            on_release: root.ids.R38.text=root.res_shown2(37)
            on_release: app.root.get_screen("third").ids.root3.ids.R39.text=root.res_shown2(38)
            on_release: app.root.get_screen("third").ids.root3.ids.R40.text=root.res_shown2(39)
            on_release: app.root.get_screen("third").ids.root3.ids.R41.text=root.res_shown2(40)
            on_release: app.root.get_screen("third").ids.root3.ids.R42.text=root.res_shown2(41)
            on_release: app.root.get_screen("third").ids.root3.ids.R43.text=root.res_shown2(42)
            on_release: app.root.get_screen("third").ids.root3.ids.R44.text=root.res_shown2(43)
            on_release: app.root.get_screen("third").ids.root3.ids.R45.text=root.res_shown2(44)
            on_release: app.root.get_screen("third").ids.root3.ids.R46.text=root.res_shown2(45)
            on_release: app.root.get_screen("third").ids.root3.ids.R47.text=root.res_shown2(46)
            on_release: app.root.get_screen("third").ids.root3.ids.R48.text=root.res_shown2(47)
            on_release: app.root.get_screen("third").ids.root3.ids.R49.text=root.res_shown2(48)
            on_release: app.root.get_screen("third").ids.root3.ids.R50.text=root.res_shown2(49)
            on_release: app.root.get_screen("third").ids.root3.ids.R51.text=root.res_shown2(50)
            on_release: app.root.get_screen("third").ids.root3.ids.R52.text=root.res_shown2(51)
            on_release: app.root.get_screen("third").ids.root3.ids.R53.text=root.res_shown2(52)
            on_release: app.root.get_screen("third").ids.root3.ids.R54.text=root.res_shown2(53)
            on_release: app.root.get_screen("third").ids.root3.ids.R55.text=root.res_shown2(54)
            on_release: app.root.get_screen("third").ids.root3.ids.R56.text=root.res_shown2(55)
            on_release: app.root.get_screen("third").ids.root3.ids.R57.text=root.res_shown2(56)
            on_release: app.root.get_screen("third").ids.root3.ids.R58.text=root.res_shown2(57)
            on_release: app.root.get_screen("third").ids.root3.ids.R59.text=root.res_shown2(58)
            on_release: app.root.get_screen("third").ids.root3.ids.R60.text=root.res_shown2(59)
            on_release: app.root.get_screen("third").ids.root3.ids.R61.text=root.res_shown2(60)
            on_release: app.root.get_screen("third").ids.root3.ids.R62.text=root.res_shown2(61)
            on_release: app.root.get_screen("third").ids.root3.ids.R63.text=root.res_shown2(62)
            on_release: app.root.get_screen("third").ids.root3.ids.R64.text=root.res_shown2(63)
            on_release: app.root.get_screen("third").ids.root3.ids.R65.text=root.res_shown2(64)
            on_release: app.root.get_screen("third").ids.root3.ids.R66.text=root.res_shown2(65)
            on_release: app.root.get_screen("third").ids.root3.ids.R67.text=root.res_shown2(66)
            on_release: app.root.get_screen("third").ids.root3.ids.R68.text=root.res_shown2(67)
            on_release: app.root.get_screen("third").ids.root3.ids.R69.text=root.res_shown2(68)
            on_release: app.root.get_screen("third").ids.root3.ids.R70.text=root.res_shown2(69)
            on_release: app.root.get_screen("third").ids.root3.ids.R71.text=root.res_shown2(70)
            on_release: app.root.get_screen("third").ids.root3.ids.R72.text=root.res_shown2(71)
            on_release: app.root.get_screen("third").ids.root3.ids.R73.text=root.res_shown2(72)
            on_release: app.root.get_screen("third").ids.root3.ids.R74.text=root.res_shown2(73)
            on_release: app.root.get_screen("third").ids.root3.ids.R75.text=root.res_shown2(74)
            on_release: app.root.get_screen("third").ids.root3.ids.R76.text=root.res_shown2(75)

            
        Button:
            id:res_2_button
            text: 
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_press:root.res_change(1)
            on_release:root.ids.res_2_button.text=root.res_change(0)
            on_release:app.root.get_screen("third").ids.root3.ids.res_3_button.text=root.res_change(0)
            on_release: root.ids.R1.text=root.res_shown2(0)
            on_release: root.ids.R2.text=root.res_shown2(1)
            on_release: root.ids.R3.text=root.res_shown2(2)
            on_release: root.ids.R4.text=root.res_shown2(3)
            on_release: root.ids.R5.text=root.res_shown2(4)
            on_release: root.ids.R6.text=root.res_shown2(5)
            on_release: root.ids.R7.text=root.res_shown2(6)
            on_release: root.ids.R8.text=root.res_shown2(7)
            on_release: root.ids.R9.text=root.res_shown2(8)
            on_release: root.ids.R10.text=root.res_shown2(9)
            on_release: root.ids.R11.text=root.res_shown2(10)
            on_release: root.ids.R12.text=root.res_shown2(11)
            on_release: root.ids.R13.text=root.res_shown2(12)
            on_release: root.ids.R14.text=root.res_shown2(13)
            on_release: root.ids.R15.text=root.res_shown2(14)
            on_release: root.ids.R16.text=root.res_shown2(15)
            on_release: root.ids.R17.text=root.res_shown2(16)
            on_release: root.ids.R18.text=root.res_shown2(17)
            on_release: root.ids.R19.text=root.res_shown2(18)
            on_release: root.ids.R20.text=root.res_shown2(19)
            on_release: root.ids.R21.text=root.res_shown2(20)
            on_release: root.ids.R22.text=root.res_shown2(21)
            on_release: root.ids.R23.text=root.res_shown2(22)
            on_release: root.ids.R24.text=root.res_shown2(23)
            on_release: root.ids.R25.text=root.res_shown2(24)
            on_release: root.ids.R26.text=root.res_shown2(25)
            on_release: root.ids.R27.text=root.res_shown2(26)
            on_release: root.ids.R28.text=root.res_shown2(27)
            on_release: root.ids.R29.text=root.res_shown2(28)
            on_release: root.ids.R30.text=root.res_shown2(29)
            on_release: root.ids.R31.text=root.res_shown2(30)
            on_release: root.ids.R32.text=root.res_shown2(31)
            on_release: root.ids.R33.text=root.res_shown2(32)
            on_release: root.ids.R34.text=root.res_shown2(33)
            on_release: root.ids.R35.text=root.res_shown2(34)
            on_release: root.ids.R36.text=root.res_shown2(35)
            on_release: root.ids.R37.text=root.res_shown2(36)
            on_release: root.ids.R38.text=root.res_shown2(37)
            on_release: app.root.get_screen("third").ids.root3.ids.R39.text=root.res_shown2(38)
            on_release: app.root.get_screen("third").ids.root3.ids.R40.text=root.res_shown2(39)
            on_release: app.root.get_screen("third").ids.root3.ids.R41.text=root.res_shown2(40)
            on_release: app.root.get_screen("third").ids.root3.ids.R42.text=root.res_shown2(41)
            on_release: app.root.get_screen("third").ids.root3.ids.R43.text=root.res_shown2(42)
            on_release: app.root.get_screen("third").ids.root3.ids.R44.text=root.res_shown2(43)
            on_release: app.root.get_screen("third").ids.root3.ids.R45.text=root.res_shown2(44)
            on_release: app.root.get_screen("third").ids.root3.ids.R46.text=root.res_shown2(45)
            on_release: app.root.get_screen("third").ids.root3.ids.R47.text=root.res_shown2(46)
            on_release: app.root.get_screen("third").ids.root3.ids.R48.text=root.res_shown2(47)
            on_release: app.root.get_screen("third").ids.root3.ids.R49.text=root.res_shown2(48)
            on_release: app.root.get_screen("third").ids.root3.ids.R50.text=root.res_shown2(49)
            on_release: app.root.get_screen("third").ids.root3.ids.R51.text=root.res_shown2(50)
            on_release: app.root.get_screen("third").ids.root3.ids.R52.text=root.res_shown2(51)
            on_release: app.root.get_screen("third").ids.root3.ids.R53.text=root.res_shown2(52)
            on_release: app.root.get_screen("third").ids.root3.ids.R54.text=root.res_shown2(53)
            on_release: app.root.get_screen("third").ids.root3.ids.R55.text=root.res_shown2(54)
            on_release: app.root.get_screen("third").ids.root3.ids.R56.text=root.res_shown2(55)
            on_release: app.root.get_screen("third").ids.root3.ids.R57.text=root.res_shown2(56)
            on_release: app.root.get_screen("third").ids.root3.ids.R58.text=root.res_shown2(57)
            on_release: app.root.get_screen("third").ids.root3.ids.R59.text=root.res_shown2(58)
            on_release: app.root.get_screen("third").ids.root3.ids.R60.text=root.res_shown2(59)
            on_release: app.root.get_screen("third").ids.root3.ids.R61.text=root.res_shown2(60)
            on_release: app.root.get_screen("third").ids.root3.ids.R62.text=root.res_shown2(61)
            on_release: app.root.get_screen("third").ids.root3.ids.R63.text=root.res_shown2(62)
            on_release: app.root.get_screen("third").ids.root3.ids.R64.text=root.res_shown2(63)
            on_release: app.root.get_screen("third").ids.root3.ids.R65.text=root.res_shown2(64)
            on_release: app.root.get_screen("third").ids.root3.ids.R66.text=root.res_shown2(65)
            on_release: app.root.get_screen("third").ids.root3.ids.R67.text=root.res_shown2(66)
            on_release: app.root.get_screen("third").ids.root3.ids.R68.text=root.res_shown2(67)
            on_release: app.root.get_screen("third").ids.root3.ids.R69.text=root.res_shown2(68)
            on_release: app.root.get_screen("third").ids.root3.ids.R70.text=root.res_shown2(69)
            on_release: app.root.get_screen("third").ids.root3.ids.R71.text=root.res_shown2(70)
            on_release: app.root.get_screen("third").ids.root3.ids.R72.text=root.res_shown2(71)
            on_release: app.root.get_screen("third").ids.root3.ids.R73.text=root.res_shown2(72)
            on_release: app.root.get_screen("third").ids.root3.ids.R74.text=root.res_shown2(73)
            on_release: app.root.get_screen("third").ids.root3.ids.R75.text=root.res_shown2(74)
            on_release: app.root.get_screen("third").ids.root3.ids.R76.text=root.res_shown2(75)
<ThirdScreen>:
    CustomLayout6:
    RootWidget3:
        id:root3
<CustomLayout6>
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            texture: self.background_image.texture
            pos: self.pos
            size: self.size
<RootWidget3>:
    CustomLayout7:
        size_hint: 1.0, 1.0
        pos_hint: {'center_x': .5, 'center_y': .5}
        rows:20
        cols:4
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R39'
            halign: 'left'
        TextInput:
            id:R39
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R40'
            halign: 'left'
        TextInput:
            id:R40
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R41'
            halign: 'left'
        TextInput:
            id:R41
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R42'
            halign: 'left'
        TextInput:
            id:R42
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R43'
            halign: 'left'
        TextInput:
            id:R43
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R44'
            halign: 'left'
        TextInput:
            id:R44
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R45'
            halign: 'left'
        TextInput:
            id:R45
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R46'
            halign: 'left'
        TextInput:
            id:R46
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R47'
            halign: 'left'
        TextInput:
            id:R47
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R48'
            halign: 'left'
        TextInput:
            id:R48
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R49'
            halign: 'left'
        TextInput:
            id:R49
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R50'
            halign: 'left'
        TextInput:
            id:R50
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R51'
            halign: 'left'
        TextInput:
            id:R51
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R52'
            halign: 'left'
        TextInput:
            id:R52
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R53'
            halign: 'left'
        TextInput:
            id:R53
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R54'
            halign: 'left'
        TextInput:
            id:R54
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R55'
            halign: 'left'
        TextInput:
            id:R55
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R56'
            halign: 'left'
        TextInput:
            id:R56
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'

        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R57'
            halign: 'left'
        TextInput:
            id:R57
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R58'
            halign: 'left'
        TextInput:
            id:R58
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R59'
            halign: 'left'
        TextInput:
            id:R59
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R60'
            halign: 'left'
        TextInput:
            id:R60
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R61'
            halign: 'left'
        TextInput:
            id:R61
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R62'
            halign: 'left'
        TextInput:
            id:R62
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R63'
            halign: 'left'
        TextInput:
            id:R63
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R64'
            halign: 'left'
        TextInput:
            id:R64
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R65'
            halign: 'left'
        TextInput:
            id:R65
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R66'
            halign: 'left'
        TextInput:
            id:R66
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R67'
            halign: 'left'
        TextInput:
            id:R67
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R68'
            halign: 'left'
        TextInput:
            id:R68
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R69'
            halign: 'left'
        TextInput:
            id:R69
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R70'
            halign: 'left'
        TextInput:
            id:R70
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R71'
            halign: 'left'
        TextInput:
            id:R71
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R72'
            halign: 'left'
        TextInput:
            id:R72
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R73'
            halign: 'left'
        TextInput:
            id:R73
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R74'
            halign: 'left'
        TextInput:
            id:R74
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R75'
            halign: 'left'
        TextInput:
            id:R75
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Label:
            text_size: self.width-20, self.height
            font_size: 30
            text:'R76'
            halign: 'left'
        TextInput:
            id:R76
            text_size: self.width-20, self.height
            font_size: 30
            halign: 'right'
        Button:
            text: 'HOME'
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_release: app.root.current ='first'
            on_release: app.root.get_screen("first").ids.root1.ids.res_1206.state=root.button_state(0)
            on_release: app.root.get_screen("first").ids.root1.ids.res_0805.state=root.button_state(1)
        Button:
            text: 'Privious'
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_release: app.root.current ='second'
        Button:
            text: 'SAVE'
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R1.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R2.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R3.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R4.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R5.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R6.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R7.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R8.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R9.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R10.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R11.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R12.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R13.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R14.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R15.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R16.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R17.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R18.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R19.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R20.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R21.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R22.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R23.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R24.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R25.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R26.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R27.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R28.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R29.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R30.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R31.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R32.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R33.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R34.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R35.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R36.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R37.text)
            on_press:root.res_save_onpress(app.root.get_screen("second").ids.root2.ids.R38.text)
            on_press:root.res_save_onpress(root.ids.R39.text)
            on_press:root.res_save_onpress(root.ids.R40.text)
            on_press:root.res_save_onpress(root.ids.R41.text)
            on_press:root.res_save_onpress(root.ids.R42.text)
            on_press:root.res_save_onpress(root.ids.R43.text)
            on_press:root.res_save_onpress(root.ids.R44.text)
            on_press:root.res_save_onpress(root.ids.R45.text)
            on_press:root.res_save_onpress(root.ids.R46.text)
            on_press:root.res_save_onpress(root.ids.R47.text)
            on_press:root.res_save_onpress(root.ids.R48.text)
            on_press:root.res_save_onpress(root.ids.R49.text)
            on_press:root.res_save_onpress(root.ids.R50.text)
            on_press:root.res_save_onpress(root.ids.R51.text)
            on_press:root.res_save_onpress(root.ids.R52.text)
            on_press:root.res_save_onpress(root.ids.R53.text)
            on_press:root.res_save_onpress(root.ids.R54.text)
            on_press:root.res_save_onpress(root.ids.R55.text)
            on_press:root.res_save_onpress(root.ids.R56.text)
            on_press:root.res_save_onpress(root.ids.R57.text)
            on_press:root.res_save_onpress(root.ids.R58.text)
            on_press:root.res_save_onpress(root.ids.R59.text)
            on_press:root.res_save_onpress(root.ids.R60.text)
            on_press:root.res_save_onpress(root.ids.R61.text)
            on_press:root.res_save_onpress(root.ids.R62.text)
            on_press:root.res_save_onpress(root.ids.R63.text)
            on_press:root.res_save_onpress(root.ids.R64.text)
            on_press:root.res_save_onpress(root.ids.R65.text)
            on_press:root.res_save_onpress(root.ids.R66.text)
            on_press:root.res_save_onpress(root.ids.R67.text)
            on_press:root.res_save_onpress(root.ids.R68.text)
            on_press:root.res_save_onpress(root.ids.R69.text)
            on_press:root.res_save_onpress(root.ids.R70.text)
            on_press:root.res_save_onpress(root.ids.R71.text)
            on_press:root.res_save_onpress(root.ids.R72.text)
            on_press:root.res_save_onpress(root.ids.R73.text)
            on_press:root.res_save_onpress(root.ids.R74.text)
            on_press:root.res_save_onpress(root.ids.R75.text)
            on_press:root.res_save_onpress(root.ids.R76.text)
            on_release: app.root.get_screen("second").ids.root2.ids.R1.text=root.res_shown2(0)
            on_release: app.root.get_screen("second").ids.root2.ids.R2.text=root.res_shown2(1)
            on_release: app.root.get_screen("second").ids.root2.ids.R3.text=root.res_shown2(2)
            on_release: app.root.get_screen("second").ids.root2.ids.R4.text=root.res_shown2(3)
            on_release: app.root.get_screen("second").ids.root2.ids.R5.text=root.res_shown2(4)
            on_release: app.root.get_screen("second").ids.root2.ids.R6.text=root.res_shown2(5)
            on_release: app.root.get_screen("second").ids.root2.ids.R7.text=root.res_shown2(6)
            on_release: app.root.get_screen("second").ids.root2.ids.R8.text=root.res_shown2(7)
            on_release: app.root.get_screen("second").ids.root2.ids.R9.text=root.res_shown2(8)
            on_release: app.root.get_screen("second").ids.root2.ids.R10.text=root.res_shown2(9)
            on_release: app.root.get_screen("second").ids.root2.ids.R11.text=root.res_shown2(10)
            on_release: app.root.get_screen("second").ids.root2.ids.R12.text=root.res_shown2(11)
            on_release: app.root.get_screen("second").ids.root2.ids.R13.text=root.res_shown2(12)
            on_release: app.root.get_screen("second").ids.root2.ids.R14.text=root.res_shown2(13)
            on_release: app.root.get_screen("second").ids.root2.ids.R15.text=root.res_shown2(14)
            on_release: app.root.get_screen("second").ids.root2.ids.R16.text=root.res_shown2(15)
            on_release: app.root.get_screen("second").ids.root2.ids.R17.text=root.res_shown2(16)
            on_release: app.root.get_screen("second").ids.root2.ids.R18.text=root.res_shown2(17)
            on_release: app.root.get_screen("second").ids.root2.ids.R19.text=root.res_shown2(18)
            on_release: app.root.get_screen("second").ids.root2.ids.R20.text=root.res_shown2(19)
            on_release: app.root.get_screen("second").ids.root2.ids.R21.text=root.res_shown2(20)
            on_release: app.root.get_screen("second").ids.root2.ids.R22.text=root.res_shown2(21)
            on_release: app.root.get_screen("second").ids.root2.ids.R23.text=root.res_shown2(22)
            on_release: app.root.get_screen("second").ids.root2.ids.R24.text=root.res_shown2(23)
            on_release: app.root.get_screen("second").ids.root2.ids.R25.text=root.res_shown2(24)
            on_release: app.root.get_screen("second").ids.root2.ids.R26.text=root.res_shown2(25)
            on_release: app.root.get_screen("second").ids.root2.ids.R27.text=root.res_shown2(26)
            on_release: app.root.get_screen("second").ids.root2.ids.R28.text=root.res_shown2(27)
            on_release: app.root.get_screen("second").ids.root2.ids.R29.text=root.res_shown2(28)
            on_release: app.root.get_screen("second").ids.root2.ids.R30.text=root.res_shown2(29)
            on_release: app.root.get_screen("second").ids.root2.ids.R31.text=root.res_shown2(30)
            on_release: app.root.get_screen("second").ids.root2.ids.R32.text=root.res_shown2(31)
            on_release: app.root.get_screen("second").ids.root2.ids.R33.text=root.res_shown2(32)
            on_release: app.root.get_screen("second").ids.root2.ids.R34.text=root.res_shown2(33)
            on_release: app.root.get_screen("second").ids.root2.ids.R35.text=root.res_shown2(34)
            on_release: app.root.get_screen("second").ids.root2.ids.R36.text=root.res_shown2(35)
            on_release: app.root.get_screen("second").ids.root2.ids.R37.text=root.res_shown2(36)
            on_release: app.root.get_screen("second").ids.root2.ids.R38.text=root.res_shown2(37)
            on_release: root.ids.R39.text=root.res_shown2(38)
            on_release: root.ids.R40.text=root.res_shown2(39)
            on_release: root.ids.R41.text=root.res_shown2(40)
            on_release: root.ids.R42.text=root.res_shown2(41)
            on_release: root.ids.R43.text=root.res_shown2(42)
            on_release: root.ids.R44.text=root.res_shown2(43)
            on_release: root.ids.R45.text=root.res_shown2(44)
            on_release: root.ids.R46.text=root.res_shown2(45)
            on_release: root.ids.R47.text=root.res_shown2(46)
            on_release: root.ids.R48.text=root.res_shown2(47)
            on_release: root.ids.R49.text=root.res_shown2(48)
            on_release: root.ids.R50.text=root.res_shown2(49)
            on_release: root.ids.R51.text=root.res_shown2(50)
            on_release: root.ids.R52.text=root.res_shown2(51)
            on_release: root.ids.R53.text=root.res_shown2(52)
            on_release: root.ids.R54.text=root.res_shown2(53)
            on_release: root.ids.R55.text=root.res_shown2(54)
            on_release: root.ids.R56.text=root.res_shown2(55)
            on_release: root.ids.R57.text=root.res_shown2(56)
            on_release: root.ids.R58.text=root.res_shown2(57)
            on_release: root.ids.R59.text=root.res_shown2(58)
            on_release: root.ids.R60.text=root.res_shown2(59)
            on_release: root.ids.R61.text=root.res_shown2(60)
            on_release: root.ids.R62.text=root.res_shown2(61)
            on_release: root.ids.R63.text=root.res_shown2(62)
            on_release: root.ids.R64.text=root.res_shown2(63)
            on_release: root.ids.R65.text=root.res_shown2(64)
            on_release: root.ids.R66.text=root.res_shown2(65)
            on_release: root.ids.R67.text=root.res_shown2(66)
            on_release: root.ids.R68.text=root.res_shown2(67)
            on_release: root.ids.R69.text=root.res_shown2(68)
            on_release: root.ids.R70.text=root.res_shown2(69)
            on_release: root.ids.R71.text=root.res_shown2(70)
            on_release: root.ids.R72.text=root.res_shown2(71)
            on_release: root.ids.R73.text=root.res_shown2(72)
            on_release: root.ids.R74.text=root.res_shown2(73)
            on_release: root.ids.R75.text=root.res_shown2(74)
            on_release: root.ids.R76.text=root.res_shown2(75)
        Button:
            id:res_3_button
            text: 
            font_size: 30
            background_color:1.3,1.98,2.18,1
            on_press: root.res_change(1)
            on_release: root.ids.res_3_button.text=root.res_change(0)
            on_release: app.root.get_screen("second").ids.root2.ids.res_2_button.text=root.res_change(0)
            on_release: app.root.get_screen("second").ids.root2.ids.R1.text=root.res_shown2(0)
            on_release: app.root.get_screen("second").ids.root2.ids.R2.text=root.res_shown2(1)
            on_release: app.root.get_screen("second").ids.root2.ids.R3.text=root.res_shown2(2)
            on_release: app.root.get_screen("second").ids.root2.ids.R4.text=root.res_shown2(3)
            on_release: app.root.get_screen("second").ids.root2.ids.R5.text=root.res_shown2(4)
            on_release: app.root.get_screen("second").ids.root2.ids.R6.text=root.res_shown2(5)
            on_release: app.root.get_screen("second").ids.root2.ids.R7.text=root.res_shown2(6)
            on_release: app.root.get_screen("second").ids.root2.ids.R8.text=root.res_shown2(7)
            on_release: app.root.get_screen("second").ids.root2.ids.R9.text=root.res_shown2(8)
            on_release: app.root.get_screen("second").ids.root2.ids.R10.text=root.res_shown2(9)
            on_release: app.root.get_screen("second").ids.root2.ids.R11.text=root.res_shown2(10)
            on_release: app.root.get_screen("second").ids.root2.ids.R12.text=root.res_shown2(11)
            on_release: app.root.get_screen("second").ids.root2.ids.R13.text=root.res_shown2(12)
            on_release: app.root.get_screen("second").ids.root2.ids.R14.text=root.res_shown2(13)
            on_release: app.root.get_screen("second").ids.root2.ids.R15.text=root.res_shown2(14)
            on_release: app.root.get_screen("second").ids.root2.ids.R16.text=root.res_shown2(15)
            on_release: app.root.get_screen("second").ids.root2.ids.R17.text=root.res_shown2(16)
            on_release: app.root.get_screen("second").ids.root2.ids.R18.text=root.res_shown2(17)
            on_release: app.root.get_screen("second").ids.root2.ids.R19.text=root.res_shown2(18)
            on_release: app.root.get_screen("second").ids.root2.ids.R20.text=root.res_shown2(19)
            on_release: app.root.get_screen("second").ids.root2.ids.R21.text=root.res_shown2(20)
            on_release: app.root.get_screen("second").ids.root2.ids.R22.text=root.res_shown2(21)
            on_release: app.root.get_screen("second").ids.root2.ids.R23.text=root.res_shown2(22)
            on_release: app.root.get_screen("second").ids.root2.ids.R24.text=root.res_shown2(23)
            on_release: app.root.get_screen("second").ids.root2.ids.R25.text=root.res_shown2(24)
            on_release: app.root.get_screen("second").ids.root2.ids.R26.text=root.res_shown2(25)
            on_release: app.root.get_screen("second").ids.root2.ids.R27.text=root.res_shown2(26)
            on_release: app.root.get_screen("second").ids.root2.ids.R28.text=root.res_shown2(27)
            on_release: app.root.get_screen("second").ids.root2.ids.R29.text=root.res_shown2(28)
            on_release: app.root.get_screen("second").ids.root2.ids.R30.text=root.res_shown2(29)
            on_release: app.root.get_screen("second").ids.root2.ids.R31.text=root.res_shown2(30)
            on_release: app.root.get_screen("second").ids.root2.ids.R32.text=root.res_shown2(31)
            on_release: app.root.get_screen("second").ids.root2.ids.R33.text=root.res_shown2(32)
            on_release: app.root.get_screen("second").ids.root2.ids.R34.text=root.res_shown2(33)
            on_release: app.root.get_screen("second").ids.root2.ids.R35.text=root.res_shown2(34)
            on_release: app.root.get_screen("second").ids.root2.ids.R36.text=root.res_shown2(35)
            on_release: app.root.get_screen("second").ids.root2.ids.R37.text=root.res_shown2(36)
            on_release: app.root.get_screen("second").ids.root2.ids.R38.text=root.res_shown2(37)
            on_release: root.ids.R39.text=root.res_shown2(38)
            on_release: root.ids.R40.text=root.res_shown2(39)
            on_release: root.ids.R41.text=root.res_shown2(40)
            on_release: root.ids.R42.text=root.res_shown2(41)
            on_release: root.ids.R43.text=root.res_shown2(42)
            on_release: root.ids.R44.text=root.res_shown2(43)
            on_release: root.ids.R45.text=root.res_shown2(44)
            on_release: root.ids.R46.text=root.res_shown2(45)
            on_release: root.ids.R47.text=root.res_shown2(46)
            on_release: root.ids.R48.text=root.res_shown2(47)
            on_release: root.ids.R49.text=root.res_shown2(48)
            on_release: root.ids.R50.text=root.res_shown2(49)
            on_release: root.ids.R51.text=root.res_shown2(50)
            on_release: root.ids.R52.text=root.res_shown2(51)
            on_release: root.ids.R53.text=root.res_shown2(52)
            on_release: root.ids.R54.text=root.res_shown2(53)
            on_release: root.ids.R55.text=root.res_shown2(54)
            on_release: root.ids.R56.text=root.res_shown2(55)
            on_release: root.ids.R57.text=root.res_shown2(56)
            on_release: root.ids.R58.text=root.res_shown2(57)
            on_release: root.ids.R59.text=root.res_shown2(58)
            on_release: root.ids.R60.text=root.res_shown2(59)
            on_release: root.ids.R61.text=root.res_shown2(60)
            on_release: root.ids.R62.text=root.res_shown2(61)
            on_release: root.ids.R63.text=root.res_shown2(62)
            on_release: root.ids.R64.text=root.res_shown2(63)
            on_release: root.ids.R65.text=root.res_shown2(64)
            on_release: root.ids.R66.text=root.res_shown2(65)
            on_release: root.ids.R67.text=root.res_shown2(66)
            on_release: root.ids.R68.text=root.res_shown2(67)
            on_release: root.ids.R69.text=root.res_shown2(68)
            on_release: root.ids.R70.text=root.res_shown2(69)
            on_release: root.ids.R71.text=root.res_shown2(70)
            on_release: root.ids.R72.text=root.res_shown2(71)
            on_release: root.ids.R73.text=root.res_shown2(72)
            on_release: root.ids.R74.text=root.res_shown2(73)
            on_release: root.ids.R75.text=root.res_shown2(74)
            on_release: root.ids.R76.text=root.res_shown2(75)
''')



##class MainApp(App):
##
##    def build(self):
##            return RootWidget()

if __name__ == '__main__':
    Res_fun().read_text()
    MainApp().run()
