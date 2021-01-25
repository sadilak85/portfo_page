from flask import Flask, flash, render_template, url_for, request, redirect
import csv
import re

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
  with open('database.txt', mode='a') as database:
    email = data["email"]
    message = data["message"]
    name = data["name"]
    file = database.write(f'\n{email},{message},{name}')

def write_to_csv(data):
  with open('database.csv', newline='', mode='a') as database2:
    email = data["email"]
    message = data["message"]
    name = data["name"]
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
      flash("not a valid email")
      return
    csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([email,message,name])
    flash("ok halt")

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
      try:
        data = request.form.to_dict()
        write_to_csv(data):
        return redirect(url_for('submit_form'))
        #return redirect('index.html')
      except:
        return 'did not save to database'
    else:
      return 'something went wrong. Try again!'


if __name__ == '__main__':
   app.run(debug = True)
