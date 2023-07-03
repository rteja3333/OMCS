from django import forms
from .models import doctor , patient
from .models import hospital
from django.forms import TextInput
# class HospitalForm(forms.ModelForm):
#     class Meta:
#         model = hospital
#         fields = ('name', 'address', 'email', 'phone_number', 'pincode', 'description') 
class HospitalForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, error_messages={'required':'' }, widget=TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=200, error_messages={'required':'' }, widget=TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone', max_length=20, error_messages={'required':'' }, widget=TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', max_length=100, error_messages={'required':'' }, widget=TextInput(attrs={'class': 'form-control'}))
    pincode = forms.CharField(label='Pincode', max_length=200, error_messages={'required':'' }, widget=TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', max_length=200, error_messages={'required':'' }, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = hospital
        fields = ('name', 'address', 'email', 'phone_number', 'pincode', 'description')


class DoctorForm(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['name', 'age', 'phone_number', 'email', 'address', 'experience'] 

class PatientForm(forms.ModelForm):
    class Meta:
        model = patient
        fields = ['name', 'age', 'phone_number', 'email', 'address', 'description'] 


    # pincode_regex = RegexValidator(regex=r'[0-9]{6}$', message="Enter a valid Indian pincode.")
    # pincode = models.CharField(max_length=6, validators=[pincode_regex])