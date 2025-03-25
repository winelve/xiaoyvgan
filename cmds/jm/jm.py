from jmcomic import *
from command import Command
import os 


class JmCMD(Command):
    def execute(self, args):
        file = download_album_to_pdf(args.id)
        return {"type":"pdf","file":file}

def create_command(config_dict:dict):
    return JmCMD(config_dict)


def download_album_to_pdf(album_id):
    # 配置文件路径
    config_path = './cmds/jm/option.yml'
    
    # 从配置文件创建option
    option = create_option_by_file(config_path)
    
    # 创建客户端
    client = option.new_jm_client()
    
    # 设置PDF路径（使用album_id作为文件名）
    pdf_dir = './data/jm/pdf/'  # 从配置文件中获取
    pdf_path = f"{pdf_dir}{album_id}.pdf"  # 相对路径
    absolute_pdf_path = os.path.abspath(pdf_path)  # 转换为绝对路径
    
    # 下载本子
    download_album(album_id, option)  # 假设配置文件已改为使用Aid
    
    # 返回绝对路径
    return absolute_pdf_path


# 示例调用
if __name__ == "__main__":
    album_id = 438696  # 你可以替换为任意有效的本子ID
    pdf_path = download_album_to_pdf(album_id)
    print(f"PDF路径: {pdf_path}")