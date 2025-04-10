import mariadb
import sys

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

inp = int(input("Bitte den Ihr PLZ eingeben: "))

cur.execute(f"""SELECT kunden.Name, kunden.Vorname, anrede.Anrede, kunden.Strasse, kunden.Husnummer, ort.PLZ, ort.Ort
            FROM (kunden JOIN anrede ON kunden.Anrede = anrede.`ID_Anrede`) JOIN ort ON kunden.OrtID = ort.ID_Ort
            WHERE ort.PLZ LIKE {inp}""")

kundenbestell_list = []

for i, j, k, l, m, n, o in cur:
    kundenbestell_list.append(kundenbestellung(i, j, k, l, m, n, o))

for i in kundenbestell_list:
    print(i.anrede, i.name, i.vorname, i.bestelldatum, i.artikelname)