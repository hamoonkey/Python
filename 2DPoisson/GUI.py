# モジュールのインポート
import tkinter as tk
import os, tkinter.filedialog, tkinter.messagebox

def file_select():
    # ファイル選択ダイアログの表示
    root = tk.Tk()
    root.withdraw()
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('○×プログラム','処理ファイルを選択してください！')
    file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    print(file)

    return file

def entry_get(text):
    #ルートウィジェット（親）初期化
    root=tk.Tk()
    root.title("文字入力")

    def show_entry_fields():
        global namae
        namae=e1.get()
        print("取得: %s" % (namae))

    tk.Label(root, text=text).grid(row=0)
    e1 = tk.Entry(root)
    e1.grid(row=1)
    tk.Button(root, text="取得", command=show_entry_fields).grid(row=2)

    root.mainloop()
    return namae

def radio_get(text):
    root=tk.Tk()
    root.title("文字入力")
    v = tk.IntVar()
    v.set(1) # valueの値が1のものを選択。つまりPython
    languages = [ ("20枚",1), ("40枚",2), ("60枚",3), ("80枚",4), ("100枚",5) ]

    def ShowChoice():
        global choice
        choice=v.get()
        print("取得: %d" %(choice))

    tk.Label(root, text=text).pack()
    for language, val in languages:
        tk.Radiobutton(root, text=language, variable=v,value=val).pack(anchor=tk.W)
    tk.Button(root, text="取得", command=ShowChoice).pack()

    root.mainloop()
    return choice
