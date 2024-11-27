from django import forms

from .models import Account

class RagistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password '
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password '
    }))
    class Meta:
        model = Account
        fields =['first_name','last_name','phone_number','email','password']


    def __init__(self,*args,**kwargs):
        super(RagistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your First Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your First Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your First Name'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RagistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        #check for matching password is equal to confirm password or not 
        if password != confirm_password:
            raise forms.ValidationError('Password does not match!')
        
        

