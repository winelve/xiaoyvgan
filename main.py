import json
import argparse
import importlib
import shlex

config_path = './config.json'
cmds_path = 'cmds/'

def load_commands(subparser):
    with open(config_path,'r',encoding='utf-8') as f:
        global_config = json.load(f)
        loading_cmd_list = global_config['commands']
        for cmd_info_dict in loading_cmd_list:
            plugin_name = cmd_info_dict['plugin_name']
            plugin_config_file = cmd_info_dict['config_file']
            plugin_module_path = str(cmds_path + plugin_name + '/' + plugin_name).replace('/','.')
            try:
                pf = open(plugin_config_file,'r',encoding='utf-8')
                plugin_config_dict = json.load(pf)
                
                module = importlib.import_module(plugin_module_path)
                #这个是找到的cmd类
                command = module.create_command(plugin_config_dict)
                parser = subparser.add_parser(name=plugin_config_dict['cmd_name'],help=plugin_config_dict['description'])
                command.setup_parser(parser)
                parser.set_defaults(func=command.execute)
            except FileNotFoundError:
                print(f'配置文件异常: {plugin_config_file}')
            finally:
                pf.close()
        
    
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='cmd')
load_commands(subparser)

cmd_str = 'pixiv 12345 83 435 234 -r 12'
args = parser.parse_args(shlex.split(cmd_str))

if hasattr(args,'func'):
    args.func(args)
    print(args)
else:
    parser.print_help()
