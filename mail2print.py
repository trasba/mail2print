#!/usr/bin/env python3
from imap_mail import ImapMail
import file_print
import json, os
import urllib.request

script_path = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(script_path, 'config.json')
with open(config_file_path) as json_data_file:
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
        # for control purposes
        urllib.request.urlopen(config['webhook'] + file_path)