# -*- coding: utf-8 -*-

import tkinter
import sys
from tkinter import messagebox
import pyqrcode
import csv
import os

TITLE = '入退室用QRコード生成システムv1.0'
ID_PATH = 'id.csv'

root = tkinter.Tk()
root.resizable(width=False,height=False)

username = ""  #登録するユーザーネーム

def popup(str):
    messagebox.showinfo(TITLE,str)

def is_usedname(username):
    l = load_csv(ID_PATH)
    for i in range(len(l)): #usernameの重複チェック
        print(i)
        if i==0:
            continue
        else:
            if(l[i][1] == username):
                return True
    return False

def is_wrong_name(username):
        for char in username:
            try:
                _ = (ord)(char)
            except ValueError:
                return True
            if(97 > ord(char) or ord(char) > 122): #半角英小文字のみ許容
                return True
        return False

def load_csv(csv_path):
    if(os.path.exists(ID_PATH)): #filecheck
        with open(csv_path) as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            f.close()
        return l
    else:
        messagebox.showerror(TITLE,'IDを管理するcsvファイルが存在しません。')

def add_info_to_csv(csv_path, id, username):
    if(os.path.exists(csv_path)):
        with open(csv_path, 'a', newline="") as f:
            l = [id, username]
            writer = csv.writer(f)
            writer.writerow(l)
            f.close()
    else:
        messagebox.showerror(TITLE,'IDを管理するcsvファイルが存在しません。')

def qrcode_generator(username): #qrコードを発行する(login：赤, logout：青)
    id_table = load_csv(ID_PATH)
    if(len(id_table)==0):
        messagebox.showerror(TITLE, ID_PATH + 'の書式が不正です。')
    elif(id_table[len(id_table)-1][0]=='ID'):
        newest_id = 1001
    else:
        newest_id = (int)(id_table[len(id_table)-1][0]) #現在登録されている最も番号の大きい（末尾の）IDナンバーを取得
        newest_id = newest_id + 1 #インクリメントしてその人のIDナンバーを決定
    qr_login_info = (str)(newest_id) + '/' + username + '/' + 'login' #login用qrのinfo
    qr_logout_info = (str)(newest_id) + '/' + username + '/' + 'logout' #logout用qrのinfo
    qr_login_img = pyqrcode.create(content = qr_login_info , error = 'H')
    qr_logout_img = pyqrcode.create(content = qr_logout_info , error = 'H')

    if(not os.path.exists('qrcode')): #qrcodeディレクトリがなければ作成
        os.mkdir('qrcode')

    path = 'qrcode' + '/' + username

    if(os.path.exists(path)):
        ret = messagebox.askyesno(TITLE, path + 'に既にQRコードが存在します。上書きしますか？')
        if(ret):
            qr_login_img.png(file = path + '/'+ username + '_login.png' , scale = 6, module_color = [255,0,0,255])
            qr_logout_img.png(file = path + '/' +username + '_logout.png' , scale = 6, module_color = [0,0,255,255] )
            messagebox.showinfo(TITLE, path + 'にQRコードを保存しました。')
    else:
        os.mkdir(path)
        qr_login_img.png(file = path + '/'+ username + '_login.png' , scale = 6, module_color = [255,0,0,255])
        qr_logout_img.png(file = path + '/' +username + '_logout.png' , scale = 6, module_color = [0,0,255,255] )
        messagebox.showinfo(TITLE, path + 'にQRコードを保存しました。')
    return newest_id, username

def issue_qrcode(event):
    if(is_usedname(entry_name.get())):
        messagebox.showerror(TITLE,'そのユーザー名は既に使用されています。')
    elif(entry_name.get() == "" or entry_name.get() == "名前を入力" ): #usernameの入力があるか
        messagebox.showerror(TITLE,"名前を入力してください。")
    elif(is_wrong_name(entry_name.get())): #usernameに半角英小文字以外が含まれていないか
        messagebox.showerror(TITLE,"半角英小文字のみで入力してください。")
    else:
        username = entry_name.get()
        l = qrcode_generator(username)
        add_info_to_csv(ID_PATH, (int)(l[0]), l[1])

root.title(TITLE)
root.geometry("720x400")

title = tkinter.Label(text=TITLE,font=("",20))
title.grid(row=1,column=1,padx=30,pady=30)

explanation = tkinter.Label(text="下のテキストボックスにユーザーネームを入力して発行ボタンをクリックすると、\n入退室システムで使用するQRコードが発行できます。\n（半角英小文字のみで入力してください）",font=("",15))
explanation.grid(row=2,column=1,padx=30,pady=30)

entry_name = tkinter.Entry(width=50)
entry_name.insert(tkinter.END,"ユーザーネームを入力")
entry_name.grid(row=3,column=1,padx=30,pady=30)

issue_Btn = tkinter.Button(text='発行',width=30,height=3)
issue_Btn.bind("<ButtonRelease-1>",issue_qrcode)
issue_Btn.grid(row=4,column=1,padx=30,pady=30)

root.mainloop()