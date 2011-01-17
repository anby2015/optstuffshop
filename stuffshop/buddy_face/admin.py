__author__ = 'denis'

class ChineeseBuddyAdmin(admin.ModelAdmin):
    list_display = ('name','position','quote','image')

admin.site.register(ChineeseBuddy, ChineeseBuddyAdmin)