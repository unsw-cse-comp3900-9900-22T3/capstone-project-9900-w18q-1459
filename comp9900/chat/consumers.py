import time
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import redis

pool = redis.ConnectionPool(
  host="127.0.0.1",
  port=6379,
  max_connections=10,
  decode_response=True,
)
conn = redis.Redis(connection_pool=pool, decode_responses=True)


class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self, ):
    self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
    self.room_group_name = "chat_%s" % self.room_name

    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name,
    )
    await self.accept()

  async def disconnect(self, close_code):
    print("close_code: ", close_code)
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  async def receive(self, text_data=None, bytes_data=None):
    text_data_json = json.loads(text_data)
    message = text_data_json["message"]
    print("receive_message：", message)
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        "type": "chat_message",
        "message": message
      }
    )

  async def chat_message(self, event):
    receive_message = event["message"]
    response_message = "You message is :" + receive_message
    await self.send(text_data=json.dumps({
      "message": response_message
    }))


class PushMessage(WebsocketConsumer):

  def connect(self):
    self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]
    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,
      self.channel_name
    )
    self.accept()

  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      self.room_group_name,
      self.channel_name
    )

  def push_message(self, event):
    """
    主动推送
    :param event:
    :return:
    """
    print(event, type(event))
    while True:
      time.sleep(2)
      msg = time.strftime("%Y-%m-%d %H:%M:%S") + "--- room_name: %s" % event["room_name"]
      self.send(text_data=json.dumps(
        {"message": msg}
      ))