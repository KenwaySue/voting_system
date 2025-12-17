from django.core.management.base import BaseCommand
from elections.models import Candidate, Election, Vote
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = '创建示例选举数据'
    
    def handle(self, *args, **kwargs):
        # 创建选举
        election, created = Election.objects.get_or_create(
            title="2023年总统选举",
            defaults={
                'description': '2023年全国总统大选',
                'start_date': timezone.now() - timedelta(days=1),
                'end_date': timezone.now() + timedelta(days=30),
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('创建选举成功'))
        else:
            self.stdout.write(self.style.SUCCESS('选举已存在'))
        
        # 创建候选人
        candidates_data = [
            {
                'username': 'liminghua',
                'full_name': '李明华',
                'party': '民主党',
                'bio': '前副总统，任职期间专注于经济改革和医疗保障体系完善。主张增加教育投资、推动绿色能源发展和加强国际合作。拥有8年从政经验。',
                'color': '#1e3a8a'
            },
            {
                'username': 'wangjianguo',
                'full_name': '王建国',
                'party': '共和党',
                'bio': '知名企业家，曾任州长。主张降低企业税、减少政府干预、加强国防建设和限制移民政策。承诺创造更多就业机会。拥有6年从政经验。',
                'color': '#dc2626'
            },
            {
                'username': 'chensiying',
                'full_name': '陈思颖',
                'party': '独立候选人',
                'bio': '著名社会活动家，政治改革倡导者。主张政治透明化、消除贫富差距、加强科技伦理监管和推动全面教育改革。拥有12年社会活动经验。',
                'color': '#6b7280'
            }
        ]
        
        for data in candidates_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': f"{data['username']}@example.com",
                    'first_name': data['full_name'],
                    'is_staff': True
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
            
            candidate, created = Candidate.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': data['full_name'],
                    'party': data['party'],
                    'bio': data['bio'],
                    'color': data['color'],
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"创建候选人 {data['full_name']} 成功"))
            else:
                self.stdout.write(self.style.SUCCESS(f"候选人 {data['full_name']} 已存在"))
        
        self.stdout.write(self.style.SUCCESS('示例数据创建完成'))