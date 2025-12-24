from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Election(models.Model):
    """
    Голосование / Election
    """
    title = models.CharField(max_length=200, verbose_name="选举标题")
    description = models.TextField(verbose_name="选举描述")
    start_date = models.DateTimeField(verbose_name="开始时间")
    end_date = models.DateTimeField(verbose_name="结束时间")
    is_active = models.BooleanField(default=False, verbose_name="是否进行中")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "选举"
        verbose_name_plural = "选举"

    def __str__(self):
        return self.title

    @property
    def total_votes(self):
        return Vote.objects.filter(election=self).count()

    def is_open(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date


class Candidate(models.Model):
    """
    Кандидат / Candidate
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    full_name = models.CharField(max_length=200, verbose_name="姓名")
    photo = models.ImageField(upload_to='candidates/', blank=True, null=True, verbose_name="照片")
    bio = models.TextField(verbose_name="个人简介")
    program = models.TextField(verbose_name="竞选纲领")
    party = models.CharField(max_length=100, blank=True, verbose_name="政党")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    color = models.CharField(max_length=7, default='#1e3a8a', verbose_name="代表颜色")
    light_color = models.CharField(max_length=7, blank=True, verbose_name="浅色")

    class Meta:
        verbose_name = "候选人"
        verbose_name_plural = "候选人"

    def __str__(self):
        return self.full_name

    def get_votes_count(self, election=None):
        qs = Vote.objects.filter(candidate=self)
        if election:
            qs = qs.filter(election=election)
        return qs.count()

    def get_vote_percentage(self, election):
        total = Vote.objects.filter(election=election).count()
        if total == 0:
            return 0
        return round((self.get_votes_count(election) / total) * 100, 2)


class Vote(models.Model):
    """
    Голос / Vote
    """
    voter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="投票人")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="候选人")
    election = models.ForeignKey(Election, on_delete=models.CASCADE, verbose_name="选举")
    voted_at = models.DateTimeField(auto_now_add=True, verbose_name="投票时间")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP地址")

    class Meta:
        unique_together = ['voter', 'election']
        verbose_name = "投票"
        verbose_name_plural = "投票记录"

    def __str__(self):
        return f"{self.voter.username} -> {self.candidate.full_name} ({self.election.title})"
