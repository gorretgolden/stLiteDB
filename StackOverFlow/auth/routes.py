from flask import  jsonify, request, Blueprint
import validators
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import  create_access_token
from StackOverFlow.models.models import User
from StackOverFlow.models.models import db


auth = Blueprint('auth', __name__, url_prefix='/auth')



#signup endpoint
@auth.route('/signup', methods= ['POST','GET'])
def register_user():
  
  if request.method == "POST":
        
      username = request.json['username']
      email = request.json['email']
      password = request.json['password']

      if len(password) < 6:
            return jsonify({'error': "Password is too short"}), 400

      if len(username) < 3:
        return jsonify({'error': "User is too short"}),400

      if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), 400

      if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), 400

      if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), 409

      if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), 409
       
        #creating a hashed password in the database
      hashed_password = generate_password_hash(password,method="sha256")
      user = User(username=username, password=hashed_password, email=email)  
      #inserting values
      db.session.add(user)
      db.session.commit()
 
        
      return jsonify({'message':'new user created','username':username,'email':email}),200
  return jsonify({'error':'wrong credentials'}) ,400


#login endpoint
@auth.route('/login', methods= ['POST'])

def login_user():
        
   
         if request.method == 'POST':
           email = request.json["email"]
           password = request.json['password']
        
          #empty fields
           if not email and password:
                return jsonify({'error': 'All fields are required'}), 400
          
           user = User.query.filter_by(email=email).first()
          #check if email exits
           if user:
            is_pass_correct = check_password_hash(user.password, password)

            if is_pass_correct:
            
              access = create_access_token(identity=user.id)

              return jsonify({
                'user': {
                    
                    'access': access,
                    'username': user.username,
                    'email': user.email
                 }

                }), 200
 
                
           return jsonify({'error': 'Wrong credentials'}), 401

      
          
        

#retrieving all users
@auth.route("/users", methods=['GET'])
def all_users():
    all_users= User.query.all()

    return jsonify({"users":all_users}),200



@auth.route("/users/<int:user_id>", methods=['GET'])
def user_id(user_id):
    #ensuring that a user has logged in

    user = User.query.filter_by(id=user_id).first()
    return jsonify(user),200


