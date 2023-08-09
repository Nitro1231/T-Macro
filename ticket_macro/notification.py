import ssl
import smtplib
from windows_toasts import WindowsToaster, ToastText1, ToastDuration


class Notification:
    def send(self, title: str, message: str):
        pass


class DesktopNotification(Notification):
    def __init__(self, duration: any = ToastDuration.Short) -> None:
        super().__init__()
        self.duration = duration


    def send(self, title: str, message: str):
        wintoaster = WindowsToaster(title)
        toast = ToastText1()
        toast.SetBody(message)
        toast.SetDuration(ToastDuration(self.duration))
        wintoaster.show_toast(toast)


class EmailNotification(Notification):
    def __init__(self,
                 host: str,
                 port: int,
                 sender_email: str,
                 sender_password: str,
                 receiver_email: str
                 ) -> None:
        super().__init__()
        self.server = smtplib.SMTP_SSL(host, port, context=ssl.create_default_context())
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email


    def send(self, title: str, message: str):
        try:
            self.server.login(self.sender_email, self.sender_password)
            body = f'Subject: {title}\n\n{message}'
            self.server.sendmail(self.sender_email, self.receiver_email, body.encode('utf-8'))
            self.server.quit()
            print('Message sent successfully!')
        except Exception as e:
            print(f'Failed to send message. Error: {e}')
