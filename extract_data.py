import pandas as pd
import psycopg2, json

try:
    with open('config.txt', 'r') as f:
        params = json.load(f)
    connect_str = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(params['dbname'], params['user'], params['host'], params['password'])
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_type = 'BASE TABLE'and table_schema = 'public'
                    ORDER BY table_name;
                    """)
    tnames = cursor.fetchall()
    for t in tnames:
        table = t[0]
        cursor.execute("""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = '{0}';
                        """.format(table))
        cnames = cursor.fetchall()
        cnames = [x[0] for x in cnames]
        cursor.execute("""SELECT * FROM {0} LIMIT 2000;""".format(table))
        rows = pd.DataFrame(data=cursor.fetchall(), columns=cnames)
        rows.to_csv('tables/{0}.csv'.format(table),index=False,header=True)

except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
