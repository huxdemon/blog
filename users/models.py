from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class VerifyCode(models.Model):
    CHOICE = [
        (0, '密码找回'),
        (1, '转账'),
        (2, '登录验证'),
    ]
    user = models.ForeignKey(User)
    code = models.CharField('验证码', max_length=10)
    type = models.IntegerField('类型', choices=CHOICE, default=0)
    is_valid = models.BooleanField('是否有效', default=1)
    active_time = models.DateTimeField('有效期', default=timezone.now)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-id']

