# -*-coding:utf-8-*-
import os
global s2
s2={}
class Binary_search(object):    
    def __init__(self, search_value,list1):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        # 设置属性
        self.search_value = search_value
        self.list1 = list1
        for i in range(len(list1)):
            self.list1[i]=float(list1[i])
    def search(self):
        #global res_back
          left=0
          D_value=0
          if(self.search_value>self.list1[len(self.list1)-1]) :
              return self.list1[len(self.list1)-1],format(self.search_value-self.list1[len(self.list1)-1],'.3f'),len(self.list1)-1
          elif(self.search_value<0):
              return 0,0,0
          if self.list1 is not None:
              right=len(self.list1)
          else:
              right=0
          while(left <= right):
              mid=int((left+right)/2)
              if self.list1[mid]>self.search_value:
                      right = mid - 1
              elif self.list1[mid]<self.search_value:
                      left = mid + 1
              else:
                  break
          if(right<0):
                      right = 0
          if(left>len(self.list1)):
              left=len(self.list1)
          if (left <= right):
              return self.list1[mid],D_value,mid
          else:
             k=(self.list1[left]+self.list1[right])/2
             if(self.search_value>=k):
                 return self.list1[left],format(self.list1[left]-self.search_value,'.3f'),left
             else:
                 return self.list1[right],format(self.list1[right]-self.search_value,'.3f'),right                  
class Res(object):   
    def __init__(self, Res_value,Res_Category):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        # 设置属性
        global s2
        self.s1={}
        self.Res_value = Res_value
        self.Res_Category = Res_Category
        open_txt().open(str(self.Res_Category))
        for i in range(len(s2)):
            self.s1[i]=s2[i][1]
    def Res_value_one(self):
        s=Binary_search(self.Res_value,self.s1).search()
        return s
    def Res_value_two(self): 
        s=Binary_search(self.Res_value,self.s1).search()
        i=0
        p=0
        z={}
        m={}
        n={}
        t=9999
        #(s[2]-1+i)<len(s2)
        while( (s[2]-1+i)>=0 and (s[2]-1+i)<len(s2) and 2*self.Res_value<=float(self.s1[len(s2)-1])):
            if(float(self.s1[s[2]-1+i])>self.Res_value and float(self.s1[s[2]-1+i])<=2*self.Res_value):
                r=float(self.s1[s[2]-1+i])*self.Res_value/(float(self.s1[s[2]-1+i])-self.Res_value)
                k=Binary_search(r,self.s1).search()
                r1=float(self.s1[s[2]-1+i])*k[0]/(float(self.s1[s[2]-1+i])+k[0])
                if(abs(r1-self.Res_value)<abs(t)):
                    t=r1-self.Res_value
                    m=float(self.s1[s[2]-1+i])
                    n=k[0]
                    p=s[2]-1+i
            i+=1
        if m:
            return m,n,format(t,'.3f'),p
        else:
            return
    def Res_value_three(self):
        z=Res(self.Res_value,self.Res_Category).Res_value_one()
        i=0
        t=9999
        m={}
        n={}
        p={}
        #float(self.s1[z[2]-1+i])
        while ((z[2]-1+i)>=0 and 3*self.Res_value<=float(self.s1[len(s2)-1]) and (z[2]-1+i)<len(s2) ):
            #print (float(self.s1[z[2]-1+i]))
            if(float(self.s1[z[2]-1+i])>self.Res_value and float(self.s1[z[2]-1+i])<=3*self.Res_value):
                a=float(self.s1[z[2]-1+i])*self.Res_value/(float(self.s1[z[2]-1+i])-self.Res_value)
                b=Res(a,self.Res_Category).Res_value_two()
                if (b is not None ):
                    t1=float(self.s1[z[2]-1+i])*b[0]*b[1]/(float(self.s1[z[2]-1+i])*b[0]+float(self.s1[z[2]-1+i])*b[1]+b[0]*b[1])-self.Res_value
                    if(abs(t1)<abs(t)):
                        t=t1
                        m=float(self.s1[z[2]-1+i])
                        n=b[0]
                        p=b[1]
            i=i+1
        if m:
            return m,n,p,format(t,'.3f')
        else:
            return
           
class open_txt(object):
    def __init__(self):
        #路径调用，否者会出现找不到文件，闪退
        cur_dir1 = os.path.dirname(os.path.abspath(__file__))
        self.path1 = os.path.join(os.path.abspath(cur_dir1 + os.path.sep + "./src"), "1206.txt")
        self.path2 = os.path.join(os.path.abspath(cur_dir1 + os.path.sep + "./src"), "0805.txt") 
    def open(self,file_name):
        try:
            if (str(file_name)=='0805'):
                dianzu = open(self.path2,'r')
            elif(str(file_name)=='1206'):
                dianzu = open(self.path1,'r')
            else:
                return
            s=dianzu.readlines()
            for i in range(len(s)):
                if('\n' in s):
                    s[i] = s[i].replace('\n', '')  # 替换换行符
            for i in range(len(s)):
                if('' in s):
                    s.remove('')
            # 使用 for 循环，将读到的内容，打印出来
        ##    num = 1
        ##    for con in dianzu:
            global s2
            #打开的文件不能为空
            if  len(s)!=0:
                for i in range(len(s)):
                    s[i]=list(filter(lambda x:x!='\t',s[i].split('\t')))
                for i in range(len(s)):
                    s[i][1]=s[i][1].strip()
                s2=s
            else:
                for i in range(50):
                    s2[i]=['R'+str(i+1),i] 
        # 最后需要将文件关闭
        finally:
##            print('出问题了')
            # 最后需要将文件关闭
            dianzu.close()
        return s2
class write_txt(object):
    def __init__(self):
        pass
    def open(self,file_name,number):
        try:
            if number.replace(".",'').isdigit():
                if number.count(".")==0:
                    pass
                elif number.count(".")==1:
                    pass
                else :
                    number=''
            else:pass
            ss=open_txt().open(str(file_name))
            if (str(file_name)=='0805'):
                dianzu1 = open('./src/0805.txt', 'w')
            elif(str(file_name)=='1206'):
                dianzu1 = open('./src/1206.txt', 'w')
            else:
                return
            k={}
            j=0
            i=0
##            for i in range(len(ss)-1):
##                s[i]=ss[i][1]
##            if(m.get(float(number)) is not None):
##                for i in range(len(ss)):
##                    k[i]=ss[i][1]
##            else:
            while( i<len(ss)):
                 k[i+j]=ss[i][1]
                 if((i+1)<len(ss)):
                     if(float( number)>float(ss[i][1]) and float(ss[i+1][1])>float(number)):
                         k[i+1]=number
                         k[i+2]=ss[i+1][1]
                         j=1
                         i=i+1
                 i=i+1
            if(len(ss)>0):
              if(j!=1 and float(number)>float(ss[len(ss)-1][1]) and len(k)==len(ss) ):
                 k[len(k)]=number
            for i in range(len(k)):
                dianzu1.write('R'+str(i+1)+'\t'+str(k[i])+'\n')
            #dianzu1.write('\n')
##            dianzu1.write('R'+str(len(k))+'\t'+str(k[len(k)])+'\n')
            
        finally:
           dianzu1.close()
        return k
if __name__ == '__main__':
    #m=Res(1000,'0805').Res_value_one()
    #m=Res(0.01).Res_value_two()
    
    #m=Res(5).Res_value_three()
    m=open_txt().open('1206')
    #m=write_txt().open('0805','3000')
    print(m)
