from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mlnbook_backend.utils.global_choices import LANGUAGE_CODE_CHOICES


class User(AbstractUser):
    """
    Default custom user model for mlnbook_backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Profile(models.Model):
    # 与User外键连接
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 个人信息附加字段
    nick_name = models.CharField("别名", max_length=50, blank=True)
    native_language = models.CharField("母语", max_length=16, default='zh_CN', choices=LANGUAGE_CODE_CHOICES)
    learn_language = models.IntegerField("学习语言", max_length=16, default='en_US', choices=LANGUAGE_CODE_CHOICES)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_user_profile"

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 同步更新
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
