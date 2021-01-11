from django import forms
from . import models

class LoginForm(forms.Form):
    
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")

    # def clean_password(self):
    #     email = self.clead_data.get('email')
    #     password = self.cleaned_data('password')
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password) :
    #             return password
    #         else:
    #             raise forms.ValidationError("비밀번호가 틀렸습니다")
    #     except models.User.DoesNotExist:
    #         pass
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password) :
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀렸습니다"))
        except models.User.DoesNotExist:
            self.add_error("email", selforms.ValidationError("사용자가 존재하지 않습니다"))


# class SignUpForm(forms.Form):
    
#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)

#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Confirmed Password")

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("중복된 아이디입니다")
#         except models.User.DoesNotExist:
#             return email
    
#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")
#         if password != password1:
#             raise forms.ValidationError("비밀번호가 일치하지 않습니다")
#         else:
#             return password

#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")

#         user = models.User.objects.create_user(email, email, password)

#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()

class SignUpForm(forms.ModelForm):
	
    class Meta:
        model=models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget = forms.PasswordInput)
    password1 = forms.CharField(widget = forms.PasswordInput, label="Confirmed Password")
	
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            return password
    
    def save(self, *args, **kwargs):
	    user = super().save(commit=False)
	    email = self.cleaned_data.get("email")
	    password = self.cleaned_data.get("password")
	
	    user.username = email
	    user.set_password(password)
	    user.save()
