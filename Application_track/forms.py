from django.forms import ModelForm
from .models import JobAdvert,JobApplication
from django import forms

class JobAdvertForms(ModelForm):
    class Meta:
        model=JobAdvert
        fields=[
            "title",
            "company_name",
            "employement_type",
            "exprience_level",
            "description",
            "job_type",
            "location",
            "deadline",
            "skills",
            "is_published",
        ]

        widgets = {
             "title":forms.TextInput(attrs={"placeholder":"Job Title","class":"form-control"}),
             "description":forms.Textarea(attrs={"placeholder":"Description","class":"form-control"}),
             "company_name":forms.TextInput(attrs={"placeholder":"company name","class":"form-control"}),
             "employement_type":forms.Select(attrs={"class":"form-control"}),
             "exprience_level":forms.Select(attrs={"class":"form-control"}),
             "job_type":forms.Select(attrs={"class":"form-control"}),
             "location":forms.TextInput(attrs={"placeholder":"optional","class":"form-control"}),
             "deadline":forms.DateInput(attrs={"placeholder":"Date","class":"form-control"}),
             "skills":forms.TextInput(attrs={"placeholder":"comma separated","class":"form-control"}),
}

class JobApplicationForm(ModelForm):
    class Meta:
        model=JobApplication
        fields=[
        "name",
        "email",
        "portfolio_url",
        "cv"
        ]
        widgets = {
             "name":forms.TextInput(attrs={"placeholder":"Your name","class":"form-control"}),
             "email":forms.EmailInput(attrs={"placeholder":"Your email","class":"form-control"}),
             "portfolio_url":forms.URLInput(attrs={"placeholder":"your portfolio link","class":"form-control"}),
             "cv":forms.FileInput(attrs={"placeholder":"select your cv","class":"form-control","accept":".pdf,.docx,.doc"}),
        }
        