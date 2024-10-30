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
    emotions = ["Anger", "Sadness", "Disgust", "Happiness", "Fear", "Surprise"]
    welcome_text = psg.Text("Welcome to FacE-ERaTA", font=("Arial", 20, "bold"))
    context = psg.Text("FacE-ERaTA stands for Facial Emotion Expressiveness Rating for Theatrical Actors.\n"
                            "It is an app designed to help actors perfect their portrayal of emotions "
                            "through their facial expressions with the help of Artificial Intelligence for Facial Emotion Recognition (FER) and emotion rating " 
                            "based on facial landmarks.\nThe whole process happens in the form of a game, where the app picκs an emotion at random and the actor "
                            "has to do their best to portray it in a picture of their choosing. The app then identifies and rates their attempt.\n"
                            "To play, press the button below and follow the instructions.", font=("Arial Bold", 14), size=(90, None), justification="center")
    emotion_picker_button = psg.Button(button_text="Pick an emotion", key="EPB", font=("Arial", 15, "bold"), pad=30)
    emotion_text = psg.Text("", key="emotion", font=("Arial", 20, "bold"))
    pic_search = psg.FileBrowse(key="picsearch", pad=30, button_text="Upload Picture", font=("Arial", 16, "bold"), disabled=True, target="picsearch", enable_events=True)
    take_pic = psg.Button(button_text="Take a Picture", key="livepic", font=("Arial", 16, "bold"), disabled=True)
    submit = psg.Button(button_text="Submit", key="Submit",font=("Arial", 16, "bold"), disabled=True)
    back = psg.Button(button_text="Back", key="BACKRESULTS",font=("Arial", 16, "bold"))
    result_text = psg.Text("", key="resulttext", font=("Arial", 25, "bold"), pad=30)
    photo = psg.Image("", key="testphoto", pad=20)
    chart = psg.Image("", key="chart", pad = 20)
    accuracy = psg.Text("", key="accuracy", font=("Arial", 15, "bold"), pad=20)
    # All the stuff inside your window.
    layoutintro = [[welcome_text],
              [psg.HorizontalSeparator(pad=10)],
              [context],
              [emotion_picker_button],
              [emotion_text],
              [pic_search,take_pic],
                [submit]]

    layoutresult = [[back],
                    [psg.Push(), result_text, psg.Push()],
                    [psg.Push(), photo, chart, psg.Push()],
                    [psg.Push(), accuracy, psg.Push()]
    ]
    layoutmain = [[psg.Column(layoutintro, key="-INTRO-", element_justification="c"), psg.Column(layoutresult, key="-RESULT-", visible=False)]]
    # Create the Window
    window = psg.Window('FacE-ERaTA DEMO', layoutmain, element_justification="c") #size=(700, 500)\

    cam = VideoCapture(0)
    livecamvalidity = checkCamValidity(0)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED:  # if user closes window
            break
        elif event == "EPB":
            emotion = random.choice(emotions)
            window["emotion"].update(emotion)
            window["picsearch"].update(disabled=False)
            window["Submit"].update(disabled=False)
            window["livepic"].update(disabled=False)

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
        elif event == "picsearch":
            picpath = values["picsearch"]
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
            window["-INTRO-"].update(visible=False)
            window["-RESULT-"].update(visible=True)
        elif event == "BACKRESULTS":
            if ".jpg" in picpath.lower() or ".jpeg" in picpath.lower():
                os.remove(new_image_path)
            window["-RESULT-"].update(visible=False)
            window["-INTRO-"].update(visible=True)
    window.close()