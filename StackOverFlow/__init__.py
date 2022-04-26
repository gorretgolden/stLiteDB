import os
from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from StackOverFlow.models.models import db

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

#Application Factory Function
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
       app.config.from_mapping(

        CORS_HEADERS= 'Content-Type',
        SQLALCHEMY_DATABASE_URI = database_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
 
    )
    else:
        # load the test config if passed in , resources=r'/*'
        app.config.from_mapping(test_config)
    CORS(app,resources={r"/*": {"origins": "*"}})
    
  
    app.static_folder = 'static'
   
    JWTManager(app)
    
   
    from StackOverFlow.questions.routes import questions
    from StackOverFlow.auth.routes import auth
 
    #registering blueprints    
  
    app.register_blueprint(questions)
    app.register_blueprint(auth)
    
    JWTManager(app)
    
    SWAGGER_URL = "/v1/api/docs"
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,API_URL,
    config={'app_name': "StackOverflow-lite"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
   

    @app.route('/')
    def index():
        return "<h1 >StackOveflow-lite</h1>"

    db.app = app
    db.init_app(app)
    db.create_all()
    return app

