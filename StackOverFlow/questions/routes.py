from flask import  jsonify, request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from StackOverFlow.models.models import db
from StackOverFlow.models.models import Answer, Question
questions = Blueprint('questions', __name__,url_prefix="/questions")



#retrieving all questions 
@questions.route("/", methods=['GET'])
@jwt_required()
def all_questions():
    #ensuring that a user has logged in
    all_questions = Question.query.all()
    return jsonify(all_questions),200


#retrieving all questions for a user
@questions.route("/users", methods=['GET'])
@jwt_required()
def all_user_questions():
    #ensuring that a user has logged in
    current_user = get_jwt_identity()
    all_questions = Question.query.filter_by(user_id=current_user).all()
    return jsonify(all_questions),200


#retrieving single questions item
@questions.route("/<string:questionId>", methods=['GET'])
def single_question(questionId):
    single_question = Question.query.filter_by(id=questionId).first()
    
    if not single_question:
        return jsonify({'message': '  Question not found'}), 404
    return jsonify(single_question),200


#retrieving single questions item for a user
@questions.route("/<string:questionId>", methods=['GET'])
def single_user_question(questionId):
    current_user = get_jwt_identity()
    single_question = Question.query.filter_by(user_id=current_user,id=questionId).first()
    
    if not single_question:
        return jsonify({'message': '  Question not found'}), 404
    return jsonify(single_question),200


#creating questions
@questions.route("/", methods=["POST"])
@jwt_required()
def new_questions():
    if request.method == "POST":
        
        user_id = get_jwt_identity()
        title = request.json['title']
        body = request.json['body']
        tag = request.json['tag']
       
       
        #checking if title exists
        if Question.query.filter_by(title=title).first():
                return jsonify({
                'error': 'Question title exists'
            }), 409
        
        #checking if body exists
        if Question.query.filter_by(body=body).first():
                return jsonify({
                'error': 'Question body already exists'
            }), 409
        
           

        #inserting values into the questions_list
        new_question = Question(title=title,body=body,user_id=user_id,tag=tag)
        db.session.add(new_question)
        db.session.commit()
        
         
  
    return jsonify({'message':'new question posted','tag':tag,'title':title,'body':body,'user_id':user_id}),200
    


 
# #deleting a question
@questions.route("/remove/<string:questionId>", methods=['DELETE'])
@jwt_required()
def delete_questions(questionId):
    current_user = get_jwt_identity()

    question = Question.query.filter_by(user_id=current_user, id=questionId).first()

    if not question:
        return jsonify({'message': 'Item not found'}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({}), 204

    


#creating answers
@questions.route("/<string:questionId>/answers", methods=["POST"])
@jwt_required()
def new_answers(questionId):
    if request.method == "POST":
        
        question_id =  request.json['question_id']
        user_id = get_jwt_identity()
        body = request.json['body']
       
       
        #checking if body exists
        if Answer.query.filter_by(body=body).first():
                return jsonify({
                'error': 'This answer already exists'
            }), 409
        
           

        #inserting values into the questions_list
        new_answer = Answer(questionId=question_id,body=body,user_id=user_id)
        db.session.add(new_answer)
        db.session.commit()
       
         
  
    return jsonify({'message':'new answer posted','question':question_id,'body':body,'user_id':user_id}),200
    

#Viewing an answer by id
@questions.route("/<string:answer_id>/answers", methods=["POST"])
@jwt_required()
def single_answer(answer_id):
    single_answer = Answer.query.filter_by(id=answer_id).first()
  
    return jsonify(single_answer),200

#retrieving all answers for a specific user
@questions.route("/answers/<string:user_id>", methods=['GET'])
@jwt_required()
def user_answers(user_id):
    #ensuring that a user has logged in
    user_id = get_jwt_identity()
    answers = Answer.query.filter_by(user_id=user_id).first()
    return jsonify(answers),200



#retrieving all answers
@questions.route("/answers", methods=['GET'])
def all_answers():
    all_answers = Answer.query.all()
    return jsonify(all_answers),200