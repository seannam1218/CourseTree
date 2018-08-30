from flask import Flask, render_template, request, redirect, url_for
import MySQLdb
import constants

app = Flask(__name__)

# connect to mysql:
mysql = MySQLdb.connect(host = constants.HOST,
                        user = constants.USER,
                        passwd = constants.PW,
                        db = constants.DB)

class User(object):
    instance = None

    @staticmethod
    def getInstance(self):
        if self.instance == None:
            self.instance = User()
        return self.instance

    def __init__(self):
        if self.instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.sid = None
            self.fname = None
            self.lname = None
            self.courses = []
            self.instance = self


user = User.getInstance(User)
cur = mysql.cursor()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur.execute("select * from student")
        sids = cur.fetchall()
        sid = request.form.get("sid")

        for i in range(len(sids)):
            if sid == sids[i][0]:
                user.sid = sids[i][0]
                user.fname = sids[i][1]
                user.lname = sids[i][2]
                return redirect(url_for('welcome'))
        return redirect(url_for('loginFailed'))
    return render_template('login.html')

@app.route('/loginFailed')
def loginFailed():
    return render_template('loginFailed.html')

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == "POST":
        return redirect(url_for('tree'))
    return render_template('welcome.html', userName = user.fname)

@app.route('/coursesTaken')
def coursesTaken():
    result = cur.execute("SELECT * FROM student, taken WHERE student.sid = taken.sid AND student.sid = %s", [user.sid])
    if result > 0:
        studentTable = cur.fetchall()
    else:
        return redirect(url_for('loginFailed'))
    return render_template('coursesTaken.html', studentTable = studentTable)

@app.route('/allCourses')
def allCourses():
    result = cur.execute("SELECT * FROM course LEFT OUTER JOIN prereq ON course.cid = prereq.cid")
    if result > 0:
        courseTable = cur.fetchall()
        print(courseTable)
    else:
        return redirect(url_for('loginFailed'))
    return render_template('allCourses.html', courseTable = courseTable)

@app.route('/tree')
def tree():
    return render_template('tree.html')

if __name__ == '__main__':
    app.run(debug=True)

