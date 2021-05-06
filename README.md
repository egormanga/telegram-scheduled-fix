# telegram-scheduled-fix

A script which is meant to be run periodically (i.e. each minute) to send scheduled Telegram messages in specified chats at the right time (given that Telegram itself is doing a bad job at this). Also re-schedules messages which contain the text `#draft' to a day later indefinitely (useful for public channel posting).
