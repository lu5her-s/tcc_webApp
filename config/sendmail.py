from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# Assuming your Profile model is in the same app
# If not, adjust the import path accordingly
from account.models import Profile


class SendMail:
    def __init__(self, user, content):
        self.user = user
        self.content = content

    def send(self):
        try:
            profile = Profile.objects.get(user=self.user)
            recipient_email = profile.email

            send_mail(
                "Notification",  # Subject
                self.content,  # Message
                settings.DEFAULT_FROM_EMAIL,  # From email (must be configured in settings.py)
                [recipient_email],  # To email
                fail_silently=False,  # Raise an exception if the email fails to send
            )
            return True
        except ObjectDoesNotExist:
            # Handle the case where the user doesn't have a profile
            print(f"No profile found for user: {self.user.username}")
            return False
        except Exception as e:
            # Handle other potential errors (e.g., email sending failure)
            print(f"Error sending email: {e}")
            return False
