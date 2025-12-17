from django.contrib import admin
from .models import Candidate, Election, Vote

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'party', 'created_at']
    search_fields = ['full_name', 'party']
    list_filter = ['created_at', 'party']

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    date_hierarchy = 'start_date'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'election', 'voted_at']
    list_filter = ['election', 'voted_at']
    readonly_fields = ['voted_at']
    date_hierarchy = 'voted_at'