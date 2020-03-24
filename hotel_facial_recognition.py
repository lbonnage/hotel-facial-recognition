import face_recognition
import cv2
from PIL import Image
import numpy as np

guest = {}


def add_guest(photo, name):

    image = face_recognition.load_image_file(photo)
    face_encoding = tuple(face_recognition.face_encodings(image)[0])
    guest[name] = face_encoding
#	top, right, bottom, left = face_recognition.face_locations(image)[0]
#	face_image = image[top:bottom, left:right]
#	pil_image = Image.fromarray(face_image)
#	pil_image.show()


def detect_guest():
    pass


def remove_guest(guesst):
    guest.pop(guesst)


def draw_box_around_face(video):
    """

    :param video:
    :return:
    """

    # Open the input movie file
    input_movie = cv2.cv2.VideoCapture(video)
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an output movie file (make sure resolution/frame rate matches input video!)
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    output_movie = cv2.VideoWriter('output.mp4', fourcc, 29.7, (1920, 1080))

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0

    while True:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        frame_number += 1

        # Quit when the input video file ends
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_frame = frame[:, :, ::-1]
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(known_faces[1], face_encoding)
            name = 'Unknown'

            # If a match was found in known_face_encodings, just use the first one.
            if True in match:
                first_match_index = match.index(True)
                name = known_faces[0][first_match_index]

            face_names.append(name)

        # Label the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
                continue
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1, (255, 255, 255), 1)

        # Write the resulting image to the output video file
        print("Writing frame {} / {}".format(frame_number, length))
        output_movie.write(frame)
        # All done!

    input_movie.release()
    cv2.destroyAllWindows()


def valid_guest_detected():
    pass


def invalid_guest_detected():
    pass


known_faces = []


def get_known_faces():

    names = []
    encodings = []
    for name, encoding in guest.items():
        names.append(name)
        encodings.append(encoding)

    known_faces.append(names)
    known_faces.append(encodings)


add_guest('a.jpg', "gakkk")
get_known_faces()

draw_box_around_face('b.mp4')
