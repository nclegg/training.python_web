from django.contrib import admin
from myblog.models import Post
from myblog.models import Category


class MembershipInline(admin.TabularInline):
    model = Category.posts.through

class PostAdmin(admin.ModelAdmin):
    inlines = [MembershipInline,] 

class CategoryAdmin(admin.ModelAdmin):
    #inlines = [MembershipInline,]
    exclude = ("posts",)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
