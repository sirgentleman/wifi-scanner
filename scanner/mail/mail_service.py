from functools import reduce
import smtplib, ssl
from email.mime.text import MIMEText


def dict_to_HTMLArray(dictionary_arr):
    if len(dictionary_arr) == 0:
        return "<table></table>"

    return_value = "<table>"
    return_value += "<tr>"
    for element in dictionary_arr[0].keys():
        return_value += "<th>" + element + "</th>"
    return_value += "</tr>"

    for element in dictionary_arr:
        return_value += "<tr>" + reduce(lambda a, b: a + "<td>" + b + "</td>",
                                        element.values()) + "</tr>"

    return return_value + "</table>"


class MailService:
    def __init__(self, mail_sender, mail_password, receiver_mail):

        self._mail_sender = mail_sender
        self._mail_password = mail_password
        self._receiver_mail = receiver_mail

    def send_curr_state(self, currently_connected):

        inner_html = """\
            <html>
                <body>
                    <p>CURRENTLY CONNECTED DEVICES</p>
                    {table}
                </body>
            </html>
            """.format(table=dict_to_HTMLArray(currently_connected))
        message = MIMEText(inner_html, "html")
        message["Subject"] = "[HOME SCANNER] Currently connected devices"
        message["From"] = self._mail_sender
        message["To"] = self._receiver_mail

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                              context=context) as server:
            server.login(self._mail_sender, self._mail_password)
            server.sendmail(self._mail_sender, self._receiver_mail,
                            message.as_string())
