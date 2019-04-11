from instruction_graph import BasePrimitiveLibrary
from instruction_graph import ActionPrimitive as Action, ConditionalPrimitive as Cond
from instruction_graph.example.PepperMemory import States
from datetime import datetime as dt
import time


reference_minute = dt.now().time().minute


class PepperPrimitiveLibrary(BasePrimitiveLibrary):

    def list_action_primitives(self):
        return [
            Action(PrimitiveIds.SAY, self.say, "Say", "Perform text to speech on the input argument",
                   match_re_or_fn="say (.*)",
                   argparse_re_or_fn="say (.*)",
                   parsed_description=lambda args: "say %s" % args[0]),
            Action(PrimitiveIds.ROTATE, self.rotate, "Rotate", "Rotate the Robot's base",
                   match_re_or_fn="rotate (right|left) [0-9.]+ radian(s|)",
                   argparse_re_or_fn="rotate (right|left) ([0-9.]+) radian(?:s|)",
                   parsed_description=lambda args: "rotate %s radians %s" % (args[0], args[1])),
            Action(PrimitiveIds.PERSON_FOUND, self.mark_person_found, "Person Found", "Mark Person Found",
                   match_re_or_fn="mark person found",
                   parsed_description=lambda args: "mark person as found"),
            Action(PrimitiveIds.MOVE_FORWARD, self.move_forward, "Move Forward", "Move forward the specified distance.",
                   match_re_or_fn="move forward [.0-9]+ meter(s|)",
                   argparse_re_or_fn="move forward ([0-9.]+) meter(?:s)?",
                   parsed_description=lambda args: "move forward %s meters" % args),
            Action(PrimitiveIds.WHAT_TIME, self.say_what_time,
                   match_re_or_fn=".*what time.*",
                   parsed_description=lambda args: "What time is it?"),
            Action(PrimitiveIds.WHEN_MEETING, self.say_when_is_meeting,
                   match_re_or_fn="(when is my meeting|state meeting time)",
                   parsed_description=lambda args: "when is my meeting"),
            Action(PrimitiveIds.THANK_YOU, self.thank_you,
                   match_re_or_fn="thank you",
                   parsed_description=lambda args: ""),
            Action(PrimitiveIds.CLEANUP, self.cleanup),
        ]

    def list_conditional_primitives(self):
        return [
            Cond(PrimitiveIds.IS_DONE_SEARCHING, self.is_person_found, "is done searching", "status is found person",
                 match_re_or_fn="person found",
                 parsed_description=lambda args: "person found"),
            Cond(PrimitiveIds.IS_HUMAN_VISIBLE, self.is_human_visible, "visible", "is a human visible",
                 match_re_or_fn=".*human.*visible.*",
                 parsed_description=lambda args: "a human is visible"),
        ]

    def library_name(self):
        return "Pepper_Example_Primitive_Library"

    @staticmethod
    def time_from_ref_minute():
        now = dt.now().time().minute
        diff = reference_minute - now
        return diff if diff >= 0 else (60 - reference_minute + now)

    @staticmethod
    def say_what_time(memory):
        now_m = dt.now().time().minute
        now_h = dt.now().time().hour
        PepperPrimitiveLibrary.say(memory, "Current time is %d %d" % (now_h, now_m))

    @staticmethod
    def say_when_is_meeting(memory):
        elapsed = PepperPrimitiveLibrary.time_from_ref_minute()
        PepperPrimitiveLibrary.say(memory, "Hello Aaron. You have %d minutes until your meeting." % (60 - elapsed))
        PepperPrimitiveLibrary.cleanup(memory)

    @staticmethod
    def say(memory, text):
        memory.tts.say(text)

    @staticmethod
    def move_forward(memory, meters):
        meters = float(meters)
        meters = meters - (meters % 0.1)
        angles = [meters, 0, 0]
        motion = memory.motion_service
        motion.moveTo(angles)

    @staticmethod
    def thank_you(memory):
        PepperPrimitiveLibrary.say(memory, "You are welcome")

    @staticmethod
    def rotate(memory, direction, radians):
        if direction not in ['R', 'L', "left", "right"]:
            raise ValueError("'direction' should be 'R' or 'L'")
        radians = float(radians)
        angles = [0, 0, radians if direction in ['L', "left"] else -radians]
        motion = memory.motion_service
        print("Moving to angles", angles)
        motion.moveTo(angles)

    @staticmethod
    def mark_person_found(memory):
        memory.state = States.FOUND_PERSON

    @staticmethod
    def cleanup(memory):
        memory.cleanup()

    @staticmethod
    def is_pepper_searching(memory):
        return memory.state == States.SEARCHING

    @staticmethod
    def is_person_found(memory):
        return memory.state == States.FOUND_PERSON

    @staticmethod
    def is_human_visible(memory):
        time.sleep(1)
        mem_proxy = memory.session.service("ALMemory")
        val = mem_proxy.getData("FaceDetected", 0)
        human_data_exists = (val is not None and isinstance(val, list) and len(val) == 5)
        return human_data_exists


# noinspection PyClassHasNoInit
class PrimitiveIds:
    SAY = "say"
    ROTATE = "rotate"
    PERSON_FOUND = "change_state_to_person_found"
    CLEANUP = "cleanup"
    MOVE_FORWARD = "move_forward"
    WHEN_MEETING = "when_meeting"
    WHAT_TIME = "what_time"
    THANK_YOU = "thank you"

    IS_DONE_SEARCHING = "is_pepper_searching"
    IS_HUMAN_VISIBLE = "is_human_visible"
