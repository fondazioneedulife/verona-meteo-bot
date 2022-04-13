BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Locazione" (
	"ID"	INTEGER NOT NULL,
	"Data"	TEXT,
	"Ora"	TEXT,
	"IDStazione"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Pioggia" (
	"ID"	INTEGER NOT NULL,
	"RAIN"	REAL,
	"DP"	REAL,
	"ID_Locazione"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("ID_Locazione") REFERENCES "Locazione"("ID")
);
CREATE TABLE IF NOT EXISTS "Vento" (
	"ID"	INTEGER NOT NULL,
	"WIND"	REAL,
	"RAFF"	REAL,
	"WIND_DIR"	TEXT,
	"ID_Locazione"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("ID_Locazione") REFERENCES "Locazione"("ID")
);
CREATE TABLE IF NOT EXISTS "Temperatura" (
	"ID"	INTEGER NOT NULL,
	"T"	REAL,
	"UR"	INTEGER,
	"PR"	REAL,
	"ID_Locazione"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("ID_Locazione") REFERENCES "Locazione"("ID")
);
COMMIT;