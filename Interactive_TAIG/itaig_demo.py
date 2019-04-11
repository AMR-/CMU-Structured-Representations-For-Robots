#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import sys
import argparse
import time
from instruction_graph.interactive.InteractiveManager import InteractiveManager
from pepper_ig.ITAIGDemoMemoryObject import PepperMemory
from pepper_ig.ITAIGDemoPrimitiveLibrary import PepperPrimitiveLibrary


class InteractiveTAIGDemo(object):

    def _on_word_recognized(self, value):
        phrase = value[0]
        confidence = value[1]
        print("On word reg detected:\n%s with confidence %f" % (phrase, confidence))
        if confidence > self._min_confidence and self._listening:
            self._last_phrase_heard = phrase

    def __init__(self, app):
        super(InteractiveTAIGDemo, self).__init__()
        app.start()
        session = app.session
        self._min_confidence = 0.52
        self._last_phrase_heard = None
        self._listening = True
        self.tts = session.service("ALTextToSpeech")
        self.mem = session.service("ALMemory")
        self.sr = session.service("ALSpeechRecognition")
        self._setup_vocab_listener()
        self.stop = False
        self.osd_sub = self.mem.subscriber("WordRecognized")
        self.osd_sub.signal.connect(self._on_word_recognized)

        self.im = InteractiveManager(library=PepperPrimitiveLibrary(),
                                     memory=PepperMemory(session))
        self.im.ig_dir = "pepper_ig/taigs/"

        self.tts.say("Ready.")
        self.sec_ct = 0
        while not self.stop:
            self.respond_to_speech()
            if self.sec_ct > 1000:
                self.tts.say("Timeout.")
                self.stop = True
        # self.tts.say("Stopping.")
        self.sr.unsubscribe("Test_ASR")

    def _setup_vocab_listener(self):
        self.sr.deleteAllContextSets()
        self.sr.setLanguage("English")
        self.sr.pause(True)
        vocabulary = ["yes", "no", "thank you", "stop",
                      "Done learning",
                      "Else", "End If", "End Loop",
                      "I will teach you to spin search",
                      "I will teach you to find me and remind me of a meeting",
                      "If a human is visible",
                      # "Move forward one meter",
                      "Move forward 1 meter",
                      "Mark person found",
                      "Pepper, what time is it?",
                      "Rotate left 0.78 radians", "Rotate right 0.78 radians",
                      "Run spin search", "Run find me and remind me of a meeting",
                      "say no one is in front of me",
                      "State meeting time",
                      "While not person found"]
        print("Vocabulary is")
        print(vocabulary)
        self.sr.setVocabulary(vocabulary, False)
        self.sr.pause(False)

        # Start the speech recognition engine with user Test_ASR
        self.sr.subscribe("Test_ASR")
        print('Speech recognition engine started')

    def respond_to_speech(self):
        self.sec_ct = self.sec_ct + 1
        print(self.sec_ct)
        time.sleep(1)
        if self._last_phrase_heard:
            self._listening = False
            if self._last_phrase_heard == "stop":
                self.stop = True
                self.tts.say("stopping")
            else:
                if self._last_phrase_heard == "thank you":
                    self.stop = True
                # self.tts.say("Heard %s" % self._last_phrase_heard)
                response = self.im.parse_input_text(self._last_phrase_heard)
                if response:
                    self.tts.say(response)
            self._listening, self._last_phrase_heard = True, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--speech", type=str, default=None,
                        help="Speech to say")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        qi_app = qi.Application(["StandInit", "--qi-url=" + connection_url])
        tsr = InteractiveTAIGDemo(qi_app)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n")
        sys.exit(1)
