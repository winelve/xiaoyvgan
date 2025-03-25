import json
import websockets

class MessageSegment:
    @staticmethod
    def text(text: str) -> dict:
        return {"type": "text", "data": {"text": text}}

    @staticmethod
    def at(id: str) -> dict:
        return {"type": "at", "data": {"qq": id}}

    @staticmethod
    def image(file: str) -> dict:
        return {"type": "image", "data": {"file": file}}
    
    @staticmethod
    def pdf(file: str) -> dict:
        return {"type": "file", "data": {"file": file}}
    
    

'''
MessageSender方法是用来,发送数据的一个类
'''
class MessageSender:
    def __init__(self, ws):
        self.ws = ws

    async def send_combined(self, target_id: str, messages: list, is_group: bool = False):
        action = "send_group_msg" if is_group else "send_private_msg"
        params = {"group_id" if is_group else "user_id": target_id, "message": messages}
        await self._send(action, params)

    async def _send(self, action: str, params: dict):
        request = {"action": action, "params": params, "echo": f"{action}_{params.get('user_id', params.get('group_id'))}"}
        await self.ws.send(json.dumps(request))
        response = await self.ws.recv()
        print(f"发送响应: {response}")
        
        
