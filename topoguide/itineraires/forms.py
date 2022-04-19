from django import forms

class authForm(forms.form):
  template_name= 'login.html'
  username = forms.CharField(label="Username")
  password = forms.PasswordInput(label="Password")
  date = forms.DateField(label='date')