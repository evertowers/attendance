import cv2
import face_recognition
import os


def load_known_faces(known_faces_folder):
    known_faces = []
    known_names = []

    for filename in os.listdir(known_faces_folder):
        image = face_recognition.load_image_file(os.path.join(known_faces_folder, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(os.path.splitext(filename)[0])

    return known_faces, known_names

def recognize_faces(frame, known_faces, known_names):
    # Perform face detection on the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Perform face recognition on the detected faces
    face_names = []
    for face_encoding in face_encodings:
        # Compare the face encoding with the known face encodings
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        # Find the best match
        if True in matches:
            matched_index = matches.index(True)
            name = known_names[matched_index]

        face_names.append(name)

    # Draw face bounding boxes and labels on the frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        
    # print("Recognized Faces: ", face_names)

    return frame, face_names[0] if face_names else None
