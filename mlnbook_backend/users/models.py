from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mlnbook_backend.utils.global_choices import LANGUAGE_CODE_CHOICES, PHASE_LEVEL


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


class Author(models.Model):
    # B端作者和C段用户需要区分出来
    name = models.CharField("姓名", max_length=100)
    phone = models.CharField("联系方式", max_length=16, blank=True)
    email = models.CharField("email", max_length=50, blank=True)
    id_card = models.CharField("身份信息", max_length=20, blank=True)
    description = models.TextField("介绍信息", blank=True)
    language = models.CharField("母语", max_length=16, default='zh_CN', choices=LANGUAGE_CODE_CHOICES)
    c_type = models.CharField("作者类型", max_length=16, default="staff",
                              help_text="certification 入驻认证，staff 平台内部组员，public 历史公开公共资源")
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_user_authors"

    def __str__(self):
        return self.name


class Profile(models.Model):
    # 与User外键连接
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 个人信息附加字段
    nick_name = models.CharField("别名", max_length=50, blank=True)
    native_language = models.CharField("母语", max_length=16, default='zh_CN', choices=LANGUAGE_CODE_CHOICES)
    learn_language = models.CharField("学习语言", max_length=16, default='en_US', choices=LANGUAGE_CODE_CHOICES)
    phase = models.CharField("学段", max_length=20, choices=PHASE_LEVEL, default="preschool")
    child_gender = models.CharField("孩子性别", max_length=16, default="M", help_text="M male, F female, U Unknown")
    child_age = models.IntegerField("孩子年龄", default=2)
    valid_author = models.BooleanField("认证作者", default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, help_text="平台作者认证，生成author对象关联")
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_user_profile"

    def __str__(self):
        return self.nick_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 同步更新
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
