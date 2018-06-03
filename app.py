import os
import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
	con = sqlite3.connect('test.db')
	con.close()
	return render_template("index.html")

@app.route('/send', methods=['GET', 'POST'])
def send():
	if request.method == 'POST':
		date_time = datetime.datetime.today()
		msg1 = float(request.form['msg1'])
		msg2 = float(request.form['msg2'])
		msg3 = int(request.form['example2'])



		con = sqlite3.connect('test.db')
		c = con.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS message(msg1,msg2,msg3, date_time)''')
		c.execute('INSERT INTO message VALUES (?,?,?,?)', (msg1, msg2, msg3, date_time))
		con.commit()
		c = con.execute("select * from message")
		for row in c:
			result_0 = (row[0])
			result_1 = (row[1])
			result_2 = (row[2])
			result_3 = row[3]
		data_name = 'summary_data.csv'
		data = pd.read_csv(data_name)
		valid_list = np.where(data['price'] == msg3)[0]
		tmp = data.iloc[valid_list, :]
		latitude_list = np.asarray(tmp["latitude"])
		longitude_list = np.asarray(tmp["longitude"])
		dist = np.power(latitude_list - msg1, 2) + np.power(longitude_list - msg2, 2)
		target = valid_list[np.argmin(dist)]
		target_url = data.iloc[target]["url"]
		target_image = data.iloc[target]["image_url"]
		target_name = data.iloc[target]["name"]

		return render_template('index.html', result_0=result_0, result_1=result_1, result_2=result_2, result_3=result_3, result_4=target_image, result_5 = target_url, result_6 = target_name)

if __name__ == '__main__':
	app.debug = True
	app.run() 		