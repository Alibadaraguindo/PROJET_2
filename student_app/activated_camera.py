from datetime import datetime
import cv2
import face_recognition
from student_app.models import Marking,ClassSession,Module,ModuleAssociate
from student_app.models import Student
from datetime import datetime
import re
def preprocess_student_images():
    student_encodings = {}
    students = Student.objects.all()
    for student in students:
        try:
            if student.photo:  # Vérifiez si l'étudiant a une photo
                student_photo = student.photo
                print(f"Student: {student.first_name} {student.last_name}, Photo: {student_photo}")
                image_to_detect = face_recognition.load_image_file(student_photo.path)
                face_encoding = face_recognition.face_encodings(image_to_detect)[0]
                student_encodings[f"{student.first_name} {student.last_name}"] = face_encoding
        except Exception as e:
            print(f"Error processing student {student.first_name} {student.last_name}: {e}")
    return student_encodings


from datetime import datetime, time


def get_current_class_session(teacher):
    try:
        current_datetime = datetime.now().time()
        
        # Get all module associations for the given teacher
        module_associates = ModuleAssociate.objects.filter(teacher=teacher)
        print(module_associates);
        modules = [module_assoc.module for module_assoc in module_associates]

        # Check if modules list is empty
        if not modules:
            print("No modules associated with the teacher.")
            return None

        for module in modules:
            # Get all class sessions for the current module
            class_sessions = ClassSession.objects.filter(module=module)
            for class_session in class_sessions:
                # Check if both heureDebut and heureFin are set
                if class_session.heureDebut and class_session.heureFin:
                    # Compare current time with class session times
                    if class_session.heureDebut <= current_datetime <= class_session.heureFin:
                        return class_session
                else:
                    print(f"Class session {class_session.id} does not have valid start and end times.")

        # No active class session found
        print("No current class session found for the teacher.")
        return None

    except ClassSession.DoesNotExist:
        # Handle case where no class sessions are found
        print("ClassSession.DoesNotExist exception caught.")
        return None





def camera_maked(student_encodings, teacher):

    current_class_session = get_current_class_session(teacher)
    if current_class_session is None:
        print("Aucune séance de cours n'a été trouvée pour ce professeur.")
        print(f"Date du jour : {datetime.now()}")
        return
    
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            for student, encoding in student_encodings.items():
                student_name = student
                
                match = face_recognition.compare_faces([encoding], face_encoding, tolerance=0.3)
                if match[0]:
                    print(f"Match found for student: {student_name}") 
                    
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, student_name, (left, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 1)
                    
                    try:
                        student_obj = Student.objects.get(first_name=student.split()[0], last_name=student.split()[1])
                        if Marking.objects.filter(code_massar=student_obj, class_session=current_class_session).exists():
                            print("Vous êtes déjà marqué")
                        else:
                            marking = Marking.objects.create(code_massar=student_obj, class_session=current_class_session, status=True)
                            marking.save()
                    except Exception as e:
                        print(f"Error creating marking for student {student_name}: {e}")

                    break

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()