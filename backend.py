import sqlite3
class Database():
    def __init__(self):

        self.database_connection=sqlite3.connect('db-todolist.db')
        self.my_cursor=self.database_connection.cursor()

        self.my_cursor.execute('SELECT * FROM work')
        self.data = self.my_cursor.fetchall()

    def add_data(self,title,description,time,date):
        id=int(self.data[len(self.data)-1][0])
        print(id)
        self.my_cursor.execute(f'INSERT INTO work(id,title,description,done,time,date) VALUES("{id+1}","{title}","{description}",0,"{time}","{date}")')
        self.database_connection.commit()
    def update_data(self,id,number):
        self.my_cursor.execute(f'UPDATE work SET done="{number}" WHERE id="{id}"')
        self.database_connection.commit()
    def update_data_star(self,id,number):
        self.my_cursor.execute(f'UPDATE work SET star="{number}" WHERE id="{id}"')
        self.database_connection.commit()
    def remove_data(self,id):
        self.my_cursor.execute(f'DELETE FROM work WHERE id={id}')
        self.database_connection.commit()
