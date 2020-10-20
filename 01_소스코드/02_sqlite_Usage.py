import sqlite3
conn = sqlite3.connect("./hashtag.db")
cur = conn.cursor()
cur.execute("insert into HashTag(id,location,date,hashtag) values(?,?,?,?)", ('nayohan','home','2020', '#home'))
conn.commit()
conn.close()