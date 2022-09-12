from django import forms

class RegistroForm(forms.Form):
    nombre_user = forms.CharField(label="registerFirstName", required=False)
    apellido_user = forms.CharField(label="registerLastName", required=False)  
    username_user = forms.CharField(label="registerUsername", required=False)
    email = forms.CharField(label="email", required=False)
    password = forms.CharField(label="password", required=False)