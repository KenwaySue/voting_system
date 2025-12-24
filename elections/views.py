from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  # 注册表单
from django.contrib.auth import login                  # 登录函数
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from .models import Election, Candidate, Vote

def home(request):
    """
    视图原型：首页
    描述：展示欢迎信息、最新的选举概况及候选人总数。
    路由：GET /
    """
    elections = Election.objects.all().order_by('-start_date')
    
    # 计算首页所需的变量，防止模板报错
    current_election = elections.filter(is_active=True).first()
    candidates_count = Candidate.objects.count()
    
    return render(request, 'home.html', {
        'elections': elections,
        'current_election': current_election,
        'candidates_count': candidates_count
    })

def election_list(request):
    """
    视图原型：选举列表 (核心投票页)
    描述：显示所有选举。如果没有活跃选举，默认显示最新的一个。
          计算每个候选人在当前选举中的票数和百分比。
          检查当前用户的投票状态。
    路由：GET /elections/
    """
    elections = Election.objects.all().order_by('-start_date')
    
    # 获取当前正在进行的选举
    current_election = elections.filter(is_active=True).first()
    if not current_election:
        current_election = elections.first()
        
    # 查询所有候选人
    candidates = Candidate.objects.all()
    
    total_votes = 0
    has_voted = False
    vote_timestamp = None
    
    if current_election:
        # 计算当前选举的总票数
        total_votes = Vote.objects.filter(election=current_election).count()
        
        # 检查当前用户是否已投票
        if request.user.is_authenticated:
            user_vote = Vote.objects.filter(
                voter=request.user, 
                election=current_election
            ).first()
            if user_vote:
                has_voted = True
                vote_timestamp = user_vote.voted_at

    # 为每个候选人添加统计属性
    for candidate in candidates:
        # 只统计在当前选举中的票数
        candidate.vote_count = Vote.objects.filter(candidate=candidate, election=current_election).count()
        if total_votes > 0:
            candidate.percentage = (candidate.vote_count / total_votes) * 100
        else:
            candidate.percentage = 0

    return render(request, 'elections/index.html', {
        'elections': elections,
        'current_election': current_election,
        'candidates': candidates,
        'total_votes': total_votes,
        'has_voted': has_voted,
        'vote_timestamp': vote_timestamp,
        'remaining_time': '计算中...' 
    })

def election_detail(request, election_id):
    """
    视图原型：选举详情
    描述：查看单个选举的详细信息。
    路由：GET /elections/<id>/
    """
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.all()

    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(
            voter=request.user,
            election=election
        ).first()

    return render(request, 'elections/election_detail.html', {
        'election': election,
        'candidates': candidates,
        'user_vote': user_vote,
    })

@login_required
def vote(request, election_id, candidate_id):
    """
    视图原型：处理投票
    描述：接收 POST 请求。
          1. 验证选举是否活跃。
          2. 验证用户是否已投过票。
          3. 创建 Vote 记录。
          4. 支持响应 AJAX (返回 JSON) 或普通表单提交 (重定向)。
    路由：POST /elections/<id>/vote/<cand_id>/
    """
    election = get_object_or_404(Election, id=election_id)
    candidate = get_object_or_404(Candidate, id=candidate_id)

    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method")

    # 检查选举是否开放
    if not election.is_active:
         messages.error(request, "该选举未开始或已结束。")
         return redirect('elections:election_detail', election_id=election.id)

    # 检查是否已投票
    if Vote.objects.filter(voter=request.user, election=election).exists():
        # 如果是 AJAX 请求，返回 JSON 错误
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': '您已经投过票了'})
        messages.warning(request, "You have already voted in this election.")
        return redirect('elections:election_detail', election_id=election.id)

    # 创建投票
    Vote.objects.create(
        voter=request.user,
        candidate=candidate,
        election=election,
        ip_address=get_client_ip(request),
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # 如果是 AJAX 请求，返回 JSON 成功
        return JsonResponse({'success': True, 'message': '投票成功'})
    else:
        # 如果是普通表单提交，跳转页面
        messages.success(request, "Your vote has been recorded successfully.")
        return redirect('elections:election_detail', election_id=election.id)

def get_client_ip(request):
    """
    辅助函数：获取用户 IP 地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def election_results(request, election_id):
    """
    视图原型：单个选举结果
    描述：按票数降序显示特定选举的结果。
    路由：GET /elections/<id>/results/
    """
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.all()
    
    # 计算每个候选人的票数
    results = []
    for candidate in candidates:
        vote_count = Vote.objects.filter(candidate=candidate, election=election).count()
        
        if vote_count > 0:
            results.append({
                'candidate': candidate,
                'vote_count': vote_count
            })
    
    # 按票数排序
    results.sort(key=lambda x: x['vote_count'], reverse=True)
    
    total_votes = sum(r['vote_count'] for r in results)
    
    return render(request, 'elections/election_results.html', {
        'election': election,
        'results': results,
        'total_votes': total_votes
    })

def results(request):
    """
    视图原型：所有结果汇总
    描述：遍历所有选举，计算并显示其结果统计。
    路由：GET /elections/results/
    """
    elections = Election.objects.all().order_by('-start_date')
    results_data = []
    
    for election in elections:
        candidates = Candidate.objects.all()
        total_votes = Vote.objects.filter(election=election).count()
        
        election_results = []
        for candidate in candidates:
            vote_count = Vote.objects.filter(
                candidate=candidate,
                election=election
            ).count()
            
            percentage = 0
            if total_votes > 0:
                percentage = (vote_count / total_votes) * 100
            
            election_results.append({
                'candidate': candidate,
                'vote_count': vote_count,
                'percentage': percentage
            })
        
        # 按票数排序
        election_results.sort(key=lambda x: x['vote_count'], reverse=True)
        
        results_data.append({
            'election': election,
            'results': election_results,
            'total_votes': total_votes
        })
    
    return render(request, 'elections/results.html', {
        'results_data': results_data
    })

def api_results(request):
    """
    视图原型：AJAX API
    描述：返回当前活跃选举的 JSON 数据，用于前端动态更新图表。
    路由：GET /elections/api/results/
    """
    current_election = Election.objects.filter(is_active=True).first()
    if not current_election:
        current_election = Election.objects.first()
    
    if not current_election:
        return JsonResponse({
            'success': False,
            'message': '没有找到选举'
        })
    
    # 获取该选举的投票结果
    candidates = Candidate.objects.all()
    total_votes = Vote.objects.filter(election=current_election).count()
    
    results = []
    for candidate in candidates:
        vote_count = Vote.objects.filter(
            candidate=candidate, 
            election=current_election
        ).count()
        
        percentage = 0
        if total_votes > 0:
            percentage = (vote_count / total_votes) * 100
        
        results.append({
            'id': candidate.id,
            'full_name': candidate.full_name,
            'votes': vote_count,
            'percentage': percentage
        })
    
    return JsonResponse({
        'success': True,
        'results': results,
        'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    })

def register(request):
    """
    视图原型：用户注册
    描述：使用 Django 内置 UserCreationForm 处理新用户注册。
          注册成功后自动登录并跳转到选举列表。
    路由：GET/POST /register/
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 注册成功后自动登录用户
            login(request, user)
            # 跳转到选举列表页
            return redirect('elections:election_list') 
    else:
        form = UserCreationForm()
    
    return render(request, 'elections/register.html', {'form': form})
