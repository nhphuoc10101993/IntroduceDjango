from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from models import Document,FileStorage
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email'
        }
    def save(self,commit=True):
        frm_user = super(RegisterForm,self).save(commit=False)
        frm_user.username = self.cleaned_data['username']
        frm_user.email = self.cleaned_data['email']
        frm_user.first_name = self.cleaned_data['first_name']
        frm_user.last_name = self.cleaned_data['last_name']
        if commit:
            frm_user.save()
        return frm_user
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = {
            'description',
            'doc',
        }
class FileStorageForm(forms.ModelForm):
    class Meta:
        model = FileStorage
        fields = {
            'description',
            'filename',
            'images',
        }