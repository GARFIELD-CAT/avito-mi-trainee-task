from django.contrib import admin

from .models import Choice, Poll, Vote


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll_id', 'text')


class PollAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'creator', 'pub_date', 'active'
    )


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'voter', 'poll_id', 'choice_id')


admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)
