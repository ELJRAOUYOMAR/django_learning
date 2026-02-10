#!/usr/bin/env python3
"""  """
from django import forms 
from .models import Post


class PostForm(forms.ModelForm):
    """ form for creating and editing blog posts """
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter post title"
            }), 
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 10,
                'placeholder': 'Write your post content here...'
            }), 
            'category': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Category (optional)'
            }),
            'status':forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Post title', 
            'content': 'Content', 
            'category': 'Category', 
            'status': 'Status'
        }
    
    def clean_title(self):
        """ validate that title isn't empty and has minimum length """
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('title must be at least 5 characteres long')
        return title

    def clean_content(self):
        """ validate that content is not empty """
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError('content must be at least 50 characteres long')
        return content   

    



