from django.db import models
from django.urls import reverse
from common.models import BaseModel
from accounts.models import User
from .enums import EmployementType,ExprienceLevel,LocationTypeChoice,ApplicationStatus
# Create your models here.
class JobAdvert(BaseModel):
    title=models.CharField(max_length=150)
    company_name=models.CharField(max_length=150)
    employement_type=models.CharField(max_length=60,choices=EmployementType)
    exprience_level=models.CharField(max_length=50,choices=ExprienceLevel)
    description=models.TextField()
    job_type=models.CharField(max_length=50,choices=LocationTypeChoice)
    location=models.CharField(max_length=255,null=True,blank=True)
    is_published=models.BooleanField(default=True)
    deadline=models.DateField()
    skills=models.CharField(max_length=255)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        ordering=("-created_at",)
    
  
    def publish_advert(self)->None:
        self.is_published=True
        self.save(update_fields=["is_published"])  
    @property
    def total_applicants(self):
        return self.applications.count() 
    def get_absolute_url(self):
        return reverse('job_advert',kwargs={"advert_id":self.id})     
class JobApplication(BaseModel):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    portfolio_url=models.URLField()
    cv=models.FileField()
    status=models.CharField(max_length=20,choices=ApplicationStatus.choices,default=ApplicationStatus.APPLIED)       
    job_advert=models.ForeignKey(JobAdvert,related_name="applications",on_delete=models.CASCADE)