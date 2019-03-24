#!/usr/bin/env python

# Copyright 2015 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Draws squares around detected faces in the given image."""
import os
import argparse

# [START vision_face_detection_tutorial_imports]
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
        An array of Face objects with information about the picture.
    """
    # [START vision_face_detection_tutorial_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_face_detection_tutorial_client]

    content = face_file.read()
    image = types.Image(content=content)
    
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        # if(face.anger_likelihood == 'POSSIBLE' | face.anger_likelihood == 'LIKELY' | face.anger_likelihood == 'VERY_LIKELY'):
        #     emotion = "anger"
        # if(face.joy_likelihood == 'POSSIBLE' | face.joy_likelihood == 'LIKELY' | face.joy_likelihood == 'VERY_LIKELY'):
        #     emotion = "joy"
        # if(face.surprise_likelihood == 'POSSIBLE' | face.surprise_likelihood == 'LIKELY' | face.surprise_likelihood == 'VERY_LIKELY'):
        #     emotion = "surprise"
        emotion = 0
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    return emotion


def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  fill='#FF0000')
    im.save(output_filename)
# [END vision_face_detection_tutorial_process_response]





# [START vision_face_detection_tutorial_run_application]
def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        emotion = detect_face(image, max_results)
        print(emotion)


        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        #highlight_faces(image, faces, output_filename)
# [END vision_face_detection_tutorial_run_application]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects faces in the given image.')
    parser.add_argument(
        'input_image', help='the image you\'d like to detect faces in.')
    parser.add_argument(
        '--out', dest='output', default='out.jpg',
        help='the name of the output file.')
    parser.add_argument(
        '--max-results', dest='max_results', default=4,
        help='the max results of face detection.')
    args = parser.parse_args()

    main(picture, args.output, args.max_results)
