#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import string
import time
import hashlib
import json
import os, sys
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('自助翻译软件 Verson1.0.0')
        self.master.geometry('567x442')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.Text1 = Entry(font=('宋体',9))
        self.Text1.place(relx=0.014, rely=0.09, relwidth=0.975, relheight=0.328)
        self.Text2Var = StringVar()
        self.style.configure('Command1.TButton',font=('宋体',9))
        self.Command1 = Button(self.top, text='点我翻译（百度翻译接口）', command=self.Command1_Cmd, style='Command1.TButton')
        self.Command1.place(relx=0., rely=0.434, relwidth=0.298, relheight=0.129)

        self.Text2 = Entry(textvariable=self.Text2Var, font=('宋体',9))
        self.Text2.place(relx=0.014, rely=0.652, relwidth=0.975, relheight=0.328)

        self.style.configure('Label3.TLabel',anchor='w', font=('宋体',9))
        self.Label3 = Label(self.top, text='提示：暂时只支持中英文互译，每秒请求次数为1次。本版本为初始版本', style='Label3.TLabel')
        self.Label3.place(relx=0.325, rely=0.471, relwidth=0.651, relheight=0.075)

        self.style.configure('Label2.TLabel',anchor='w', font=('宋体',9))
        self.Label2 = Label(self.top, text='翻译结果：', style='Label2.TLabel')
        self.Label2.place(relx=0.042, rely=0.597, relwidth=0.439, relheight=0.038)

        self.style.configure('Label1.TLabel',anchor='w', font=('宋体',9))
        self.Label1 = Label(self.top, text='请输入你需要翻译的文本', style='Label1.TLabel')
        self.Label1.place(relx=0.028, rely=0.018, relwidth=1.131, relheight=0.038)
    def Command1_Cmd(self):
        #TODO, Please finish the function here!
        word = self.Text1.get()
        ans= requests_for_dst(word)
        if ans:
            self.Text2Var.set(ans)

#class trans(Application_ui): 
#init
  
 
def requests_for_dst(word): #,createWidgets
    #init salt and final_sign
    api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    my_appid = 'APPID'
    cyber = '密钥'
    lower_case = set("".join(string.ascii_lowercase)+"".join(string.ascii_lowercase).upper())
    salt = str(time.time())[:10]
    final_sign = str(my_appid)+word+salt+cyber
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    #区别en,zh构造请求参数
    if set(word) & lower_case:
        print(set(word) | lower_case)
        print(lower_case)
        paramas = {
            'q':word,
            'from':'en',
            'to':'zh',
            'appid':'%s'%my_appid,
            'salt':'%s'%salt,
            'sign':'%s'%final_sign
            }
        my_url = api_url+'?appid='+str(my_appid)+'&q='+word+'&from='+'en'+'&to='+'zh'+'&salt='+salt+'&sign='+final_sign
    else:
        paramas = {
            'q':word,
            'from':'zh',
            'to':'en',
            'appid':'%s'%my_appid,
            'salt':'%s'%salt,
            'sign':'%s'%final_sign
            }
        my_url = api_url+'?appid='+str(my_appid)+'&q='+word+'&from='+'zh'+'&to='+'en'+'&salt='+salt+'&sign='+final_sign
    response = requests.get(api_url,params = paramas).content
    content = str(response,encoding = "utf-8")
    json_reads = json.loads(content)
    print(json_reads)
    if 'trans_result' in json_reads:
        return json_reads['trans_result'][0]['dst']
    else:
        return False
 



class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    
if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    

    try:
        top.destroy()
    except:
        pass
    





    
