import psycopg2
from config import config

# teste
# teste 123

class Database:

    def __init__():
        # Connect to the PostgreSQL
        conn = None
        try:
            # read connection parameters
            params = config()
 
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
 
            # create a cursor
            cur = conn.cursor()

    # def insert(self,title,author,year,isbn):
    #     self.cur.execute("INSERT INTO book VALUES (NULL,?,?,?,?)",(title,author,year,isbn))
    #     self.conn.commit()

            def view(self):
                self.cur.execute("SELECT * FROM AGOF")
                rows=self.cur.fetchall()
                return rows
                print(rows)

    # def search(self,title="",author="",year="",isbn=""):
    #     self.cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title,author,year,isbn))
    #     rows=self.cur.fetchall()
    #     return rows

    # def delete(self,id):
    #     self.cur.execute("DELETE FROM book WHERE id=?",(id,))
    #     self.conn.commit()

    # def update(self,id,title,author,year,isbn):
    #     self.cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",(title,author,year,isbn,id))
    #     self.conn.commit()

    # def __del__(self):
    #     self.conn.close()

#insert("The Sun","John Smith",1918,913123132)
#delete(3)
#update(4,"The moon","John Smooth",1917,99999)
#print(view())
#print(search(author="John Smooth"))

                                    # cur.close()
                                    #                     except (Exception, psycopg2.DatabaseError) as error:
                                    #                             print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                                             
                                             
        if __name__ == '__main__':
            connect()