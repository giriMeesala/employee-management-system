import cv2
import mediapipe as mp


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def start_camera():

    cap = cv2.VideoCapture(0)

    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.7
    ) as face_detection:

        while True:

            success, frame = cap.read()

            if not success:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face_detection.process(image)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.detections:

                for detection in results.detections:

                    mp_drawing.draw_detection(image, detection)

            cv2.imshow("Face Detection", image)

            key = cv2.waitKey(1)

            if key == ord("q"):
                break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera()