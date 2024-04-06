from django.shortcuts import render,HttpResponse,redirect
from .forms import *
import sys 
from moviepy.editor import *
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pydub import AudioSegment
import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . serializers import ItemSerializer
from . models import *
import cv2



# Create your views here.

@api_view(['GET'])

def getData(reqeust):
    app=voicerec.objects.all()
    serializer=ItemSerializer(app,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def postData(request):
    serializer=ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)









#???????????????????????????????????{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}






def index(request):
    text=''
    form=''
    data=''
    if request.method=='POST':
        video=request.FILES.get('vid')
        if video.name.endswith('.mp4'):
            mp4_file=video
            filevideo=VideoFileClip(mp4_file.temporary_file_path())
            audio1=filevideo.audio
            au1=f"{mp4_file}.wav"
            audio1.write_audiofile(au1)
            audio1.close()
            filevideo.close()
            print("Successfull extract audio")
            r=sr.Recognizer()
            fileaudio=sr.AudioFile(au1)

            with fileaudio as source:
                audio_text=r.record(source)

            print(type(audio_text))
# filtering text from the audio text :
            audiodata=r.recognize_google(audio_text)
            fillter_words=['is','um','world','like','you Know','so','very','actually','literally','wake','up','to','realty']
            audiodatalower=audiodata.lower()
            filtertext=list(set(word for word in fillter_words if word in audiodatalower))
            print(filtertext)

            data=videoupload()
            data1=voicerec()
            data.videos=video
            data1.videos=video
            data.caption=audiodata
            data1.caption=audiodata
            data.save()

            data1.VideoTitle=mp4_file
            data1.audioTitle=au1
            data1.filter_words=filtertext

        # return render(request,"result.html",) 

# _______________________________________________________
# SentimentIntensity Analyzer :
# """/Sentiment Analysis is the process of 'computationally'
#  determining whether a piece of writing is positive,
#    negative or neutral. It's also known as opinion mining, 
# deriving the opinion or attitude of a speaker./"""
            sid=SentimentIntensityAnalyzer()
            sentiment_scores=sid.polarity_scores(audiodata)
            print(sentiment_scores)
            sentiment_scores_average=(sentiment_scores['compound']+1)/2

            #Determine sentiment based on the compound score

            if sentiment_scores['compound']>=0.05:
                print("Positive")
                Sentiment="Positive"
            elif  sentiment_scores['compound']<=0.05:
                print("Negative")
                Sentiment="Negative"
            else:
                print("Neutral")
                Sentiment="Neutral"

            data1.sentiment_scores_compound=Sentiment
            data1.sentiment_scores=sentiment_scores
            data1.sentiment_scores_average=sentiment_scores_average

            

            
            
            # Voice_monotone:A monotone voice is one that stays at
            #  the same level of pitch, tone, volume, speed, and pauses throughout the speech.
 
            audio =AudioSegment.from_file(au1)
            sample=np.array(audio.get_array_of_samples())
            # Calculate the roop mean square (RMS) of the audio signal 
            rms =np.sqrt(np.mean(np.square(sample)))
            data1.RMS=rms

            # Print the RMS value for reference
            print("RMS",rms)
            #Set a threshold for determinig monotone or clear voice
            min_threshold=20 #Adjust this threshold based on your observations
            max_threshold=50

            # Check if the RMS value is below the threshold

            if min_threshold<rms<max_threshold:
                print("Voice is clear")
                voiceThreshold="Voice is Clear"
            else:
                print("voice is monotone/noise")
                voiceThreshold="Voice is Too Bad or Monotone"

            data1.RMS_threshold=voiceThreshold



        # PERFORM VOICE MODULATION ANALYSIS 

            audio=AudioSegment.from_wav(au1)
            
            pitch=audio.dBFS


            # Check if pitch is -inf and handle it

            if pitch==float('-inf'):
                pitch=None

            min_pitch=-40
            max_pitch=0
            data1.Pitch=pitch
            # Calculate the percentage of voice modulation

            if pitch is not None:
                percentage_modulation=(pitch - min_pitch)/(max_pitch - min_pitch)*100
                percentage_modulation=max(0,min(100,percentage_modulation)) # Ensure it's within the 0-100 range
            else:
                percentage_modulation=0
            data1.percentage_modulation=percentage_modulation
            
            # You can define your own criteria for ratiing voice modulation

            if pitch is not None:
                if pitch>-12:
                    modulation_rating="Excellent"
                elif -12>=pitch>=-27:
                    modulation_rating="Good"
                else:
                    modulation_rating="Need Improvement"
            else:
                modulation_rating="Not Available"
            
            data1.Modulation_rating=modulation_rating
            data1.save()

            print( f"Pitch:{round(pitch,2)}\n Percentage Modulation:{round(percentage_modulation,2)}\n Modulation_rating:{modulation_rating}")
            








    return render(request,"index.html",{"data":data})



   


#________________________________________________________________________________________
# _____________face Detected_______________________________
    

                
def  detect_face(request):

    if request.GET:

        def detect_faces_live(output_filename="videoname.mp4",f_w=640,f_h=480,fps=20.0):
            fourcc=cv2.VideoWriter_fourcc(*'mp4v')
            out=cv2.VideoWriter(output_filename,fourcc,fps,(f_w,f_h))

    # Load the pre-trained Haar Cascade classifier for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # Start capturing video from the camera
            cap = cv2.VideoCapture(0)  # 0 is the default camera index, change it if you have multiple cameras

            while True:
                # Read the frame from the camera
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert the frame to grayscale (necessary for face detection)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                # Draw rectangles around the faces
                i=0
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0),2)

                    # Increment 
                    i=i+1

                    cv2.putText(frame,'face num'+str(i),(x-10,y-10),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                    
                print(i)

                    

                out.write(frame)
                # Display the frame with face rectangles
                cv2.imshow('Face Detection', frame)

                # Check for the 'q' key to quit the program
                if cv2.waitKey(1) & 0xFF == ord('q'):

                    break
                    
                
            # Release the camera and close all OpenCV windows
            cap.release()
            out.release()
            cv2.destroyAllWindows()


        videoname=request.GET["nam"]
        detect_faces_live(videoname+str(".mp4"))

    return render(request,'facelive.html')



        

        