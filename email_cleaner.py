import imaplib
import email
from email.header import decode_header

# Konfigurationsdatei mit E-Mail-Einstellungen
email_config = {
    'gmx': {
        'username': 'IhrBenutzername',
        'password': 'IhrPasswort',
        'imap_url': 'imap.gmx.net',
        'domains_to_delete': ['domain1.com', 'domain2.com']
    },
    # Fügen Sie hier weitere E-Mail-Anbieter hinzu...
}

for provider, config in email_config.items():
    # Verbindung zum Server herstellen
    mail = imaplib.IMAP4_SSL(config['imap_url'])

    # Anmelden
    mail.login(config['username'], config['password'])

    # Wählen Sie den Posteingang oder den gewünschten Ordner aus
    mail.select("inbox")

    # Alle Mails durchsuchen
    result, data = mail.uid('search', None, "ALL")
    inbox_item_list = data[0].split()

    for item in inbox_item_list:
        result2, email_data = mail.uid('fetch', item, '(BODY[HEADER.FIELDS (FROM)])')
        raw_email = email_data[0][1].decode("utf-8")
        email_message = email.message_from_string(raw_email)

        # Absender der Email bekommen
        fromaddr = email.utils.parseaddr(email_message['From'])[1]
        domain = fromaddr.split('@')[1]

        # Wenn die Domain in der Liste ist, löschen Sie die Email
        if domain in config['domains_to_delete']:
            mail.uid('STORE', item, '+FLAGS', '(\Deleted)')
    mail.expunge()
