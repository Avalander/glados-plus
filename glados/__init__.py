'''This module provides mock interfaces for used GLaDOS2 classes'''

class Help(object):
    def __init__(self, command, argument_list, description):
        pass

    def get(self):
        pass

class Module(object):
    def __init__(self):
        self.client = None

    @staticmethod
    def commands(*command_list):
        pass
