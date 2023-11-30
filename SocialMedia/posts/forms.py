from django import forms
from .models import Post, Comment,Image
from django.db import models
# Tạo 1 bài viết mới
class PostModelForm(forms.ModelForm):
    # image = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': False}))

    class Meta:
        model = Post
        fields = ('content','visibility',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'content-post','placeholder':'Bạn đang nghĩ gì?'}),
            'visibility': forms.Select(attrs={'class': 'visibility'}),
        }
    


        
        
        
class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'placeholder':'Bình luận bài viết','class':'input-comment'})) 
    class Meta:
        model = Comment
        fields = ('body',)

# Sửa bài viết
class EditPostModelForm(forms.ModelForm):
    

    class Meta:
        model = Post
        fields = ('content', 'visibility',)
class EditCmtModelForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('body',)