import threading
from django.core.mail import send_mail
from django.conf import settings


class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list, html_message=None):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=False,
            html_message=self.html_message,
        )


def send_verification_email(username, email, verification_token):
    """
    Send email verification link to user
    """
    verification_url = f"http://127.0.0.1:8000/api/auth/verify-email/{verification_token}"
    
    subject = 'Verify Your Email Address'
    
    # Plain text version
    message = f"""Hello {username},

Welcome to our platform! Please verify your email address to activate your account.

Click the link below to verify your email:
{verification_url}

This link will expire in 24 hours.

If you didn't create an account, please ignore this email.

Best regards,
The Team"""
    
    # HTML version
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #667eea;">Welcome to Our Platform!</h2>
            <p>Hello <strong>{username}</strong>,</p>
            <p>Thank you for signing up! Please verify your email address to activate your account.</p>
            
            <div style="margin: 30px 0;">
                <a href="{verification_url}" 
                   style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white;
                          padding: 12px 30px;
                          text-decoration: none;
                          border-radius: 5px;
                          display: inline-block;
                          font-weight: bold;">
                    Verify Email Address
                </a>
            </div>
            
            <p style="color: #666; font-size: 14px;">
                Or copy and paste this link into your browser:<br>
                <a href="{verification_url}" style="color: #667eea;">{verification_url}</a>
            </p>
            
            <p style="color: #999; font-size: 12px; margin-top: 30px;">
                This link will expire in 24 hours.<br>
                If you didn't create an account, please ignore this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    recipient_list = [email]
    
    EmailThread(subject, message, recipient_list, html_message).start()
