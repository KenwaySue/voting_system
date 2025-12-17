from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Candidate, Election, Vote

def home(request):
    """投票系统首页"""
    current_election = Election.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()
    
    # 获取候选人数据并计算统计
    candidates = Candidate.objects.all()
    total_votes = 0
    
    if current_election:
        total_votes = Vote.objects.filter(election=current_election).count()
    
    candidate_data = []
    for candidate in candidates:
        vote_count = 0
        if current_election:
            vote_count = Vote.objects.filter(candidate=candidate, election=current_election).count()
        
        # 计算百分比
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        
        # 为候选人分配颜色
        colors = ['#1e3a8a', '#dc2626', '#6b7280', '#10b981', '#8b5cf6']
        candidate_color = colors[candidate.id % len(colors)] if candidate.id else colors[0]
        
        candidate_data.append({
            'id': candidate.id,
            'full_name': candidate.full_name,
            'party': candidate.party,
            'bio': candidate.bio,
            'photo': candidate.photo,
            'color': candidate_color,
            'vote_count': vote_count,
            'percentage': round(percentage, 1)
        })
    
    # 计算剩余时间
    remaining_time = "未开始"
    if current_election:
        remaining = current_election.end_date - timezone.now()
        if remaining.total_seconds() > 0:
            days = remaining.days
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            remaining_time = f"{days}天 {hours}小时 {minutes}分钟"
        else:
            remaining_time = "已结束"
    
    # 检查用户是否已投票
    has_voted = False
    vote_timestamp = None
    if request.user.is_authenticated and current_election:
        try:
            vote = Vote.objects.get(voter=request.user, election=current_election)
            has_voted = True
            vote_timestamp = vote.voted_at.strftime("%Y-%m-%d %H:%M")
        except Vote.DoesNotExist:
            has_voted = False
    
    context = {
        'current_election': current_election,
        'candidates': candidate_data,
        'total_votes': total_votes,
        'remaining_time': remaining_time,
        'has_voted': has_voted,
        'vote_timestamp': vote_timestamp,
    }
    return render(request, 'elections/index.html', context)

def candidate_list(request):
    """所有候选人列表"""
    candidates = Candidate.objects.all()
    return render(request, 'elections/candidate_list.html', {'candidates': candidates})

def candidate_detail(request, candidate_id):
    """候选人详细信息"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    return render(request, 'elections/candidate_detail.html', {'candidate': candidate})

@login_required
@csrf_exempt
def vote(request):
    """处理投票请求"""
    if request.method == 'POST':
        try:
            candidate_id = request.POST.get('candidate_id')
            current_election = Election.objects.filter(
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now(),
                is_active=True
            ).first()
            
            if not current_election:
                return JsonResponse({
                    'success': False,
                    'message': '当前没有活跃的选举。'
                })
            
            # 检查用户是否已经投过票
            if Vote.objects.filter(voter=request.user, election=current_election).exists():
                return JsonResponse({
                    'success': False,
                    'message': '您已经在此次选举中投过票了。'
                })
            
            candidate = get_object_or_404(Candidate, id=candidate_id)
            
            # 记录投票
            Vote.objects.create(
                voter=request.user,
                candidate=candidate,
                election=current_election,
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, '您的投票已成功提交！')
            return JsonResponse({
                'success': True,
                'message': '投票成功！'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'投票失败：{str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': '无效的请求方法。'
    })

def results(request):
    """显示投票结果页面"""
    current_election = Election.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()
    
    candidates = Candidate.objects.all()
    total_votes = 0
    results_data = []
    
    if current_election:
        total_votes = Vote.objects.filter(election=current_election).count()
        votes = Vote.objects.filter(election=current_election)
        
        for candidate in candidates:
            vote_count = votes.filter(candidate=candidate).count()
            percentage = round((vote_count / total_votes * 100), 1) if total_votes > 0 else 0
            
            # 为候选人分配颜色
            colors = ['#1e3a8a', '#dc2626', '#6b7280', '#10b981', '#8b5cf6']
            candidate_color = colors[candidate.id % len(colors)] if candidate.id else colors[0]
            
            results_data.append({
                'id': candidate.id,
                'name': candidate.full_name,
                'party': candidate.party,
                'votes': vote_count,
                'percentage': percentage,
                'color': candidate_color
            })
        
        # 按票数排序
        results_data.sort(key=lambda x: x['votes'], reverse=True)
    
    # 选民统计
    from django.contrib.auth.models import User
    total_voters = User.objects.count()
    voted_count = total_votes
    turnout_rate = round((voted_count / total_voters * 100), 1) if total_voters > 0 else 0
    
    context = {
        'current_election': current_election,
        'results': results_data,
        'total_votes': total_votes,
        'voter_count': total_voters,
        'voted_count': voted_count,
        'turnout_rate': turnout_rate,
        'election_active': current_election.is_active if current_election else False,
    }
    return render(request, 'elections/results.html', context)

def api_results(request):
    """API接口：获取实时投票结果"""
    current_election = Election.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()
    
    candidates = Candidate.objects.all()
    total_votes = 0
    results_data = []
    
    if current_election:
        total_votes = Vote.objects.filter(election=current_election).count()
        votes = Vote.objects.filter(election=current_election)
        
        for candidate in candidates:
            vote_count = votes.filter(candidate=candidate).count()
            percentage = round((vote_count / total_votes * 100), 1) if total_votes > 0 else 0
            
            colors = ['#1e3a8a', '#dc2626', '#6b7280', '#10b981', '#8b5cf6']
            candidate_color = colors[candidate.id % len(colors)] if candidate.id else colors[0]
            
            results_data.append({
                'id': candidate.id,
                'name': candidate.full_name,
                'votes': vote_count,
                'percentage': percentage,
                'color': candidate_color
            })
    
    return JsonResponse({
        'success': True,
        'results': results_data,
        'total_votes': total_votes,
        'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# 添加缺失的视图函数
def custom_login(request):
    """自定义登录页面"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"欢迎回来, {username}!")
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'elections/login.html', {'form': form})

def register(request):
    """注册页面"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功！")
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'elections/register.html', {'form': form})

def custom_logout(request):
    """退出系统"""
    logout(request)
    messages.info(request, "您已成功退出系统。")
    return redirect('home')

def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# 可选：添加管理后台视图
@login_required
def admin_dashboard(request):
    """管理后台页面"""
    if not request.user.is_staff:
        messages.error(request, "您没有权限访问管理后台。")
        return redirect('home')
    
    current_election = Election.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()
    
    # 获取统计信息
    from django.contrib.auth.models import User
    total_voters = User.objects.count()
    total_votes = Vote.objects.count() if current_election else 0
    
    # 模拟时间线数据
    vote_timeline = [
        {'time': '08:00', 'votes': 120},
        {'time': '10:00', 'votes': 450},
        {'time': '12:00', 'votes': 780},
        {'time': '14:00', 'votes': 920},
        {'time': '16:00', 'votes': 1100},
        {'time': '18:00', 'votes': 1250},
        {'time': '20:00', 'votes': 1420}
    ]
    
    context = {
        'page_title': '选举管理后台',
        'election': current_election,
        'total_voters': total_voters,
        'total_votes': total_votes,
        'vote_timeline': vote_timeline
    }
    
    return render(request, 'elections/admin.html', context)