from django import forms
from .models import ImageUploadModel


class SimpleUploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.ImageField()


class ImageUploadForm(forms.ModelForm):
    
    class Meta:
        model = ImageUploadModel
        fields = ('description', 'document',)
        # 자동입력되는 시간 부분은 form에 넣지 않는다.
        