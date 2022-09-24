#!/usr/bin/env python3
# A script which is meant to be run periodically (i.e. each minute) to send scheduled Telegram messages in specified chats at the right time (given that Telegram itself is doing a bad job at this). Also re-schedules messages which contain the text `#draft' to a day later indefinitely (useful for public channel posting).

import time, socket, asyncio, os.path, datetime, operator, telethon
from config import PEERS, API_ID, API_HASH

client = telethon.TelegramClient('telegram-scheduled-fix', API_ID, API_HASH, device_model=socket.gethostname(), app_version=os.path.splitext(os.path.basename(__file__))[0].join('()'))

async def main():
	now = datetime.datetime.now(tz=datetime.timezone.utc)
	past = (now - datetime.timedelta(minutes=2))
	soon = (now + datetime.timedelta(minutes=2))

	async with client:
		for peer in PEERS:
			messages = (await client(telethon.functions.messages.GetScheduledHistoryRequest(peer, 0))).messages

			if (tosend := sorted(m.id for m in messages if past <= m.date <= now and '#draft' not in m.message)):
				print(f"[{time.strftime('%x %X')}] Sending {len(tosend)} message{'s'*(len(tosend)>1)} to {peer}: {', '.join(map(str, tosend))}")
				await client(telethon.functions.messages.SendScheduledMessagesRequest(peer, tosend))

			if (tohold := sorted((m for m in messages if now <= m.date <= soon and '#draft' in m.message), key=operator.attrgetter('id'))):
				print(f"[{time.strftime('%x %X')}] Holding {len(tohold)} message{'s'*(len(tosend)>1)} to {peer}: {', '.join(str(m.id) for m in tohold)}")
				await asyncio.gather(*(client.edit_message(m, schedule=m.date+datetime.timedelta(days=+1)) for m in tohold))

if (__name__ == '__main__'): exit(asyncio.run(main()))

# by Sdore, 2021-22
#   www.sdore.me
