import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def SendEmailTo(email):
    content = MIMEMultipart()  # 建立MIMEMultipart物件
    content["subject"] = "[違規] 停車違規通知"  # 郵件標題
    content["from"] = "tsmcscserver@gmail.com"  # 寄件者
    content["to"] = email  # 收件者
    content.attach(MIMEText("您好:\
        \n    您的車輛已違規停放，請盡速停妥。\
        \n    謝謝您的配合"))  # 郵件純文字內容
    # content.attach(MIMEImage(Path("koala.jpg").read_bytes()))  # 郵件圖片內容

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("tsmcscserver@gmail.com", "mdsysfucgilrrnef")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)