from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message # type: ignore
import os
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 500
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "shama123@gmail.com"
app.config['MAIL_PASSWORD'] = "root"

db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(200))

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'token')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(username=email).first()
        if user:
            token = jwt.encode({'reset_password': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
            user.token = token
            db.session.commit()
            msg = Message('password reset', sender='TestSite Team <noreply@example.com>', recipients=[email])
            msg.html = render_template('resetEmail.html', user=user, token=token)
            mail.send(msg)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('The email address does not exist in our system.')
     
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'])['reset_password']
        user = User.query.get(id)
    except:
        return 'Invalid token'
    if request.method == 'POST':
        user.password = request.form['password']
        user.token = ''
        db.session.commit()
        flash('Your password has been reset. You can now sign in.', 'success')
        return redirect(url_for('loginPage'))
     
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)