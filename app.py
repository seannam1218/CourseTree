from flask import Flask, render_template
import MySQLdb
import constants

app = Flask(__name__)

# connect to mysql:
mysql = MySQLdb.connect(host = constants.HOST,
                        user = constants.USER,
                        passwd = constants.PW,
                        db = constants.DB)

@app.route('/')
def index():
    # cur = mysql.cursor()
    # cur.execute('''SELECT * from student''')
    return render_template('index.html')


@app.route('/students')
def students():
    cur = mysql.cursor()
    result = cur.execute("SELECT * FROM student")
    if result > 0:
        studentTable = cur.fetchall()
        return render_template('students.html', studentTable = studentTable)

if __name__ == '__main__':
    app.run(debug=True)
