from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# dev mode
ENV = 'prod'

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:mark1609@localhost:5000/yourtube'
else:
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qzbzipcxntigdy:46f36334485512e47d816f11de79eaa2c89e70b7d24cde1de35629bd73b4ce7b@ec2-63-32-12-208.eu-west-1.compute.amazonaws.com:5432/d3jjldnit5uj8f'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)





class Users(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))

  def __init__(self,username,password):
      self.username = username
      self.password = password


@app.route('/sign', methods=['POST'])
def signIn():
  username = request.json['username']
  password = request.json['password']

  new_user = Users(username, password)

  db.session.add(new_user)
  db.session.commit()

  return 'new user'




@app.route('/login', methods=['GET'])
def login():
  allUsers = Users.query.all()
  output = []
  for user in allUsers:
    currUser = {}
    currUser['id'] = user.id
    currUser['username'] = user.username
    currUser['password'] = user.password
    output.append(currUser)
  return jsonify(output)




if __name__ == "__main__":
  app.run(port=3001)


