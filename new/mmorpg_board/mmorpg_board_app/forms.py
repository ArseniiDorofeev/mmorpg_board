from ckeditor.fields import RichTextField
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Advertisement
from .models import Response
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class AdvertisementForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor', 'cols': 80, 'rows': 20}))
    video1 = forms.URLField(required=False, label="Video 1")
    video2 = forms.URLField(required=False, label="Video 2")

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'image1', 'image2', 'video1', 'video2', ]
        widgets = {'content': RichTextField()}

    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']


class SubscribeForm(forms.Form):
    subscribe = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'subscribe-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'subscribe',
            Submit('submit', 'Update Subscription')
        )
