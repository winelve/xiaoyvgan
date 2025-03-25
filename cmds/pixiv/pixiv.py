from command import Command

class PixivCMD(Command):
    def execute(self, args):
        return super().execute(args)
    
def create_command(config_dict:dict):
    return PixivCMD(config_dict)