from flask import Flask, render_template, request, redirect, url_for
import MySQLdb
import constants

app = Flask(__name__)

# connect to mysql:
mysql = MySQLdb.connect(host = constants.HOST,
                        user = constants.USER,
                        passwd = constants.PW,
                        db = constants.DB)

user = None
cur = mysql.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    if request.method == 'POST':
        cur.execute("select * from student")
        sids = cur.fetchall()
        user = request.form.get("sid")

        for i in range(len(sids)):
            if user == sids[i][0]:
                userName = sids[i][1]
                return render_template('welcome.html', userName = userName)
        return render_template('loginFailed.html')


@app.route('/coursesTaken', methods=['GET'])
def students():
    if request.method == "GET":
        result = cur.execute("SELECT * FROM student, taken WHERE student.sid = taken.sid")
        if result > 0:
            studentTable = cur.fetchall()
            return render_template('coursesTaken.html', studentTable = studentTable)


if __name__ == '__main__':
    app.run(debug=True)
