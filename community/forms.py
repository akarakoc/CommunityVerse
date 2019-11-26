from django.contrib.auth import authenticate, get_user_model
from django import forms

class UsersLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput,)

	def __init__(self, *args, **kwargs):
		super(UsersLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"username"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"password"})

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("This user does not exists")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("User is no longer active")

		return super(UsersLoginForm, self).clean(*args, **keyargs)
 

User = get_user_model()

class UsersRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"confirm_email", 
			"password",
		]
	username = forms.CharField()
	email = forms.EmailField(label = "Email")
	confirm_email = forms.EmailField(label = "Confirm Email")
	password = forms.CharField(widget = forms.PasswordInput)


	def __init__(self, *args, **kwargs):
		super(UsersRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"username"})
		self.fields['email'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"email"})
		self.fields['confirm_email'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"confirm_email"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"password"})


	def clean(self, *args, **keyargs):
		email = self.cleaned_data.get("email")
		confirm_email = self.cleaned_data.get("confirm_email")
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if email != confirm_email:
			raise forms.ValidationError("Email must match")
		
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Email is already registered")

		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("User with this username already registered")
		
		#you can add more validations for password

		if len(password) < 8:	
			raise forms.ValidationError("Password must be greater than 8 characters")
		return super(UsersRegisterForm, self).clean(*args, **keyargs)
 


class AddCommunity(forms.Form):
	Community_Name = forms.CharField()
	Community_Description = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}))
	Community_Tags = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}))
	Community_Image = forms.ImageField()
	Private_Community = forms.BooleanField(initial=False, required=False)
	
	
	def __init__(self, *args, **kwargs):
		super(AddCommunity, self).__init__(*args, **kwargs)
		self.fields['Community_Name'].label = "Community Name"
		self.fields['Community_Name'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Community Name"})
		self.fields['Community_Description'].label = "Community Description"
		self.fields['Community_Description'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Community Description"})
		self.fields['Community_Tags'].label = "Community Tags"
		self.fields['Community_Tags'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Community Tags"})

	def clean(self, *args, **keyargs):
		Community_Name = self.cleaned_data.get("Community Name")
		Community_Description = self.cleaned_data.get("Community Description")
		Community_Tags = self.cleaned_data.get("Community Tags")
		Community_Image = self.cleaned_data.get("Community Image")
		return super(AddCommunity, self).clean(*args, **keyargs) 
		

class AddDatatype(forms.Form):
	Datatype_Name = forms.CharField()
	Datatype_Tags = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}))
	Datatype_Image = forms.ImageField()
	def __init__(self, *args, **kwargs):
		super(AddDatatype, self).__init__(*args, **kwargs)
		self.fields['Datatype_Name'].label = "Datatype Name"
		self.fields['Datatype_Name'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Datatype Name"})
		self.fields['Datatype_Tags'].label = "Datatype Tags"
		self.fields['Datatype_Tags'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Datatype Tags"})
	def clean(self, *args, **keyargs):
		Datatype_Name = self.cleaned_data.get("Datatype Name")
		Datatype_Tags = self.cleaned_data.get("Datatype Tags")
		Datatype_Image = self.cleaned_data.get("Datatype Image")
		return super(AddDatatype, self).clean(*args, **keyargs)