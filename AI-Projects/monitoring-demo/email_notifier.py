import os
import smtplib
from email.message import EmailMessage


def send_email(subject: str, body: str) -> None:
    """
    Sends an email using Gmail SMTP.
    Requires environment variables:
      SMTP_USER (your gmail address)
      SMTP_PASS (gmail app password)
      EMAIL_TO  (destination email address)
    """
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    email_to = os.getenv("EMAIL_TO")

    if not smtp_user or not smtp_pass or not email_to:
        raise RuntimeError(
            "Missing env vars. Set SMTP_USER, SMTP_PASS, and EMAIL_TO before sending email."
        )

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.set_content(body)

    # Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
