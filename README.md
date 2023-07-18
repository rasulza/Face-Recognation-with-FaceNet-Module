# Face-Recognation-with-FaceNet-Module
Face Recognation with FaceNet Module and queue management by face

### language & tools 
- opencv
- numpy
- FaceNet
- django
- python

# Face Recognition Project using FaceNet

This project is a face recognition system that utilizes the FaceNet model for face detection and recognition. The system is developed using Python and Django framework.

## Features

- Real-time face detection using the Haar Cascade classifier
- Face recognition using the FaceNet model
- Integration with Django framework for web-based interface
- Tracking the number of breads ordered by customers

## Installation

1. Clone the repository:
  git@github.com:Russell-zabanbar/Face-Recognation-with-FaceNet-Module.git
2. Install the required dependencies:
  pip install -r requirements.txt

3. Download the pre-trained FaceNet model and place it in the appropriate directory.

## Usage

1. Run the Django development server:
  python manage.py runserver


# Discription
After opening the device's camera through OpenCV, immediately after recognizing a face, a shot of his face will be taken, and then after extracting the features of the person's face in the photo, it will be compared with all the extracted features of the previous photos and from Through the Euclidean model, if a face is close to the input face, it will be identified and the person's order information will be shown to it, otherwise the user is a new user and we will register a new order for him.




