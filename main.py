import tkinter
from tkinter import ttk
import mariadb
import sys 

def ins(rows):
    for item in treeview.get_children():
        treeview.delete(item)

    for col_name in cols:
        treeview.heading(col_name, text=col_name)

    for value_tuple in rows:
        row = []
        row.append(value_tuple.name)
        row.append(value_tuple.vorname)
        row.append(value_tuple.anrede)
        row.append(value_tuple.strasse)
        row.append(value_tuple.hausnummer)
        row.append(value_tuple.plz)
        row.append(value_tuple.ort)
        treeview.insert('', tkinter.END, values=row)

def search():
    inp = int(entry.get())

    cur.execute(f"""SELECT kunden.Name, kunden.Vorname, anrede.Anrede, kunden.Strasse, kunden.Husnummer, ort.PLZ, ort.Ort
            FROM (kunden JOIN anrede ON kunden.Anrede = anrede.`ID_Anrede`) JOIN ort ON kunden.OrtID = ort.ID_Ort
            WHERE ort.PLZ LIKE {inp}""")
    
    kundenbestell_list = []

    for i, j, k, l, m, n, o in cur:
        kundenbestell_list.append(kundenbestellung(i, j, k, l, m, n, o))

    ins(kundenbestell_list)
    
class kundenbestellung():
    def __init__(self, anrede, name, vorname, strasse, hausnummer, plz, ort):
        self.anrede = anrede
        self.name = name
        self.vorname = vorname
        self.strasse = strasse
        self.hausnummer = hausnummer
        self.plz = plz
        self.ort = ort

try:
    conn = mariadb.connect(
        user="Geister_Eule",
        password="Jd787811?",
        host="localhost",
        port=3306,
        database="schlumpfshop3"
    )
except mariadb.Error as e:
    print(f"Error {e}")
    sys.exit(1)

cur = conn.cursor()

root = tkinter.Tk()

cols = ("Name", "Vorname", "Anrede", "Strasse", "Husnummer", "PLZ", "Ort")

style = ttk.Style(root)
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Search")
widgets_frame.grid(row=0, column=0, padx=10, pady=10)

entry = ttk.Entry(widgets_frame)
entry.insert(0, "PLZ")
entry.bind("<FocusIn>", lambda e: entry.delete('0', 'end'))
entry.grid(row=1, column=0, padx=5, pady=(0,5), sticky="ew")

button_insert = ttk.Button(widgets_frame, text="Suchen", command=search)
button_insert.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")


treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10, padx=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")


treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)
treeview.column("Name", width=100)
treeview.column("Vorname", width=100)
treeview.column("Anrede", width=100)
treeview.column("Strasse", width=100)
treeview.column("Husnummer", width=100)
treeview.column("PLZ", width=100)
treeview.column("Ort", width=100)
treeview.pack()
treeScroll.config(command=treeview.yview)

root.mainloop()