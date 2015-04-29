#!/usr/bin/python
import sys

import avango
import avango.gua
import avango.script

from examples_common import device

import jsonloader


class Reloader(avango.script.Script):

    Keyboard = device.KeyboardDevice()

    def __init__(self):
        self.super(Reloader).__init__()
        self.always_evaluate(True)

        self.KeyR = False

    def myConstructor(self, json_path, root):
        self.loader = jsonloader.jsonloader()
        self.json_path = json_path
        self.root = root
        # self.pipe = pipe
        self.reload()

    def get_window(self, window_str):
        return self.loader.windows[window_str]

    def get_scenegraph(self, sg_str):
        return self.loader.scenegraphs[sg_str]

    def reload(self):
        self.root.Children.value = []
        self.loader.load_json(self.json_path, self.root)
        # self.loader.load_and_set_PipelineOptions(self.pipe)

    def evaluate(self):
        if self.Keyboard.KeyR.value and not self.KeyR:
            pass
            # self.reload()
        self.KeyR = self.Keyboard.KeyR.value


def start():

    loader = jsonloader.jsonloader()
    app = loader.create_application_from_json(sys.argv[1])
    app.run()


if __name__ == '__main__':
    start()
