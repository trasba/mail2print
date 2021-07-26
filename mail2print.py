#!/usr/bin/env python3
from imap_mail import ImapMail
import file_print
import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)


### we have two safety nets to avoid printing loops
# 1 we only process UNSEEN messages and directly flag those messages to seen
# 2 we move the messages to a folder PROCESSED and only process messages in INBOX

imap = ImapMail(config['imap_server'], config['username'], config['password'])
messages, msg_uids = imap.fetch_unread_messages(config['filter'])
file_paths = []
for message in messages:
    file_paths.append(imap.save_attachment(message, config['folder_path']))
for uid in msg_uids:
    imap.move_message(uid, 'processed')
# moving this explicitly to the end to avoid printing loops
for file_path in file_paths:
    if file_path is not None:
        file_print.file_print(file_path, config['printer'])