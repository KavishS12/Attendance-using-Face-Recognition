import sqlite3

conn = sqlite3.connect('students.db')

c = conn.cursor()

c.execute("""create table students(
          name TEXT,
          regNO INTEGER PRIMARY KEY,
          present INTEGER
)""")

c.execute("insert into students(name,regNO) values('KAVISH',1234)")
c.execute("insert into students(name,regNO) values('RANVEER',6479)")
c.execute("insert into students(name,regNO) values('DWAYNE JOHNSON',4832)")
c.execute("insert into students(name,regNO) values('PAUL WALKER',8556)")
c.execute("insert into students(name,regNO) values('RYAN GOSLING',1546)")
c.execute("insert into students(name,regNO) values('RYAN REYNOLDS',2348)")
c.execute("insert into students(name,regNO) values('VIN DIESEL',7852)")

c.execute("select * from students")

#print(c.fetchone())
#print(c.fetchmany(2))

items = c.fetchall()
for item in items:
    print(item)

conn.commit()

conn.close()

