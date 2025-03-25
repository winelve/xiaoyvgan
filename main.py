import asyncio
import json
from typing import Dict, Optional, Union
import shlex

import websockets

import parse
from utils import *


parser,cmd_lists = parse.get_parser()
def extract_message_info(msg: Union[str, bytes]) -> Dict[str, Optional[str]]:
    """
    从 OneBot v11 消息中提取关键信息，适配 WebSocket 接收的数据。
    
    参数:
        msg (Union[str, bytes]): WebSocket 接收到的消息（可能是字符串或字节）
    
    返回:
        Dict[str, Optional[str]]: 包含提取信息的字典，未找到的字段值为 None
    """
    try:
        # 如果是 bytes 类型，先解码为字符串
        if isinstance(msg, bytes):
            msg_str = msg.decode('utf-8')
        else:
            msg_str = str(msg)  # 确保是字符串
        
        # 解析 JSON 消息
        msg_json = json.loads(msg_str)
        
        # 提取基本字段
        info = {
            "group_id": None,           # 群聊 ID（仅群聊消息有）
            "user_id": str(msg_json.get("user_id")),  # 用户 ID
            "nickname": msg_json.get("sender", {}).get("nickname"),  # 用户昵称
            "time": str(msg_json.get("time")),      # 时间戳
            "message": None,            # 发送的消息内容
            "message_type": msg_json.get("message_type"),  # 消息类型（private/group）
            "message_id": str(msg_json.get("message_id"))  # 消息 ID
        }
        
        # 处理群聊 ID（仅群聊消息有）
        if msg_json.get("message_type") == "group":
            info["group_id"] = str(msg_json.get("group_id"))
        
        # 提取消息内容
        if msg_json.get("message_format") == "array":
            # 数组格式，遍历 message 列表提取文本
            message_content = ""
            for segment in msg_json.get("message", []):
                if segment.get("type") == "text":
                    message_content += segment.get("data", {}).get("text", "")
            info["message"] = message_content
        else:
            # 如果是其他格式，直接取 raw_message
            info["message"] = msg_json.get("raw_message")
        
        return info
    
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
    except Exception as e:
        return {"error": f"Error processing message: {str(e)}"}


def is_valid_cmd(msg:str)->bool:
    if msg:
        split_cmds = msg.split()
        return (split_cmds[0] in cmd_lists)
    return False

class CommandHandler:
    def __init__(self, parser):
        self.parser = parser

    def handle(self, text: str) -> Optional[str]:
        """处理命令文本，返回执行结果或错误信息"""
        if not is_valid_cmd(text):
            return None

        try:
            split_text = shlex.split(text)
            args = self.parser.parse_args(split_text)

            if hasattr(args, 'func'):
                return args.func(args)
            else:
                print(f'命令 {split_text[0]} 未注册方法.')
                return '似乎这个命令还没有注册方法，请检查一下 miao~.'

        except SystemExit:
            print(f'命令 {split_text[0]} 用法错误.')
            return '用法错误 miao~'
        except Exception as e:
            print(f'执行命令 {split_text[0]} 时发生错误: {str(e)}')
            return f'执行命令时发生错误: {str(e)}'




async def work(msg, handler: CommandHandler,sender: MessageSender):
    """
    处理接收到的消息，执行命令并发送结果。
    
    参数:
        msg: WebSocket 接收到的消息（字符串或字节）
        sender: MessageSender 实例，用于发送消息
    """
    # 提取消息信息
    msg_dict = extract_message_info(msg)
    text = msg_dict.get("message")
    if not text:
        return

    # 处理命令
    result = handler.handle(text)

    # 如果有结果，则发送消息
    if result:
        if msg_dict.get('group_id'):
            
            await sender.send_combined(
                target_id=msg_dict['group_id'],
                messages=[MessageSegment.text(result)],
                is_group=True
            )
            
        elif msg_dict.get('user_id'):
            
            await sender.send_combined(
                target_id=msg_dict['user_id'],
                messages=[MessageSegment.text(result)],
                is_group=False
            )

async def main():
    uri = "ws://127.0.0.1:3001"
    headers = {"Authorization": "napcat"}  # 换成 WebUI 里的 token
    handler = CommandHandler(parser)
    async with websockets.connect(uri, extra_headers=headers) as ws:
        print("成功连上 NapCat 的 WebSocket！")
        sender = MessageSender(ws)  # 创建 MessageSender 实例
        while True:
            msg = await ws.recv()
            await work(msg, handler, sender)  # 传入 parser,sender
            


asyncio.run(main())