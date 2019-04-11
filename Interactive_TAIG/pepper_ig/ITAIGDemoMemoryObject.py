from instruction_graph.components.Memory import BaseMemory
from enum import Enum


class PepperMemory(BaseMemory):
    def __init__(self, session):
        super(BaseMemory, self).__init__()
        self.session = session
        self.state = States.SEARCHING

        self.faceProxy = self.session.service("ALFaceDetection")
        self.face = "Test_Face"
        self.faceProxy.subscribe(self.face, 500, 0.0)

        self.tts = self.session.service("ALTextToSpeech")
        self.motion_service = self.session.service("ALMotion")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        self.faceProxy.unsubscribe(self.face)

    def memory_name(self):
        return "Pepper_Example_Memory"


class States(Enum):
    SEARCHING = 0
    FOUND_PERSON = 1
