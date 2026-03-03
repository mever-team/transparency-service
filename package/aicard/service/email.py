from dotenv import dotenv_values
from typing import Optional
import smtplib, ssl, time, threading
from email.mime.text import MIMEText

def _to_bool(v): return v if isinstance(v, bool) else str(v).lower() in ("1","true","yes","on")


class EmailVerification:
    def __init__(
        self,
        env: Optional[str] = None,
        EMAIL_HOST: Optional[str] = None,
        EMAIL_PORT: Optional[int] = None,
        EMAIL_SENDER: Optional[str] = None,
        EMAIL_USERNAME: Optional[str] = None,
        EMAIL_PASSWORD: Optional[str] = None,
        EMAIL_SMTP_AUTH: Optional[bool] = None,
        EMAIL_SMTP_TLS_ENABLED: Optional[bool] = None,
        EMAIL_SMTP_SSL_ENABLED: Optional[bool] = None,
        EMAIL_TLS_REQUIRED: Optional[bool] = None,
        EMAIL_SSL_PROTOCOLS: Optional[str] = None,
    ):
        config = dotenv_values(env) if env else {}
        self.EMAIL_HOST = EMAIL_HOST or config.get("EMAIL_HOST")
        self.EMAIL_PORT = int(EMAIL_PORT or config.get("EMAIL_PORT", 587))
        self.EMAIL_SENDER = EMAIL_SENDER or config.get("EMAIL_SENDER")
        self.EMAIL_USERNAME = EMAIL_USERNAME or config.get("EMAIL_USERNAME")
        self.EMAIL_PASSWORD = EMAIL_PASSWORD or config.get("EMAIL_PASSWORD")
        self.EMAIL_SMTP_AUTH = _to_bool(EMAIL_SMTP_AUTH if EMAIL_SMTP_AUTH is not None else config.get("EMAIL_SMTP_AUTH", True))
        self.EMAIL_SMTP_TLS_ENABLED = _to_bool(EMAIL_SMTP_TLS_ENABLED if EMAIL_SMTP_TLS_ENABLED is not None else config.get("EMAIL_SMTP_TLS_ENABLED", True))
        self.EMAIL_SMTP_SSL_ENABLED = _to_bool(EMAIL_SMTP_SSL_ENABLED if EMAIL_SMTP_SSL_ENABLED is not None else config.get("EMAIL_SMTP_SSL_ENABLED", False))
        self.EMAIL_TLS_REQUIRED = _to_bool(EMAIL_TLS_REQUIRED if EMAIL_TLS_REQUIRED is not None else config.get("EMAIL_TLS_REQUIRED", True))
        self.EMAIL_SSL_PROTOCOLS = EMAIL_SSL_PROTOCOLS or config.get("EMAIL_SSL_PROTOCOLS", "TLSv1.2")
        self._last_sent = {}
        self._lock = threading.Lock()

    def _allowed(self, email):
        with self._lock:
            now = time.monotonic()
            last = self._last_sent.get(email, 0)
            if now - last < 60: return False # ONE MINUTE BETWEEN RETRIES
            self._last_sent[email] = now
            return True

    def _send_email_worker(self, to_email: str, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.EMAIL_SENDER
        msg["To"] = to_email
        context = ssl.create_default_context()
        try:
            if self.EMAIL_PORT == 465 or self.EMAIL_SMTP_SSL_ENABLED:
                with smtplib.SMTP_SSL(self.EMAIL_HOST, self.EMAIL_PORT, context=context) as server:
                    if self.EMAIL_SMTP_AUTH: server.login(self.EMAIL_USERNAME, self.EMAIL_PASSWORD)
                    server.sendmail(self.EMAIL_SENDER, [to_email], msg.as_string())
            else:
                with smtplib.SMTP(self.EMAIL_HOST, self.EMAIL_PORT) as server:
                    server.ehlo()
                    if self.EMAIL_SMTP_TLS_ENABLED:
                        server.starttls(context=context)
                        server.ehlo()
                    if self.EMAIL_SMTP_AUTH: server.login(self.EMAIL_USERNAME, self.EMAIL_PASSWORD)
                    server.sendmail(self.EMAIL_SENDER, [to_email], msg.as_string())
        except Exception as e:
            print("email send failed for "+to_email+": "+str(e))

    def send_email(self, to_email: str, subject: str, body: str):
        if not self._allowed(to_email): return False
        threading.Thread(
            target=self._send_email_worker,
            args=(to_email, subject, body),
            daemon=True
        ).start()
        return True
