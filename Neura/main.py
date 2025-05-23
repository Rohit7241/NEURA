import speech_recognition as sr
import webbrowser
import pyttsx3
import pywhatkit
import google.generativeai as genai
from config import GENAI_API

def airesponse(c):
    genai.configure(api_key=GENAI_API)
    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
    response = model.generate_content(f"{c} give response in max 50 words and act as if u are a ai assistant 'Neura'")
    print(response.text)
    return(response.text)

def processCommand(c):
    if(c.lower().startswith("open")):
        web=c.lower().split()[1]
        speak(f"opening {web}")
        webbrowser.open(f"https://{web}.com")
    elif(c.lower().startswith("play")):
        song=' '.join(c.lower().split()[1:])
        speak(f"playing {song} on youtube")
        pywhatkit.playonyt(f"{song}")
    else:
        response=airesponse(c)
        speak(response)

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(txt):
    engine.say(txt)
    engine.runAndWait()

if __name__=="__main__":
    speak("initializing Neura..")
    while True:
    #wake word "Neura"
        r=sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source,timeout=2,phrase_time_limit=2)
            recog=r.recognize_google(audio)
            print(recog)
            recognized=False
            if(recog.lower()=="neura"):
                count=0
                while(recognized==False):
                    try:
                            #listen for command
                        with sr.Microphone() as source:
                            if(count==0):
                                speak("Yes!")
                            audio=r.listen(source,timeout=4)
                            command=r.recognize_google(audio)
                            print(command)
                            processCommand(command)
                            recognized=True
                    except Exception as e:
                        count+=1
                        if count < 2:
                            speak("Couldn't recognize Speak again.")
                        else:
                            speak("Still couldn't understand Try again later.")
                            break
        except Exception as e:
            print(f"ERROR {e}")