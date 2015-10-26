from st2actions.runners.pythonrunner import Action
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail(Action):
    def run(self, email_from, email_to, subject, message, account):
        accounts = self.config.get('imap_mailboxes', None)
        if accounts is None:
            raise ValueError('"imap_mailboxes" config value is required to send email.')
        if len(accounts) == 0:
            raise ValueError('at least one account is required to send email.')

        try:
            account_data = accounts[account]
        except KeyError:
            raise KeyError('The account "{}" does not seem to appear in the configuration. '
                           'Available accounts are: {}'.format(account, ",".join(accounts.keys())))

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to
        msg.attach(MIMEText(message, 'plain'))

        s = SMTP(account_data['server'], account_data['port'], timeout=20)
        s.ehlo()
        s.starttls()
        s.login(account_data['server'], account_data['server'])
        s.sendmail(email_from, email_to, msg.as_string())
        s.quit()
        return
