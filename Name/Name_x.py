#import the necessary libraries
#render_template library is used to render a template
#request library is used to get the request from the user
#mysql.connector library is used to connect to a MySQL database
from flask import Flask, render_template, request
import mysql.connector

#The Flask library is used to create a web application
app = Flask(__name__)

#A class to manage names in a MySQL database.
class NameManager:
    
    #This method is the constructor for the class. It initializes the class variables
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sameer@786",
            database="certisured"
        )
        self.cursor = self.connection.cursor()
        
    #This method creates the names table if it doesn't exist(Mysql database certisured).
    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS names (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        
    #This method adds a name to the names table(Mysql database certisured).
    def add_name(self, name):
        insert_query = "INSERT INTO names (name) VALUES (%s)"
        values = (name,)
        self.cursor.execute(insert_query, values)
        self.connection.commit()
        
    #This method gets a name from the names table(Mysql database certisured).
    def get_name(self,name):
        select_query = "SELECT name FROM names WHERE name = %s"
        values = (name,)
        self.cursor.execute(select_query, values)
        names = self.cursor.fetchall()
    
        if names:
            return names
        else:
            return None
        
    # Closes the database connection.
    def close_connection(self):
        self.cursor.close()
        self.connection.close()

@app.route('/', methods=['GET', 'POST'])
#home() function is the main function of the web application

def home():
    #This function gets the request from the user, and then calls the appropriate method from the NameManager class
    name_manager = NameManager()
    name_manager.create_table()

    suggested_name = None

    if request.method == 'POST':
        if request.form['action'] == 'add':
            name = request.form['name']
            name_manager.add_name(name)
        elif request.form['action'] == 'get':
            name = request.form['name']
            suggested_name = name_manager.get_name(name)
        elif request.form['action'] == 'quit':
            name_manager.close_connection()
            return render_template('Name_x.html', quit=True)
        
    #function then renders the Name_x.html template with the suggested name
    return render_template('Name_x.html', suggested_name=suggested_name)

if __name__ == "__main__":
    #the application will automatically reload if the code is changed
    app.run(debug=True)