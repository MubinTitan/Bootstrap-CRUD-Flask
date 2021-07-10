import MySQLdb
from flask import Flask ,render_template, request
# from MySQLdb import mysql
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="mycrud"

mysql=MySQL(app)

@app.route('/')
def fetch():
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql1="SELECT * FROM `details`"
    cur.execute(sql1)
    data=cur.fetchall()
    return render_template('index.html',data=data)

@app.route('/search',methods=['GET', 'POST'])
def search():
    if(request.method=="POST"):
        sname=request.form['search']
        print(sname)
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT id,name, hobby from details WHERE name LIKE %s OR hobby LIKE %s", (sname,sname))
        datas=cur.fetchall()
        mysql.connection.commit()
        cur.close()
    return render_template('index.html',datas=datas)

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    print(id)
    if(request.method=="POST"):
        detailss=request.form
        print(detailss)
        hobby=detailss["hobby"]
        cur=mysql.connection.cursor()
        print(cur)
        # sql4="UPDATE `details` SET `hobby`=%s WHERE `id`=%s",(hobby, id)
        cur.execute("UPDATE `details` SET `hobby`=%s WHERE `id`=%s",(hobby, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template("bupdate.html", id=id)


@app.route('/delete/<int:id>')
def delete(id):
    cur=mysql.connection.cursor()
    sql3="DELETE FROM details WHERE id='%s'"%id
    cur.execute(sql3)
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/',methods=['GET','POST'])
def insert():
    if(request.method=="POST"):
        details=request.form
        name=details['name']
        hobby=details['hobby']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO details(name, hobby) VALUES (%s, %s)", (name, hobby))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('my.html')

if __name__ == '__main__':
    app.run(debug=True)