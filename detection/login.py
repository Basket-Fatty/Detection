import tkinter
import tkinter.messagebox
import os
import os.path
from tkinter.ttk import Style

import detection
import pymysql
import sqlite3

db_sqlite = True

# 定义要执行的创建表的SQL语句
if db_sqlite:
    login_sql = """
                CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY auto_increment,
                name varchar(20) NOT NULL,
                password varchar(20) NOT NULL
                );
           """
else:
    login_sql = """
                CREATE TABLE IF NOT EXISTS user(
                id INT auto_increment PRIMARY KEY,
                name varchar(20) not null,
                password varchar(20) not null
                )ENGINE=innodb DEFAULT CHARSET=utf8;
           """

# 获取当前工作目录
path = os.getcwd()
# 连接两个path
filename = os.path.join(path, 'info.txt')

# 创建应用程序
root = tkinter.Tk()
# 设置窗口的标题
root.title('Login')
# 设置窗口大小
root['height'] = 300
root['width'] = 600

Title = tkinter.Label(root, text='Advertising Identification',bg='#ffffff',fg='#5F8A95', font=("Sonder", 20), justify=tkinter.RIGHT,
                      anchor='e', width=200)
# 显示该组件的位置及大小
Title.place(x=90, y=30, width=400, height=30)

# 在窗口上创建标签组件（User Name）
# 各个参数的解释：       text设置文本内容    fg='设置字体颜色'    bg='设置字体背景'    font=("设置字体",设置字体大小)    justify=文本标签对齐的方式    anchor='文本对其方式', width=设置的宽度
labeName = tkinter.Label(root, text='User name：',bg='#ffffff', fg='#5F8A95',font=("Sonder", 16), justify=tkinter.RIGHT, anchor='e', width=80)
# 显示该组件的位置及大小
labeName.place(x=120, y=80, width=125, height=25)

# 创建字符串变量和文本框组件，同时设置关联的变量
varName = tkinter.StringVar(root, value='')
entryName = tkinter.Entry(root, width=80, textvariable=varName)
entryName.place(x=250, y=80, width=180, height=25)

# 在窗口上创建标签组件（User Pwd）
labeName = tkinter.Label(root, text='Password：', bg='#ffffff',fg='#5F8A95',font=("Sonder", 16), justify=tkinter.RIGHT, anchor='e', width=80)
# 显示该组件的位置及大小
labeName.place(x=120, y=120, width=125, height=25)

# 创建密码文本框,同时设置关联的变量
varPwd = tkinter.StringVar(root, value='')
entryPwd = tkinter.Entry(root, show='*', width=80, textvariable=varPwd)
entryPwd.place(x=250, y=120, width=180, height=25)

# 尝试自动填写用户名和密码
try:
    with open(filename) as fp:
        n, p = fp.read().strip().split(',')
        varName.set(n)
        varPwd.set(p)
except:
    pass

# 记住我，复选框
rememberMe = tkinter.IntVar(root, value=1)
# 选中时变量值为1，未选中时变量值为0，默认选中
checkRemember = tkinter.Checkbutton(root, text='Remember password', bg='#ffffff',fg='#5F8A95',font=("Sonder", 14), variable=rememberMe,
                                    onvalue=1, offvalue=0)
checkRemember.place(x=150, y=170, width=200, height=25)


# 登录按钮事件处理函数
def login():
    # 获取用户名和密码
    name = entryName.get()
    pwd = entryPwd.get()
    if name == 'admin' and pwd == '123456':
        tkinter.messagebox.showinfo(title='Congratulations', message='Successful login！')
        if rememberMe.get() == 1:
            # 把登录成功的信息写入临时文件
            with open(filename, 'w') as fp:
                fp.write(','.join((name, pwd)))
        else:
            try:
                os.remove(filename)
            except:
                pass
    else:
        tkinter.messagebox.showerror('Warning', message='Wrong user name or password')


# 登录函数
def user_login():
    # 输入框获取用户名密码
    user_name = entryName.get()
    user_password = entryPwd.get()
    # 连接login_sql数据库
    conn = {}
    if db_sqlite == False:
        conn = sqlite3.connect("detectiondb")  # 建立一个基于硬盘的数据库实例
    else:
        conn = pymysql.connect(host="localhost", user="root", password="123456", db="detectiondb", charset="utf8")
    curs = conn.cursor()
    # 执行SQL语句，创建user数据表
    curs.execute(login_sql)
    # 执行SQL语句，从user数据表中查询name和password字段值
    curs.execute("SELECT name,password FROM user")
    # 将数据库查询的结果保存在result中
    result = curs.fetchall()
    # fetchone()函数它的返回值是单个的元组, 也就是一行记录, 如果没有结果, 那就会返回null
    # fetchall()函数它的返回值是多个元组, 即返回多个行记录, 如果没有结果, 返回的是()
    # assert result, "数据库无该用户信息"   # 添加断言，判断数据库有无该用户信息，没有就直接断言错误

    # 登录账号操作
    name_list = [it[0] for it in result]  # 从数据库查询的result中遍历查询元组中第一个元素name
    # 判断用户名或密码不能为空
    if not (user_name and user_password):
        tkinter.messagebox.showwarning(title='Warning', message='User name or password cannot be empty')
    # 判断用户名和密码是否匹配
    elif user_name in name_list:
        if user_password == result[name_list.index(user_name)][1]:
            tkinter.messagebox.showinfo(title='Welcome',
                                        message='                 Success！\r\nThe current login account is：' + user_name)
            # win = tkinter.Tk()
            detection.Detection(root)
            # win.mainloop()
        else:
            tkinter.messagebox.showerror(title='False', message='Password input error')
    # 账号不在数据库中，则弹出是否注册的框
    else:
        is_signup = tkinter.messagebox.askyesno(title='Tip',
                                                message='This account does not exist. Do you want to register now?')
        if is_signup:
            user_register()


