from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, verbose_name="姓名")
    photo = models.ImageField(upload_to='candidates/', blank=True, null=True, verbose_name="照片")
    bio = models.TextField(verbose_name="个人简介")
    program = models.TextField(verbose_name="竞选纲领")
    party = models.CharField(max_length=100, blank=True, verbose_name="政党")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    # 添加新字段
    color = models.CharField(max_length=7, default='#1e3a8a', verbose_name="代表颜色")
    light_color = models.CharField(max_length=7, blank=True, verbose_name="浅色")

    class Meta:
        verbose_name = "候选人"
        verbose_name_plural = "候选人"

    def __str__(self):
        return self.full_name
    
    def get_vote_percentage(self, election_id=None):
        """获取候选人得票率"""
        if election_id:
            votes = Vote.objects.filter(candidate=self, election_id=election_id).count()
        else:
            votes = Vote.objects.filter(candidate=self).count()
        
        total_votes = Vote.objects.filter(election_id=election_id).count() if election_id else Vote.objects.count()
        
        if total_votes == 0:
            return 0
        return round((votes / total_votes) * 100, 1)

class Election(models.Model):
    title = models.CharField(max_length=200, verbose_name="选举标题")
    description = models.TextField(verbose_name="选举描述")
    start_date = models.DateTimeField(verbose_name="开始时间")
    end_date = models.DateTimeField(verbose_name="结束时间")
    is_active = models.BooleanField(default=False, verbose_name="是否活跃")

    class Meta:
        verbose_name = "选举"
        verbose_name_plural = "选举"

    def __str__(self):
        return self.title
    
    @property
    def total_votes(self):
        """获取总票数"""
        return Vote.objects.filter(election=self).count()

class Vote(models.Model):
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
        return f"{self.voter.username} 投票给 {self.candidate.full_name}"