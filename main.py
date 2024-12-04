# This is a sample Python script.
import os
import random
from PIL import Image
from cv2 import VideoCapture, imwrite
import PySimpleGUI as psg
import plotly.express as px

from UtilityFunctions import emotionAnalysis, checkCamValidity

if __name__ == '__main__':
    picpath = ""
    windowkey = "-INTRO-"
    # Intro Layout
    emotions = ["Anger", "Sadness", "Disgust", "Happiness", "Fear", "Surprise"]
    welcome_text = psg.Text("Welcome to FacE-ERaTA", font=("Arial", 20, "bold"))
    context = psg.Text("FacE-ERaTA stands for Facial Emotion Expressiveness Rating for Theatrical Actors.\n"
                            "It is an app designed to help actors perfect their portrayal of emotions "
                            "with the help of Artificial Intelligence for Facial Emotion Recognition (FER) and emotion rating " 
                            "based on facial landmarks.\n FacE-ERaTA will do its best to accurately rate the actor's portrayal of emotions in various"
                            " gamemodes.", font=("Arial Bold", 14), size=(90, None), justification="center")
    gamemodes_txt = psg.Text("Pick a mode:", font=("Arial Bold", 14), size=(90, None), justification="center")

    random_emotion_btn = psg.Button(button_text="Random Emotion", key="--RANDOMGM--", font=("Arial", 15, "bold"), pad=30)
    choose_emotion_btn = psg.Button(button_text="User Picked Emotion", key="--CHOOSEGM--", font=("Arial", 15, "bold"), pad=30)
    train_btn = psg.Button(button_text="Training", key="--TRAINGM--", font=("Arial", 15, "bold"), pad=30)




    #Random emotion layout
    backrandom = psg.Button(button_text="Back", key="BACKRANDOM",font=("Arial", 16, "bold"))
    randomtxt = psg.Text("Random Emotion Portrayal Challenge!", font=("Arial", 20, "bold"))
    randomrules = psg.Text("In this gamemode, the app will request that you portray a random emotion of its choice!\n Do your best to portray it and either"
                           " upload an existing pic or take one live using the respective buttons. The AI will then do its best to rate your portrayal "
                           "and issue its verdict!", font=("Arial Bold", 14), size=(90, None), justification="center")
    emotion_picker_button = psg.Button(button_text="New emotion", key="EPB", font=("Arial", 15, "bold"), pad=30)
    emotion_text = psg.Text("", key="emotion", font=("Arial", 20, "bold"))
    pic_search = psg.FileBrowse(key="picsearch", pad=30, button_text="Upload Picture", font=("Arial", 16, "bold"), disabled=True, target="picsearch", enable_events=True)
    take_pic = psg.Button(button_text="Take a Picture", key="livepic", font=("Arial", 16, "bold"), disabled=True)
    submit = psg.Button(button_text="Submit", key="Submit",font=("Arial", 16, "bold"), disabled=True)

    #ResultLayout
    back = psg.Button(button_text="Back", key="BACKRESULTS",font=("Arial", 16, "bold"))
    result_text = psg.Text("", key="resulttext", font=("Arial", 25, "bold"), pad=30)
    photo = psg.Image("", key="testphoto", pad=20)
    chart = psg.Image("", key="chart", pad = 20)
    accuracy = psg.Text("", key="accuracy", font=("Arial", 15, "bold"), pad=20)




    # All the stuff inside your window.
    layoutintro = [[welcome_text],
              [psg.HorizontalSeparator(pad=10)],
              [context],
              [gamemodes_txt],
              [random_emotion_btn, choose_emotion_btn, train_btn]]

    layoutrandom=[[backrandom,psg.Push()],
                  [randomtxt],
                  [psg.HorizontalSeparator(pad=10)],
                  [randomrules],
                  [emotion_text],
                  [emotion_picker_button],
                  [pic_search,take_pic, psg.Push(),submit]
    ]

    layoutresult = [[back],
                    [psg.Push(), result_text, psg.Push()],
                    [psg.Push(), photo, chart, psg.Push()],
                    [psg.Push(), accuracy, psg.Push()]
    ]
    layoutmain = [[psg.Column(layoutintro, key="-INTRO-", element_justification="c"), psg.Column(layoutresult, key="-RESULT-", visible=False),
                   psg.Column(layoutrandom, key="-RANDOMWIN-", visible=False, element_justification="c")]]
    # Create the Window
    window = psg.Window('FacE-ERaTA DEMO', layoutmain, element_justification="c") #size=(700, 500)\

    cam = VideoCapture(0)
    livecamvalidity = checkCamValidity(0)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()


        if event == psg.WIN_CLOSED:  # if user closes window
            break

        #RANDOM GAME MODE CHOSEN
        elif event == "--RANDOMGM--":
            windowkey="-RANDOMWIN-"
            window["-INTRO-"].update(visible=False)
            window["-RANDOMWIN-"].update(visible=True)

        #EMOTION PICKER BUTTON CLICKED
        elif event == "EPB":
            emotion = random.choice(emotions)
            window["emotion"].update(emotion)
            window["picsearch"].update(disabled=False)
            window["Submit"].update(disabled=False)
            window["livepic"].update(disabled=False)

        #BACK FROM RANDOM TO INTRO
        elif event == "BACKRANDOM":
            windowkey = "-INTRO-"
            window["-INTRO-"].update(visible=True)
            window["-RANDOMWIN-"].update(visible=False)

        #TAKE LIVE PIC
        elif event == "livepic":
            if livecamvalidity:
                result, image = cam.read()
                #cam.release()
                #livecamvalidity = not livecamvalidity
                if result:
                    imwrite("livepic.png", image)
                    picpath = "livepic.png"
                else:
                    psg.popup("No image found. Please try again!")
            elif checkCamValidity(0):
                result, image = cam.read()
                #cam.release()
                if result:
                    imwrite("livepic.png", image)
                    picpath = "livepic.png"
                else:
                    psg.popup("No image found. Please try again!")
            else:
                psg.popup("Error: No camera available.")

        #SEARCH FOR PIC LOCALLY
        elif event == "picsearch":
            picpath = values["picsearch"]

        #SUBMIT PIC TO AI FOR RESULTS
        elif event == "Submit":
            if picpath == "":
                psg.popup("Error: No image selected.")
                continue
            try:
                analysis_results = emotionAnalysis(picpath, emotion, False)
            except:
                psg.popup_timed("OpenCV was unable to spot a face in the picture. Switching to RetinaFace, this might take a moment.",auto_close_duration=7, button_type= 5, non_blocking=True, auto_close=True)
                analysis_results = emotionAnalysis(picpath, emotion, True)

            analysis_results[3].write_image("starchart.png")
            size = 500, 500
            chart = Image.open("starchart.png") #Convert image into 500x500
            chart.thumbnail(size, Image.Resampling.LANCZOS)
            chart.save("starchart.png")
            window["chart"].update("starchart.png")

            im = Image.open(picpath)
            im.thumbnail(size, Image.Resampling.LANCZOS)
            new_image_path = picpath
            if ".jpg" in picpath.lower() or ".jpeg" in picpath.lower():
                new_image_path = picpath.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(".JPEG", ".png")
                im.save(new_image_path)
            window["testphoto"].update(new_image_path)
            if analysis_results[0] == "Success":
                window["resulttext"].update("Good job!", text_color="green")
                window["accuracy"].update("You have achieved an accuracy of " + str(round(analysis_results[1],2)) +
                                          "% at displaying " + emotion)
            else:
                window["resulttext"].update("Oh no :(", text_color="red")
                window["accuracy"].update("You have only achieved an accuracy of " + str(round(analysis_results[1],2)) +
                                          "% at displaying " + emotion + ". Our AI thought you were displaying " + analysis_results[2] + " instead.")
            window["-RANDOMWIN-"].update(visible=False)
            window["-RESULT-"].update(visible=True)

        #RETURN FROM RESULTS TO PREV WINDOW
        elif event == "BACKRESULTS":
            if ".jpg" in picpath.lower() or ".jpeg" in picpath.lower():
                os.remove(new_image_path)
            window["-RESULT-"].update(visible=False)
            window[windowkey].update(visible=True)


    window.close()