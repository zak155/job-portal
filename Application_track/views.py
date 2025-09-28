from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.models import User
from .forms import JobAdvertForms,JobApplicationForm
from .models import JobAdvert, JobApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator
@login_required
def create_advert(request:HttpRequest):
    form=JobAdvertForms(request.POST or None)
    if form.is_valid():
        instance:JobAdvert=form.save(commit=False)
        instance.created_by=request.user
        instance.save()

        messages.success(request,"adevert created Sucessfully,You can recieve applications")
        return redirect(instance.get_absolute_url())

    context={
        "job_advert_form":form,
        "title":"create new Application",
        "btn_text":"create advert"
    }    
    return render(request,"create_advert.html",context)

def get_advert(request:HttpRequest,advert_id):
    form=JobApplicationForm()
    job_advert=get_object_or_404(JobAdvert,pk=advert_id)
    context={
        "job_advert":job_advert,
        "application_form":form
    }
    return render(request,"advert.html",context)

def list_adverts(request:HttpRequest):
    active_jobs=JobAdvert.objects.filter(is_published=True,deadline__gte=timezone.now().date())
    paginator=Paginator(active_jobs,10)
    requested_page=request.GET.get("page")
    paginated_adverts=paginator.get_page(requested_page)
    context={
        "job_adverts":paginated_adverts,
        
    }
    return render(request,"home.html",context)
@login_required
def apply(request:HttpRequest,advert_id):
      advert=get_object_or_404(JobAdvert,pk=advert_id)
      form=JobApplicationForm(request.POST,request.FILES)
      if form.is_valid():
          #prevent email duplication
          email=form.cleaned_data['email']
          if advert.applications.filter(email__iexact=email).exists():
             messages.error(request,"you are already applied")
             return redirect("job_advert",advert_id=advert_id)
          #save the application
          application:JobApplication=form.save(commit=False)
          application.job_advert=advert
          application.save()
          messages.success(request,"Application created sucessfuly")
          return redirect("job_advert",advert_id=advert_id)
      else:
         form=JobApplicationForm()
      context={
          "job_advert":advert,
          "application_form":form
      }   
      return render(request,'advert.html',context) 
def my_application(request:HttpRequest):
     user:User=request.user
     application=JobApplication.objects.filter(email=user.email)
     paginator=Paginator(application,10)
     requested_page=request.GET.get("page")
     paginated_applications=paginator.get_page(requested_page)

     context={
         "my_applications":paginated_applications
     }
     return render(request,"my_applications.html",context)
@login_required
def my_job(request:HttpRequest):
    user:User=request.user
    jobs=JobAdvert.objects.filter(created_by=user)
    paginator=Paginator(jobs,10)
    requested_page=request.GET.get('page')
    paginated_jobs=paginator.get_page(requested_page)  

    context={
        "my_jobs":paginated_jobs,
        "current_date":timezone.now().date()
    } 

    return render(request,'my_jobs.html',context)  
@login_required
def update_advert(request:HttpRequest,advert_id):
    advert:JobAdvert=get_object_or_404(JobAdvert,pk=advert_id)  
    if request.user!=advert.created_by:
        return HttpResponseForbidden("You can only update ana advert created by you ") 
    form=JobAdvertForms(request.POST or None,instance=advert)
    if form.is_valid():
        instance:JobAdvert=form.save(commit=False)
        instance.save()
        messages.success(request,"Advert updated successfully.") 
        return redirect(instance.get_absolute_url()) 
    context={
        "job_advert_form":form,
        "btn_text":"update advert"
    } 
    return render(request,"create_advert.html",context)
@login_required
def delete_advert(request:HttpRequest,advert_id):
    advert:JobAdvert=get_object_or_404(JobAdvert,pk=advert_id)
    if request.user!=advert.created_by:
        return HttpResponseForbidden("You can only delete if you created by you")
    advert.delete()
    messages.success(request,"you deleted succesfully")
    return redirect("my_job")
@login_required
def advert_applications(request:HttpRequest,advert_id):
    advert:JobAdvert=get_object_or_404(JobAdvert,pk=advert_id)
    if request.user!=advert.created_by:
        return HttpResponseForbidden("You can only see applications for an advert created by you")
    applications=advert.applications.all()
    applications=JobApplication.objects.filter(job_advert=advert.id)
    paginator=Paginator(applications,10)
    requested_page=request.GET.get("page")
    paginated_applications=paginator.get_page(requested_page)
    context={
        "applications":paginated_applications,
        "advert":advert
    }
    return render(request,"advert_applications.html",context)
    