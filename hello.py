from flask import Flask, request
import subprocess
import mariadb
import sys

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello World!'

@app.route('/tabletest')
def show_tabletest():
	try:
		conn = mariadb.connect(
			user="fcelaya",
			password="passtest",
			host='localhost',
			port=3306,
			database='testdb'
		)
	except mariadb.Error as e:
		print(f"Got following error connecting to MariaDB: {e}")
		sys.exit(1)

	cur = conn.cursor()
	#id = 1
	try:
	#	cur.execute("SELECT * FROM tabletest WHERE id=?",(id,))
		cur.execute("SELECT * FROM tabletest")
	except mariadb.Error as e:
		print(f"Error: {e}")

	res = {'id':[], 'name':[], 'age':[]}
	for (id,name,age) in cur:
		res['id'].append(id)
		res['name'].append(name)
		res['age'].append(age)
		print(res)
	conn.close()
	return res

@app.route("/post", methods=['POST'])
def post():
	request_data = request.json
	name = str(request_data['name'])
	age = str(request_data['age'])

	try:
		conn = mariadb.connect(
			user="fcelaya",
			password="passtest",
			host='localhost',
			port=3306,
			database='testdb'
		)
	except mariadb.Error as e:
		print(f"Got following error connecting to MariaDB: {e}")
		sys.exit(1)

	cur = conn.cursor()
	try:
		id = cur.execute("SELECT MAX(id) FROM tabletest;")
		id = cur.fetchall()[0][0]+1
		print(f"INSERT INTO tabletest VALUES('{id}','{name}','{age}')")
		cur.execute(f"INSERT INTO tabletest VALUES('{id}','{name}','{age}')")
		conn.commit()
	except mariadb.Error as e:
		print(f"Error: {e}")
	finally:
		cur.close()
		conn.close()


	return f"The person is id:{id}, name:{name}, age:{age}"


if __name__=='__main__':
	app.run(debug=True,port=80,host='0.0.0.0')
