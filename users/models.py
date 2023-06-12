from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        """
        요청 받은 사용자 이메일, 사용자 닉네임, 비밀번호로 사용자를 생성하여 저장합니다.
        """
        if not email:
            raise ValueError("사용자 이메일은 필수입력 사항입니다.")

        if not nickname:
            raise ValueError("사용자 닉네임은 필수입력 사항입니다.")

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        """
        요청받은 사용자 이메일, 사용자 닉네임, 비밀번호로 수퍼유저를 생성하여 저장합니다.
        """
        user = self.create_user(
            email=email,
            nickname=nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="사용자 이메일",
        max_length=255,
        unique=True,
    )

    nickname = models.CharField(max_length=100, unique=True, verbose_name="사용자 닉네임")
    password = models.CharField(max_length=255, verbose_name="비밀번호")

    GENDER_CHOICES = [
        ("남성", "남성"),
        ("여성", "여성"),
        ("밝히고 싶지 않음", "밝히고 싶지 않음"),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=False,
        error_messages="필수 입력 값입니다.",
        verbose_name="성별",
    )
    age = models.PositiveIntegerField(null=True, verbose_name="사용자 나이")
    bio = models.TextField(blank=True, null=True, verbose_name="사용자 자기소개")
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True, verbose_name="사용자 프로필이미지"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="사용자 계정 생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="사용자 정보 마지막 수정일")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"  # 이걸로 로그인 하겠다 하는 필드. 들어가는 값은 unique=True 속성.
    REQUIRED_FIELDS = ["nickname"]  # createsuperuser할때 어떤 필드들을 작성받을 지 적는 필드.

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
