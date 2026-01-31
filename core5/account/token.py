from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type  # it provides utitlity functions for smoothing over the
                           # differences between python 2 and python 3

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    
    # we can setup the password reset token in settings.py, by default it is 7 days
    
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
            )

account_activation_token = AccountActivationTokenGenerator()