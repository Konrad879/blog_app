from django import forms
from .models import BlogPost, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class BlogPostForm(forms.ModelForm):
    body = forms.CharField(
        required=True, 
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Enter your Blog Post",
                "class": "form-control"
            }
            ), 
            label="",

        )
    image = forms.ImageField(required=False)
    
    class Meta:
        model = BlogPost
        exclude = ("user", "likes")


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
            

class UserUpdateForm(forms.ModelForm):
    username   = forms.CharField(required=False, widget=forms.TextInput(attrs={
                      'class':'form-control','placeholder':'Username'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
                      'class':'form-control','placeholder':'First Name'}))
    last_name  = forms.CharField(required=False, widget=forms.TextInput(attrs={
                      'class':'form-control','placeholder':'Last Name'}))
    email      = forms.EmailField(required=False, widget=forms.TextInput(attrs={
                      'class':'form-control','placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def clean_username(self):
        new_username = self.cleaned_data.get('username')
        if not self.instance:
            return new_username
        if new_username == self.instance.username:
            return new_username
        # Inaczej sprawdź, czy już istnieje
        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError("User with that username already exists")
        return new_username


class ProfileUpdateForm(forms.ModelForm):
    profile_image   = forms.ImageField(required=False)
    profile_bio     = forms.CharField(required=False, widget=forms.Textarea(
                        attrs={'class':'form-control','placeholder':'Bio','rows':3}))
    homepage_link   = forms.URLField(assume_scheme="https", required=False, widget=forms.URLInput(
                        attrs={'class':'form-control','placeholder':'Homepage URL'}))
    facebook_link   = forms.URLField(assume_scheme="https", required=False, widget=forms.URLInput(
                        attrs={'class':'form-control','placeholder':'Facebook URL'}))
    instagram_link  = forms.URLField(assume_scheme="https", required=False, widget=forms.URLInput(
                        attrs={'class':'form-control','placeholder':'Instagram URL'}))
    linkedin_link   = forms.URLField(assume_scheme="https", required=False, widget=forms.URLInput(
                        attrs={'class':'form-control','placeholder':'LinkedIn URL'}))

    class Meta:
        model = Profile
        fields = ['profile_image','profile_bio',
                  'homepage_link','facebook_link',
                  'instagram_link','linkedin_link']