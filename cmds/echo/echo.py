from command import *

class EchoCMD(Command):
    def execute(self, args):
        return args.text

def create_command(config_dict:dict):
    return EchoCMD(config_dict)