import sqlite3
import cgitb

cgitb.enable()

conn = sqlite3.connect("data/sqlite.db")
c = conn.cursor()
c.executescript("""
	DROP TABLE IF EXISTS zespoly;
	CREATE TABLE zespoly(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nazwa VARCHAR(30),
		miasto VARCHAR(30),
		punkty INT);
	INSERT INTO zespoly VALUES(1, 'Legia', 'Warszawa', 38);
	INSERT INTO zespoly VALUES(2, 'Lech', 'Poznan', 36);
	INSERT INTO zespoly VALUES(3, 'Arka', 'Gdynia', 31);
	INSERT INTO zespoly VALUES(4, 'Jagiellonia', 'Bialystok', 36);
	INSERT INTO zespoly VALUES(5, 'Zaglebie', 'Lublin', 32);
""")
conn.commit()
c.close()
print("ok")