# 注册函数
def user_register():
    # 确认注册函数
    def register_confirm():
        # 获取输入框内的内容
        name = new_name.get()
        password = new_password.get()
        password_confirm = new_password_confirm.get()
        # 先在本地手动创建一个login_sql数据库，然后连接该数据库
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="detectiondb",
                               charset="utf8")
        curs = conn.cursor()

        # 注册账号操作
        try:
            # 执行SQL语句，创建user数据表
            curs.execute(login_sql)
            # 向user数据表中插入语句
            insert_sql = "INSERT INTO user(name, password) VALUES ('%s', '%s')" % (name, password)
            # 读取user数据表中的name和password字段值
            read_sql = 'select * from user where name = "' + name + '" and password = "' + password + '"'
            user_data = curs.execute(read_sql)
            # 判断注册账号和密码
            if not (name and password):
                tkinter.messagebox.showwarning(title='警告', message='注册账号或密码不能为空')
            elif password != password_confirm:
                tkinter.messagebox.showwarning(title='警告', message='两次密码输入不一致，请重新输入')
            else:
                if user_data.real:
                    tkinter.messagebox.showwarning(title='警告', message='该注册账号已存在')
                else:
                    curs.execute(insert_sql)
                    tkinter.messagebox.showinfo(title='恭喜您', message='      注册成功！\r\n注册账号为：' + name)
                    print("数据插入成功")
            # 提交到数据库执行
            conn.commit()
            curs.close()
        except IOError:
            print("数据插入失败")
            conn.rollback()
        # 关闭数据库连接
        conn.close()
        window_sign_up.destroy()

    # 注册窗口
    window_sign_up = tkinter.Toplevel(root)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Welcome to register')
    window_sign_up.configure(bg='#ffffff')

    # 注册账号及标签、输入框
    new_name = tkinter.StringVar()
    labeName = tkinter.Label(window_sign_up,text='Username ：', bg='#ffffff', fg='#5F8A95', font=("Segoe UI", 12))
    labeName.place(x=50, y=10)
    #tkinter.Label(window_sign_up, text='Username：').place(x=50, y=10)
    tkinter.Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)


    # 注册密码及标签、输入框
    new_password = tkinter.StringVar()
    labeName = tkinter.Label(window_sign_up, text='Password  ：', bg='#ffffff', fg='#5F8A95', font=("Segoe UI", 12))
    labeName.place(x=50, y=50)
    #tkinter.Label(window_sign_up, text='Password：').place(x=50, y=50)
    tkinter.Entry(window_sign_up, textvariable=new_password, show='*').place(x=150, y=50)

    # 重复密码及标签、输入框
    new_password_confirm = tkinter.StringVar()
    labeName = tkinter.Label(window_sign_up, text='Confirm    ：', bg='#ffffff', fg='#5F8A95', font=("Segoe UI", 12))
    labeName.place(x=50, y=90)
    #tkinter.Label(window_sign_up, text='Confirm：').place(x=50, y=90)
    tkinter.Entry(window_sign_up, textvariable=new_password_confirm, show='*').place(x=150, y=90)


    # 确认注册按钮及位置
    bt_confirm_sign_up = tkinter.Button(window_sign_up, text='Affirm', command=register_confirm)
    bt_confirm_sign_up.place(x=150, y=130)
    bt_confirm_sign_up.configure(bg='#3eb489', fg='#ffffff')


# 创建按钮组件，同时设置按钮事件处理函数
# 参数解释：  text='Login'文本内容      activeforeground='#ff0000'按下按钮时文字颜色     command=login关联的函数
# buttonOk = tkinter.Button(root, text='登录', activeforeground='#ff0000', command=user_login_mysql)
buttonOk = tkinter.Button(root, text='Login', activeforeground='#ff0000', bg='#3eb489',fg='#ffffff',command=user_login)
buttonOk.place(x=170, y=215, width=80, height=25)

buttonRegister = tkinter.Button(root, text='Register', activeforeground='#ff0000', bg='#3eb489',fg='#ffffff',command=user_register)
buttonRegister.place(x=250, y=215, width=80, height=25)


# 取消按钮的事件处理函数
def cancel():
    # 清空用户输入的用户名和密码
    varName.set('')
    varPwd.set('')


buttonCancel = tkinter.Button(root, text='Cancel', command=cancel,bg='#3eb489',fg='#ffffff')
buttonCancel.place(x=330, y=215, width=80, height=25)

# 启动消息循环
root['background'] = '#ffffff'
root.mainloop()

