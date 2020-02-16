from application import mysqlconfg

def select(sqlselect, fetchall):
    conn = mysqlconfg.connection()
    cur = conn.cursor()
    cur.execute(sqlselect)

    if fetchall:
        fetchdata = cur.fetchall()
    else:
        fetchdata = cur.fetchone()
    
    conn.close()

    return fetchdata
