
# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, ChatRoom
from profiles.models import Profile

class ChatConsumer(AsyncWebsocketConsumer):


	
	async def connect(self):
		self.roomGroupName = "group_chat_gfg"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
		#print('------async def connect(self):-----------')
		
	async def disconnect(self , close_code):
		# await self.channel_layer.group_discard(
		# 	self.roomGroupName , 
		# 	self.channel_layer 
		# )
		await self.channel_layer.group_discard(
        self.roomGroupName,
        self.channel_name,
    )

		#print('------async def disconnect(self, close_code):-----------')


	async def receive(self, text_data):
		# Lấy từ chat.html qua
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		slug = text_data_json["slug"]
		profileId = text_data_json["profileId"]
		# print(f'Nhận vào từ chat.html: messageId={messageId}')
		# Gửi qua hàm sendMessage
		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"message" : message , 
				"username" : username,
				"chatroom_slug" : slug,
				"profileId" : profileId,


			})
		#print("------async def receive(self, text_data):-----------")

	async def sendMessage(self, event):	
		message = event["message"]
		username = event["username"]
		chatroom_slug = event["chatroom_slug"]
		profileId = event["profileId"]

		# Asynchronously get the chatroom and profile
		chatroom = await database_sync_to_async(ChatRoom.objects.get)(slug=chatroom_slug)
		profile = await database_sync_to_async(Profile.objects.get)(id=profileId)

		# Asynchronously create the message
		message = await database_sync_to_async(Message.objects.create)(
			sender=profile, chatroom=chatroom, text=message
		)
		# Send the message
		await self.send(text_data=json.dumps({"message": message.text, "username": username}))
				# Thêm messageId vào tập hợp đã xử lý
		
		
		print("Sent message")




