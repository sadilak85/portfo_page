from flask import Flask, flash, render_template, url_for, request, redirect
import csv
import re

app = Flask(__name__)

app.secret_key = 'xdsfslgmsjhotrjkjdfpsdkjfl2343thfhd'
#app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def my_home():
  return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
  return render_template(page_name)

def write_to_file(data):
  email = data["email"]
  message = data["message"]
  name = data["name"]
  with open('database.txt', mode='a') as database:
    database.write(f'\n{email},{message},{name}')

def write_to_csv(data):
  email = data["email"]
  message = data["message"]
  name = data["name"]
  if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
    flash("Not a valid email!")
    return False
  elif message == '':
    flash("Enter a text!")
    return False 
  with open('database.csv', newline='', mode='a') as database2:
    csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([email,message,name])
  flash ('')
  return True

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
  if request.method == 'POST':
    try:
      data = request.form.to_dict()
      if write_to_csv(data):
        return redirect(url_for('my_home', _anchor="thanks"))
      else:
        return redirect(url_for('my_home', _anchor="contact"))
    except:
      return 'did not save to database'
  else:
    return 'something went wrong. Try again!'