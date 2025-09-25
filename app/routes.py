from flask import Blueprint,render_template,request
#In Flask, a Blueprint is a way to organize routes and views in larger applications.
#Instead of writing all routes in one app.py, you can split them into separate files using blueprints.
#--
#Used to render HTML templates (Jinja2) stored in the templates/ folder.
#It allows you to pass variables from Python code to your HTML.
#--
#Represents the HTTP request sent by the client (browser, API client, etc.).
#It lets you access form data, JSON body, query parameters, headers, and files.
from app.utils.image_handler import process_image
from app.utils.celebrity_detector import CelebrityDetector
from app.utils.qa_engine import QAEngine

import base64 #we will wncode the image in base64 so that we can show them in html pages

main=Blueprint("main",__name__) #creating a flask blueprint with the name main

celebrity_detector = CelebrityDetector()
qa_engine = QAEngine()

@main.route("/",methods=["GET","POST"])
def index():
    player_info = ""
    result_img_data = ""
    user_question = ""
    answer = ""

    if request.method == "POST":
        if "image" in request.files:#whether image was uploaded or not
            image_file = request.files["image"]

            if image_file: #contains some data or not,valid or invalid file
                img_bytes, facebox = process_image(image_file)

                player_info , player_name = celebrity_detector.identify(img_bytes)

                if facebox is not None:
                    result_img_data = base64.b64encode(img_bytes).decode() #so as to show the image in html form
                else:
                    player_info="No face detected-Please try another image"

        elif "question" in request.form:
            user_question = request.form["question"]

            player_name = request.form["question"]
            player_info = request.form["player_name"]
            result_img_data = request.form["result_img_data"]
            
            answer = qa_engine.ask_about_celebrity(player_name,user_question)

    return render_template(
        "index.html",
        player_info=player_info,
        result_img_data=result_img_data,
        user_question=user_question,
        answer=answer
    )