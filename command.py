class Command:
    def __init__(self, config_dict):
        # self.name
        self.name = config_dict['cmd_name']
        self.description = config_dict['description']
        self.args = config_dict['arguments']
        self.type_change = {'int':int,'str':str}
    
    def setup_parser(self,parser):
        """传入对应的subparser,自动为其设置参数
        """
        for arg in self.args:
            # 先进行类型转换和检查
            if arg['kwargs'].get('type'):
                if arg['kwargs']['type'] in self.type_change.keys():
                    arg['kwargs']['type'] = self.type_change.get(arg['kwargs']['type'])
            
            #这个地方要注意,一个参数,正常来说,就只能做,"位置参数",或者指定为选项参数
            if "flags" in arg:
                parser.add_argument(*arg["flags"], **arg["kwargs"])
            elif "name" in arg:
                parser.add_argument(arg["name"], **arg["kwargs"])
                
    
    def execute(self,args):
        '''请确保自己知道args的内容'''
        print('base class of command')
        pass







