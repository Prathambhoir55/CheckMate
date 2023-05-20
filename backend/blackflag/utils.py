import face_recognition

def calculate_encodings(image):
    encodings = face_recognition.face_encodings(image, model="small")[0]
    return encodings

def compare_faces(encodings_list, unknown_encoding):
    results = face_recognition.compare_faces(encodings_list, unknown_encoding, tolerance=0.45)
    return results