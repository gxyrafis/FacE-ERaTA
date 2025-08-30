# This is a sample Python script.
import os
import random
from PIL import Image
from FreeSimpleGUI import Print
from cv2 import VideoCapture, imwrite
import FreeSimpleGUI as psg
import plotly.express as px

from UtilityFunctions import emotionAnalysis, checkCamValidity

if __name__ == '__main__':
    picpath = ""
    windowkey = "-INTRO-"
    isTraining = False
    # Intro Layout
    emotions = ['Anger', 'Sadness', 'Disgust', 'Happiness', 'Fear', 'Surprise']
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

    #User picked emotion layout
    backuserp = psg.Button(button_text="Back", key = "BACKUSERP", font=("Arial", 16, "bold"))
    userptext = psg.Text("User chosen emotion portrayal.", font=("Arial", 20, "bold"))
    userprules = psg.Text("In this gamemode you are allowed to try and portray an emotion of your choice. "
                          "Select an emotion to portray down below and then either upload a picture or take a picture live "
                          "where you express said emotion. The AI judge will then rate your attempt once you press 'Submit'.", font=("Arial Bold", 14), size=(90, None), justification="center", pad=((0,0),(0,20)))
    emotion_text_userp = psg.Text("", key="emotionU", font=("Arial", 20, "bold"))
    emotion_picker_button_userp = psg.Combo(emotions, key="EPBU", font=("Arial", 15, "bold"), pad=30, enable_events=True)
    pic_search_userp = psg.FileBrowse(key="picsearchU", pad=30, button_text="Upload Picture", font=("Arial", 16, "bold"),
                                target="picsearchU", enable_events=True, disabled=True)
    take_pic_userp = psg.Button(button_text="Take a Picture", key="livepicU", font=("Arial", 16, "bold"), disabled=True)
    submit_userp = psg.Button(button_text="Submit", key="SubmitU", font=("Arial", 16, "bold"), disabled=True)

    #Random emotion layout
    backrandom = psg.Button(button_text="Back", key="BACKRANDOM",font=("Arial", 16, "bold"))
    randomtxt = psg.Text("Random Emotion Portrayal Challenge!", font=("Arial", 20, "bold"))
    randomrules = psg.Text("In this gamemode, the app will request that you portray a random emotion of its choice!\n Do your best to portray it and either"
                           " upload an existing pic or take one live using the respective buttons. The AI will then do its best to rate your portrayal "
                           "and issue its verdict!", font=("Arial Bold", 14), size=(90, None), justification="center", pad=((0,0),(0,20)))
    emotion_picker_button = psg.Button(button_text="New emotion", key="EPB", font=("Arial", 15, "bold"), pad=30)
    emotion_text = psg.Text("", key="emotion", font=("Arial", 20, "bold"))
    pic_search = psg.FileBrowse(key="picsearch", pad=30, button_text="Upload Picture", font=("Arial", 16, "bold"), disabled=True, target="picsearch", enable_events=True)
    take_pic = psg.Button(button_text="Take a Picture", key="livepic", font=("Arial", 16, "bold"), disabled=True)
    submit = psg.Button(button_text="Submit", key="Submit",font=("Arial", 16, "bold"), disabled=True)

    #Training layout
    backtraining = psg.Button(button_text="Back", key="BACKTRAINING", font=("Arial", 16, "bold"))
    trainingtxt = psg.Text("Training Mode", font=("Arial", 20, "bold"))
    traininginfo = psg.Text("Welcome to the training mode! In this mode, the app will not request an emotion at all."
                            " Instead, you are free to take any expression that you like and either take a picture using your webcam"
                            " or upload existing ones. The AI classifier will then take this pictures and tell you what emotion it thought "
                            "you were trying to display and what the accuracy was.", font=("Arial Bold", 14), size=(90, None), justification="center", pad=((0,0),(0,20)))
    pic_search_training = psg.FileBrowse(key="picsearchT", pad=30, button_text="Upload Picture", font=("Arial", 16, "bold"),
                                target="picsearchT", enable_events=True)
    take_pic_training = psg.Button(button_text="Take a Picture", key="livepicT", font=("Arial", 16, "bold"))
    submit_training = psg.Button(button_text="Submit", key="SubmitT", font=("Arial", 16, "bold"))

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

    layoutuserp = [[backuserp, psg.Push()],
                   [userptext],
                   [psg.HorizontalSeparator(pad=10)],
                   [userprules],
                   [emotion_picker_button_userp],
                   [pic_search_userp, take_pic_userp, psg.Push(), submit_userp]
    ]

    layouttraining = [[backtraining,psg.Push()],
                      [trainingtxt],
                      [psg.HorizontalSeparator(pad=10)],
                      [traininginfo],
                      [pic_search_training, take_pic_training, psg.Push(), submit_training]
    ]

    layoutresult = [[back],
                    [psg.Push(), result_text, psg.Push()],
                    [psg.Push(), photo, chart, psg.Push()],
                    [psg.Push(), accuracy, psg.Push()]
    ]
    layoutmain = [[psg.Column(layoutintro, key="-INTRO-", element_justification="c"), psg.Column(layoutresult, key="-RESULT-", visible=False),
                   psg.Column(layoutrandom, key="-RANDOMWIN-", visible=False, element_justification="c"), psg.Column(layouttraining, key="-TRAININGWIN-", visible=False, element_justification="c"),
                   psg.Column(layoutuserp, key="-USERPWIN-", visible=False, element_justification="c")]
                  ]
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
            isTraining = False
            windowkey="-RANDOMWIN-"
            window["-INTRO-"].update(visible=False)
            window["-RANDOMWIN-"].update(visible=True)

        elif event == "--CHOOSEGM--":
            isTraining = False
            windowkey = "-USERPWIN-"
            window["-INTRO-"].update(visible=False)
            window["-USERPWIN-"].update(visible=True)

        # TRAINING MODE ACTIVATED
        elif event == "--TRAINGM--":
            windowkey = "-TRAININGWIN-"
            isTraining = True
            window["-INTRO-"].update(visible=False)
            window["-TRAININGWIN-"].update(visible=True)

        #EMOTION PICKER BUTTON CLICKED
        elif event == "EPB":
            emotion = random.choice(emotions)
            window["emotion"].update(emotion)
            window["picsearch"].update(disabled=False)
            window["Submit"].update(disabled=False)
            window["livepic"].update(disabled=False)

        #EMOTION PICKER COMBO
        elif event == "EPBU":
            emotion = values["EPBU"]
            window["picsearchU"].update(disabled=False)
            window["SubmitU"].update(disabled=False)
            window["livepicU"].update(disabled=False)

        #BACK FROM RANDOM TO INTRO
        elif event == "BACKRANDOM":
            windowkey = "-INTRO-"
            window["emotion"].update("")
            window["-INTRO-"].update(visible=True)
            window["-RANDOMWIN-"].update(visible=False)
            window["picsearch"].update(disabled=True)
            window["Submit"].update(disabled=True)
            window["livepic"].update(disabled=True)

        #BACK FROM USER PICKED TO INTRO
        elif event == "BACKUSERP":
            windowkey = "-INTRO-"
            window["-INTRO-"].update(visible=True)
            window["-USERPWIN-"].update(visible=False)
            window["picsearchU"].update(disabled=True)
            window["SubmitU"].update(disabled=True)
            window["livepicU"].update(disabled=True)

        #BACK FROM TRAINING TO INTRO
        elif event == "BACKTRAINING":
            windowkey = "-INTRO-"
            window["emotion"].update("")
            window["-INTRO-"].update(visible=True)
            window["-TRAININGWIN-"].update(visible=False)

        #TAKE LIVE PIC REGARDLESS OF MODE
        elif event == "livepic" or event == "livepicT" or event == "livepicU":
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

        elif event == "picsearchT":
            picpath = values["picsearchT"]

        elif event == "picsearchU":
            picpath = values["picsearchU"]

        #SUBMIT PIC TO AI FOR RESULTS
        elif event == "Submit" or event == "SubmitT" or event == "SubmitU":
            if picpath == "":
                psg.popup("Error: No image selected.")
                continue
            if isTraining:
                emotion = "T"
            try:
                analysis_results = emotionAnalysis(picpath, emotion, False)
            except:
                try:
                    psg.popup_timed("OpenCV was unable to spot a face in the picture. Switching to RetinaFace, this might take a moment.",auto_close_duration=7, button_type= 5, non_blocking=True, auto_close=True)
                    analysis_results = emotionAnalysis(picpath, emotion, True)
                except:
                    psg.popup("RetinaFace was also unable to spot a face in the picture. Please use a picture containing a face.")
                    continue

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
            if windowkey == "-RANDOMWIN-":
                window["-RANDOMWIN-"].update(visible=False)
            elif windowkey == "-USERPWIN-":
                window["-USERPWIN-"].update(visible = False)
            elif windowkey == "-TRAININGWIN-":
                window["-TRAININGWIN-"].update(visible=False)
                window["resulttext"].update("")
                window["accuracy"].update("Our AI thought you were displaying " + analysis_results[
                        2] + " with an accuracy of " + str(round(analysis_results[1], 2)) + "%")

            window["-RESULT-"].update(visible=True)

        #RETURN FROM RESULTS TO PREV WINDOW
        elif event == "BACKRESULTS":
            if ".jpg" in picpath.lower() or ".jpeg" in picpath.lower():
                os.remove(new_image_path)
            window["-RESULT-"].update(visible=False)
            window[windowkey].update(visible=True)



    window.close()
