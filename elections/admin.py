from django.contrib import admin
from .models import Election, Candidate, Vote


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'start_date',
        'end_date',
        'is_active',
        'total_votes',
    )
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title',)
    ordering = ('-start_date',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'party',
        'user',
        'created_at',
    )
    search_fields = ('full_name', 'party', 'user__username')
    list_filter = ('party',)
    ordering = ('full_name',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'voter',
        'candidate',
        'election',
        'voted_at',
        'ip_address',
    )
    list_filter = ('election', 'candidate')
    search_fields = ('voter__username', 'candidate__full_name')
    ordering = ('-voted_at',)

    readonly_fields = (
        'voter',
        'candidate',
        'election',
        'voted_at',
        'ip_address',
    )

    def has_add_permission(self, request):
        # 禁止管理员手动添加投票
        return False
