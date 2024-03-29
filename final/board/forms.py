from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget

class PostWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control form-title-input',
            'autofocus': True,
        })

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
