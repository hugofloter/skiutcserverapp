from config import _SMTPS_MAIL, _MAIL_SKIUTC, _MAIL_LOGIN, _MAIL_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from time import sleep
from smtplib import SMTPException, SMTP
from utils.errors import Error


class Mail():
    def __init__(self):
        self.server = SMTP(_SMTPS_MAIL, 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(_MAIL_LOGIN, _MAIL_PASSWORD)

    @staticmethod
    def batch_maker(list_mail, n=1):
        batch = len(list_mail)
        for ndx in range(0, batch, n):
            yield list_mail[ndx:min(ndx + n, batch)]

    def mail_sender(self, target, subjet, body):
        fromaddr = _MAIL_SKIUTC
        toaddr = target
        msg = MIMEMultipart()
        msg['From'] = "SKI'UTC <"+fromaddr+">"
        msg['To'] = toaddr
        msg['Subject'] = subjet
        text = MIMEText(self.use_template(body), 'html')
        msg.attach(text)
        try:
            self.server.sendmail(fromaddr, toaddr, msg.as_string())
        except SMTPException as e:
            print(e)
            return Error('Error happend during sending e-mail', 501).get_error()
        self.server.quit()

    def massive_mail_sender(self, list_mail, subjet, body):
        fromaddr = _MAIL_SKIUTC
        msg = MIMEMultipart()
        msg['From'] = "SKI'UTC <"+fromaddr+">"
        msg['Subject'] = subjet
        text = MIMEText(self.use_template(body), 'html')
        msg.attach(text)
        for batch in self.batch_maker(list_mail, 40):
            for mail in batch:
                try:
                    msg['To'] = mail
                    self.server.sendmail(fromaddr, mail, msg.as_string())
                except SMTPException as e:
                    print(e)
                    return Error('Error happend during sending e-mail', 501).get_error()
            sleep(60)

        self.server.quit()

    def use_template(self, body):
        mail_template = """
        {}
        <br>
        Ton Roger 
        ❄
        """.format(body)

        return mail_template
