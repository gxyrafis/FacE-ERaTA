from deepface import DeepFace


def emotionWordSwitch(emotion):
    if emotion == "Anger":
        return "angry"
    elif emotion == "Sadness":
        return "sad"
    elif emotion == "Disgust":
        return "disgust"
    elif emotion == "Fear":
        return "fear"
    elif emotion == "Happiness":
        return "happy"
    elif emotion == "Surprise":
        return "surprise"
    elif emotion == "Neutral":
        return "neutral"


def emotionWordSwitchR(emotion):
    if emotion == "angry":
        return "Anger"
    elif emotion == "sad":
        return "Sadness"
    elif emotion == "disgust":
        return "Disgust"
    elif emotion == "fear":
        return "Fear"
    elif emotion == "happy":
        return "Happiness"
    elif emotion == "surprise":
        return "Surprise"
    elif emotion == "neutral":
        return "Neutral"

def emotionAnalysis(picture, emotion, retinaface):
    mode = "opencv"
    if retinaface == True:
        mode = "retinaface"
    emotion = emotionWordSwitch(emotion)
    emotion_analysis = DeepFace.analyze(
        img_path=picture,
        actions=['emotion'],
        detector_backend=mode,
    )
    accuracy = emotion_analysis[0]["emotion"][emotion]
    if emotion_analysis[0]["dominant_emotion"] == emotion:
        return ["Success" , accuracy, emotionWordSwitchR(emotion_analysis[0]["dominant_emotion"])]
    else:
        return ["Failure", accuracy, emotionWordSwitchR(emotion_analysis[0]["dominant_emotion"])]