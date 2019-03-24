import os
import argparse


from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from flask import Flask, render_template
# [END vision_face_detection_tutorial_imports]

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/Arnold/Documents/emo.json'

# Flask code
app = Flask(__name__)

@app.route('/')
def index():
    picture = request.args['photo']
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)

# [START vision_face_detection_tutorial_send_request]
def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        A string with probable emotion
    """

    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        anger = ('{}'.format(likelihood_name[face.anger_likelihood]))
        joy = ('{}'.format(likelihood_name[face.joy_likelihood]))
        surprise = ('{}'.format(likelihood_name[face.surprise_likelihood]))
        sorrow = ('{}'.format(likelihood_name[face.sorrow_likelihood]))
        emotion = "unknown"
        if(anger == 'POSSIBLE' or anger == 'LIKELY' or anger == 'VERY_LIKELY'):
            emotion = "anger"


        if(joy == 'POSSIBLE' or joy == 'LIKELY' or joy == 'VERY_LIKELY'):
            if(emotion != 'unknown'):
                if( (emotion == 'POSSIBLE') and (joy == 'LIKELY' or joy == 'VERY_LIKELY') ):
                    emotion = "joy"
                if( (emotion == 'LIKELY') and (joy == 'VERY_LIKELY') ):
                    emotion = "joy"
            emotion = "joy"

        if(surprise == 'POSSIBLE' or surprise == 'LIKELY' or surprise == 'VERY_LIKELY'):
            if(emotion != 'unknown'):
                if( (emotion == 'POSSIBLE') and (surprise == 'LIKELY' or surprise == 'VERY_LIKELY') ):
                    emotion = "surprise"
                if( (emotion == 'LIKELY') and (surprise == 'VERY_LIKELY') ):
                    emotion = "surprise"
            emotion = "surprise"

        if(sorrow == 'POSSIBLE' or sorrow == 'LIKELY' or sorrow == 'VERY_LIKELY'):
            if(emotion != 'unknown'):
                if( (emotion == 'POSSIBLE') and (sorrow == 'LIKELY' or sorrow == 'VERY_LIKELY') ):
                    emotion = "sorrow"
                if( (emotion == 'LIKELY') and (sorrow == 'VERY_LIKELY') ):
                    emotion = "sorrow"
            emotion = "sorrow"

        print(anger, joy, surprise, sorrow)

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    return emotion


def main(input_filename):
    with open(input_filename, 'rb') as image:
        emotion = find_emotion(image)
        print(emotion)
        image.seek(0)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects emotion in the given image.')
    parser.add_argument(
        'input_image', help='the face you\'d like to detect emotion in.')
    args = parser.parse_args()

    main(picture)
