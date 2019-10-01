#!/usr/bin/python

import os, requests, boto3, sys
from flask import Flask
from flask import send_file
from flask import request
from datetime import datetime
import sqlite3 as sql
app = Flask(__name__)

s3 = boto3.client('s3')

# Sample URL's to download the image
#https://apod.nasa.gov/apod/image/1701/potw1636aN159_HST_2048.jpg'
#https://www.hdwallpapers.in/download/audi_rs_q3_sportback_2019_4k-1280x720.jpg

# Connecting DB and creating a table (IMAGES)
conn = sql.connect('/tmp/images.db')
conn.execute('CREATE TABLE  IF NOT EXISTS images (name TEXT, size FLOAT, url TEXT, savedate DATETIME, s3path TEXT)')

# Default landing page
@app.route('/')
def index():
    return "Flask is up and running."

# Download image and Push image to S3
@app.route('/download', methods=['GET'])
def download():
	try:
		url = request.args['url'] # user provides url in query string
		#print('\nBeginning file download with requests')
		r = requests.get(url)
		image_name = url.split('/')[-1]

		# write to a file in the app's instance folder
		with app.open_instance_resource('/tmp/'+ image_name, 'wb') as f: # saving file in /tmp folder
			f.write(r.content)
	except Exception as e:
		return "Something has happened..."

	try:
		# Pushing to s3
		bucket_name = 'demobucket'
		full_file_path = '/tmp/' + image_name
		now = datetime.now()
		full_s3_path = bucket_name + '/content/' + image_name
		s3.upload_file(full_file_path, bucket_name, 'content/' + image_name)
		#print '\nFile pushed to S3 successfully.'
		# Retrieve HTTP meta-data for Info
		#print(r.status_code)
		#print(r.headers['content-type'])
		image_size = os.stat('/tmp/' + image_name).st_size
		image_size_MB = image_size
		#print 'Size is :', image_size_MB
		# Saving image details to DB
		with sql.connect('/tmp/images.db') as con:
			cur = con.cursor()
			#print "Opened database successfully."
			cur.execute("INSERT INTO images (name,size,url,savedate,s3path) VALUES(?,?,?,?,?)",(image_name, image_size_MB, url, now, full_s3_path))
		return str('Image download: ' + image_name + 'with size of' + image_size_MB + 'MB.')
	except Exception as e:
		return "Something unexpected has happened..."

@app.route('/list')
def list_images():
	bucket_name = 'qa-conf'
	#print "\nShowing content from S3"
	try:
		response = s3.list_objects(Bucket=bucket_name, Delimiter='', Prefix='content',MaxKeys=123)
		if 'Contents' in response:
			response_status = ''
			for i in response['Contents']:
				response_status += i['Key'] + "\n"
			return response_status
		else:
			return "No files found."
	except:
		return sys.exc_info()

conn.close()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
