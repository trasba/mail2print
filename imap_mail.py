import imaplib, re, email, os, datetime
import logging_module as logger


class ImapMail():

    connection = None
    error = None
    pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(mailbox = 'INBOX', readonly=False) # so we can mark mails as read

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    def save_attachment(self, message, download_folder='/tmp'):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        filePath = None
        msg_rfc822 = None
        _ret, msg_rfc822 = self.connection.fetch(message,'(RFC822)')
        if msg_rfc822 is None:
            logger.logger.info(f"Error while trying to fetch RFC822 for message {message}")
            print("Error while trying to fetch RFC822 for message", message)
            self.close_connection()
            exit()
        for response_part in msg_rfc822:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                printString =''
                for header in [ 'subject', 'to', 'from' ]:
                    printString += header.upper() + ' ' + msg[header] + ' ' 
                logger.logger.info(printString)
                print(printString)

        # get attachment filename
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            
            if bool(fileName):
                currentDT = datetime.datetime.now()
                timeStamp = currentDT.strftime("%Y%m%d-%H%M%S")
                filePath = os.path.join(download_folder, timeStamp + '_' + fileName)
                logger.logger.info(f'saving attachment to {filePath}')
                print('saving attachment to', filePath)

            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                
        return filePath

    def parse_uid(self, raw_uid):
        """
        Helper function to parse the UID from the returned string
        """
        match = self.pattern_uid.match(raw_uid)
        return match.group('uid')

    def move_message(self, uid, dest_folder='processed'):
        """
        move message with uid to des_folder
        """

        logger.logger.info(f'moving UID: {uid}')
        print('moving UID:', uid)
        result = self.connection.uid('MOVE', uid, dest_folder)
    
    def fetch_unread_messages(self, filter_from):
        """
        Retrieve unread messages
        filter_from = 'OR (HEADER FROM cde) (HEADER FROM domain)'
        """
        emails = []
        result, messages = self.connection.search(None, *filter_from)
        if result == "OK":
            logger.logger.info(f'Found {len(messages[0])} messages')
            print('Found', len(messages[0]), 'messages')
        else:
            logger.logger.info(f"Error while searching with filter: {filter_from}")
            print("Error while searching with filter: ", filter_from)
            self.close_connection()
            exit()
        msg_uids = []
        for message in messages[0].split():
            # flag mail as seen
            _response, _data = self.connection.store(message, '+FLAGS','\\Seen')
            # fetch UID's
            ret, msg_uid = self.connection.fetch(message,'(UID)')
            msg_uids.append(self.parse_uid(msg_uid[0].decode('utf-8')))
        
        return messages[0].split(), msg_uids

    def parse_email_address(self, email_address):
        """
        Helper function to parse out the email address from the message

        return: tuple (name, address). Eg. ('John Doe', 'jdoe@example.com')
        """
        return email.utils.parseaddr(email_address)


if __name__ == '__main__':
    pass