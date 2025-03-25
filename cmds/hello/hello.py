from command import Command

class HelloCMD(Command):
    def execute(self,args):
        print(f'Hello {args.name}.')
        if args.age:
            print(f'You are {args.age} now.')
    

# 这个方法一定要实现
def create_command(config_dict:dict) -> Command:
    """统一接口用于创建对象
    """
    return HelloCMD(config_dict)