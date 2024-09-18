from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.utils.text import slugify
from django.contrib import messages
import datetime
# import json

from jobs.forms import CreateJobForm,FormContainerForm,CustomFormContainer
from jobs.models import CreateJob,ContactusImageMap,FormContainer

def home(request):
	jobs_modl = CreateJob.objects.all()		
	context = {'jobs':jobs_modl}
	return render(request,'home.html',context)

def search_feature(request):
	if request.method == 'POST':
		search_query = request.POST.get('search_query')
		jobs_modl = CreateJob.objects.filter(Q(company_name__icontains=search_query) | Q(job_title__icontains=search_query))
		context = {'query':search_query,'searched':jobs_modl}
		return render(request,'home.html',context)
	
@login_required
def createjob(request):
	form = CreateJobForm(request.POST or None,request.FILES or None)
	second_form = CustomFormContainer(request.POST or None)
	modl = CreateJob.objects.all()
	# formset = formset_fac(request.POST or None,prefix = 'items')

	# if form.is_valid():

	# 	obj = form.save(commit = False)
	# 	obj.user = request.user
	# 	obj.save()
	# 	messages.add_message(request,messages.SUCCESS,'Job Created!')
	# 	status = {'id':f'{obj.id}','name':f'{obj.company_name}'}

	# 	return JsonResponse(status,safe=False)

	# if request.method == 'POST':
	# 	name = request.POST.get('title')
	# 	content = request.POST.get('content')
	# 	heading_id = request.POST.get('create_job_name')
	# 	print(type(heading_id))
	# 	for i in modl:
	# 		if i.id == int(heading_id):	
	# 			FormContainer(createjob= i,title = name,content = content).save()
	# 			print('saved')
	# 			return redirect(reverse('jobs:detail',args=(CreateJob.objects.get(id=i.id).id,)))

	if form.is_valid() and request.method == 'POST':
		obj = form.save(commit = False)
		obj.user = request.user
		obj.save()

		print(obj.id)

		FormContainer(createjob = obj,title = request.POST.get('title'),content = request.POST.get('content')).save()
		print('saved')
		return redirect('jobs:home')


	context = {
		'form':form,
		'second_form':second_form,
		}
	return render(request,'cj_form.html',context)

def updatejob(request,id):
	jobs_model = get_object_or_404(CreateJob,id = id,user = request.user)
	form = CreateJobForm(request.POST or None,request.FILES or None,instance=jobs_model)

	# if form.is_valid():
	# 	obj = form.save(commit = False)
	# 	messages.add_message(request,messages.SUCCESS,'job information Updated!')
	# 	obj.save()
	# 	updated_slug = obj.company_name
	# 	return JsonResponse({'status':'success'},safe=False)
	# 	# return redirect(reverse('jobs:detail',args=(slugify(obj.company_name),)))

	# formContainermodel = FormContainer.objects.get(createjob = jobs_model.id)
	# customformcontainer = CustomFormContainer(initial={'title':formContainermodel.title,'content':formContainermodel.content})

	# if request.method == 'POST':
	# 	formContainermodel.title = request.POST.get('title')
	# 	formContainermodel.content = request.POST.get(	'content')
	# 	formContainermodel.save()
	# 	print('saved')
	# 	return redirect(reverse("jobs:detail",args=(jobs_model.id,)))

	formcontainermodel = FormContainer.objects.get(createjob = jobs_model.id)
	customformcontainer = CustomFormContainer(initial={'title':formcontainermodel.title,'content':formcontainermodel.content})

	if form.is_valid() and request.method == 'POST':
		obj = form.save(commit = False)
		obj.save()
		
		formcontainermodel.title = request.POST.get('title')
		formcontainermodel.content = request.POST.get('content')
		formcontainermodel.save()

		messages.add_message(request,messages.SUCCESS,'jobs information updated')
		updated_slug = obj.company_name
		return redirect(reverse('jobs:detail',args=(jobs_model.id,)))


	context = {
		'form':form,
		'jobs_model':jobs_model,
		'customformcontainer':customformcontainer,
		}
	return render(request,'updatejob.html',context)

# @login_required
def jobDetail(request,id):
	job_detail = CreateJob.objects.get(id = id)
	modl = CreateJob.objects.all()
	formcontainer = FormContainer.objects.filter(createjob=job_detail.id)

	context = {
		'job_detail':job_detail,
		'formcontainer':formcontainer,
		'date':datetime.date.today(),
	}
	return render(request,'j_detail.html',context)

@login_required
def jobDelete(request,id):
	# slug = request.POST.get('slug')
	# print(f"my slug==================={slug}")
	post = get_object_or_404(CreateJob,id = id,user = request.user)
	post.delete()
	messages.add_message(request,messages.SUCCESS,'post deleted')
	return redirect(reverse('jobs:home'))


def contactus(request):
	# contactimagemap = ContactusImageMap.objects.all()
	contact_Texts = "If you have any questions or comments, we would very much like to hear from you. We value your comments, complaints, and suggestions."
	notes = [
		'For Further information on our services and the JobsNepal.com system, please use the form below or email:',
		'For support and technical questions, please contact our support team: support@sabaikojobs.com',
		'For Sales and Marketing questions, please contact our sales team: info@sabaikojobs.com'
	]
	contact_calls = 'You can also call us during business hours in Nepal at: (977-1) xxxxxxx/ xxxxxxx (Sunday-Friday)'
	context = {
		'contact_Texts':contact_Texts,
		'notes':notes,
		'contact_calls':contact_calls,
		# 'contactimagemap':contactimagemap,
	}
	return render(request,'contactus.html',context)


def aboutus(request):
	title = "Welcome to the sabaikojobs.com"
	first_para = "Welcome to sabaikojobs.com, the largest locally focused employment website in the nation! Our mission is to lead the Internet employment industry in Nepal by providing innovative information, superior resume management software and a comprehensive selection of services."
	second_para = "sabaikojobs.com offers services to the recruiting and job-seeking community in Nepal. We are the only recruitment service provider with 100% free service to all the jobseekers."
	third_para = "It is our mission to bring the burgeoning Nepalese Internet and computing talent to bear on international Web development."
	context = {
		'title':title,
		'first_para':first_para,
		'second_para':second_para,
		'third_para':third_para,
	}
	return render(request,'aboutus.html',context)