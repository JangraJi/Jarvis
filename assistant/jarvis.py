import threading

import speech_recognition as sr

from intents.applications import Applications
from intents.greeting import Greeting
from utils.utils import Utils


class Jarvis:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.speech = sr.Recognizer()
        threading.Thread(target=self.run()).start()

    def read_voice_cmd(self):
        print(...)
        voice_input = ''
        try:
            with sr.Microphone() as source:
                audio = self.speech.listen(source=source, timeout=5, phrase_time_limit=5)
            voice_input = self.speech.recognize_google(audio)
            self.logger.info('Input : {}'.format(voice_input))
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print('Network error.')
        except sr.WaitTimeoutError:
            pass
        except TimeoutError:
            pass

        return voice_input.lower()

    def run(self):
        session = False
        while True:
            intent = ''
            voice_note = self.read_voice_cmd()
            for key in self.config:
                utterances = Utils.match_pattern(voice_note, self.config[key]['utterances'])
                if utterances:
                    intent = key
                    response = Utils.choose_random(self.config[key]['response'])
                    break

            if intent == 'intent_greeting':
                Greeting(self.logger, response).speak()
                session = True
                continue
            elif intent == 'intent_applications':
                if session:
                    applications = self.config[key]['applications']
                    Applications(logger=self.logger, response=response, applications=applications,
                                 command=voice_note).launch()
                    session = False
                    continue
