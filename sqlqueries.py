import sqlite3
conn = sqlite3.connect("database.db")
c = conn.cursor()

print("DATABASE CONNECTION SUCCESSFUL")

conn.execute("Drop table if EXISTS APPOINTMENTS")

conn.execute("""CREATE TABLE APPOINTMENTS
			(CID integer primary key AUTOINCREMENT,
			NAME VARCHAR(20) not null,
			AGE int(10) not null,
			GENDER varchar(10) not null,
			LOCATION varchar(100) not null,
			PHONE int(10) not null)""")
print("TABLE CREATED SUCCESSFULLY")

conn.execute("Drop table if EXISTS USERS")

conn.execute("""CREATE TABLE USERS
			(USERNAME VARCHAR(20) primary key not null,
			PASSWORD varchar(20) not null)""")
print("TABLE CREATED SUCCESSFULLY")

rows=[('devanshi','1234'),('Dhara','12'),('chaitali','7890')]
c.executemany("INSERT into USERS values(?,?)",rows)

rows_app = [(1, 'Abcd', 12, 'Female', 'RAJKOT', 7878787878), (2, 'Xyz', 15, 'Male', 'ABAD', 8300123456)]
c.executemany("INSERT into APPOINTMENTS values(?, ?, ?, ?, ?, ?)", rows_app)
conn.commit()