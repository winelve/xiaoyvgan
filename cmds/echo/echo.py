from command import *

class EchoCMD(Command):
    def execute(self, args) -> Dict[str,str]:
        return self.to_dict('text',args.text)

def create_command(config_dict:dict):
    return EchoCMD(config_dict)