from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = (
            'password1',
            'password2',
        )
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta(UserCreationForm):
        model = User
        fields = (
            'email',
            'name',
            'password1',
            'password2',
        )
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class SigninForm(forms.ModelForm):
    class Meta:
        fields = (
            'email',
            'password',
        )
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

# class SigninForm(forms.Form):
#     email = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user = None
#
#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data['email']
#         password = cleaned_data['password']
#         self.user = authenticate(
#             email=email,
#             password=password,
#         )
#         if not self.user:
#             raise forms.ValidationError('Login Failed!')
#         else:
#             setattr(self, 'signin', self._signin)
#
#     def _signin(self, request):
#         if self.user:
#             login(request.self.user)
