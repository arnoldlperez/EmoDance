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
# [END vision_face_detection_tutorial_imports]

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/Arnold/Documents/emo.json'


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


# [START vision_face_detection_tutorial_run_application]
def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        emotion = detect_face(image, max_results)
        print(emotion)
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

    main(args.input_image, args.output, args.max_results)
