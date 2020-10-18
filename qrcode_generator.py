# -*- coding: utf-8 -*-
# ウィンドウ立ち上げ
#--------------------------------
# Tkinterモジュールのインポート
import tkinter
import sys
from tkinter import messagebox
import pyqrcode
import csv
import os

TITLE = '入退室用QRコード生成システムv1.0'
ID_PATH = 'id.csv'

# ウィンドウ（フレーム）の作成
root = tkinter.Tk()
root.resizable(width=False,height=False)

username = ""  #登録するユーザーネーム

def popup(str):
    messagebox.showinfo(TITLE,str)

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
        return l
    else:
        messagebox.showerror(TITLE,'IDを管理するcsvファイルが存在しません。')

def add_info_to_csv(csv_path):
    print("debug")

def qrcode_generator(username): #qrコードを発行する(login：赤, logout：青)
    id_table = load_csv(ID_PATH)
    newest_id = (int)(id_table[len(id_table)-1][0]) #現在登録されている最も番号の大きい（末尾の）IDナンバーを取得
    newest_id = newest_id + 1 #インクリメントしてその人のIDナンバーを決定
    qr_login = (str)(newest_id) + '/' + username + '/' + 'login' #login用qrのinfo
    qr_logout = (str)(newest_id) + '/' + username + '/' + 'logout' #logout用qrのinfo
    qr = pyqrcode.create(content = qr_login , error = 'H')
    qr = pyqrcode.create(content = qr_logout , error = 'H')

    if(not os.path.exists('qrcode')): #qrcodeディレクトリがなければ作成
        os.mkdir('qrcode')

    path = 'qrcode' + '/' + username

    if(os.path.exists(path)):
        ret = messagebox.askyesno(TITLE, path + 'に既にQRコードが存在します。上書きしますか？')
        if(ret):
            qr.png(file = path + '/'+ username + '_login.png' , scale = 6, module_color = [255,0,0,255])
            qr.png(file = path + '/' +username + '_logout.png' , scale = 6, module_color = [0,0,255,255] )
            messagebox.showinfo(TITLE, path + 'にQRコードを保存しました。')
    else:
        os.mkdir(path)
        qr.png(file = path + '/'+ username + '_login.png' , scale = 6, module_color = [255,0,0,255])
        qr.png(file = path + '/' +username + '_logout.png' , scale = 6, module_color = [0,0,255,255] )
        messagebox.showinfo(TITLE, path + 'にQRコードを保存しました。')

def issue_qrcode(event):
    if(entry_name.get() == "" or entry_name.get() == "名前を入力" ):
        messagebox.showerror(TITLE,"名前を入力してください。")
    elif(is_wrong_name(entry_name.get())):
        messagebox.showerror(TITLE,"半角英小文字のみで入力してください。")
    else:
        username = entry_name.get()
        qrcode_generator(username)

# ウィンドウの名前を設定
root.title(TITLE)

# ウィンドウの大きさを設定
root.geometry("720x400")

title = tkinter.Label(text=TITLE,font=("",20))
#title.pack(anchor='center',expand=1)
title.grid(row=1,column=1,padx=30,pady=30)

explanation = tkinter.Label(text="下のテキストボックスにユーザーネームを入力して発行ボタンをクリックすると、\n入退室システムで使用するQRコードが発行できます。\n（半角英小文字のみで入力してください）",font=("",15))
explanation.grid(row=2,column=1,padx=30,pady=30)

entry_name = tkinter.Entry(width=50)
entry_name.insert(tkinter.END,"ユーザーネームを入力")
#EditBox.pack(anchor='center',expand=1)
entry_name.grid(row=3,column=1,padx=30,pady=30)

issue_Btn = tkinter.Button(text='発行',width=30,height=3)
issue_Btn.bind("<ButtonRelease-1>",issue_qrcode)
issue_Btn.grid(row=4,column=1,padx=30,pady=30)

# イベントループ（TK上のイベントを捕捉し、適切な処理を呼び出すイベントディスパッチャ）
root.mainloop()