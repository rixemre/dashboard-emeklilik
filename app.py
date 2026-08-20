from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':    
    name = request.form['username']
    password = request.form['password']
    if name == 'emeklilik' AND password == '1234':
      return render_template('index.html')
    else:
      return "Hatalı kullanıcı adı veya şifre"
  return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
