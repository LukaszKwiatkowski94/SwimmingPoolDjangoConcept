from multiprocessing import context
from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Passes
from .forms import PassForm
from django.core.serializers.json import DjangoJSONEncoder
import json

def show(request):
    try:
        passes = Passes.objects.filter(active=True)
        context = {
            'passes':passes
        }
        return render(request,'show.html',context)
    except:
        raise Http404("Get Passes does not exist")

def createPass(request):
    try:
        form = None
        if request.POST:
            form = PassForm(request.POST)
            if form.is_valid():
                form.save()
        if request.GET:
            form = PassForm()
            context = {
                'form':form,
                'name':"create"
            }
        return render(request, 'create-update.html',context)
    except:
        raise Http404("Create Pass does not exist")

def updatePass(request,idPass):
    try:
        form = None
        passItem = Passes.object.get(id=idPass)
        if request.POST:
            form = PassForm(request.POST)
            obj = form.save(commit=False)
            if form.is_valid() and passItem != obj:
                passItem.active = False
                passItem.save()
                newPass = Passes(namePass=obj.namePass,daysOfUse=obj.daysOfUse,price=obj.price)
                newPass.save()
        if request.GET:
            form = PassForm(instance=passItem)
            context = {
                'form':form,
                'name':"update"
            }
        return render(request, 'create-update.html',context)
    except:
        raise Http404("Update Pass does not exist")

def showAllListPasses(request):
    try:
        passes = Passes.objects.all().order_by(active=True)
        context = {
            'passes':passes
        }
        return render(request,'showAllListPasses.html',context)
    except:
        raise Http404("Passes does not exist")

def deactivatePass(request):
    if request.POST:
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            idPass = body['idPass']
            post = Passes.objects.get(id=idPass)
            post.active != post.active
            post.save()
            data = json.dump(post.active, cls=DjangoJSONEncoder)
        except:
            data = json.dump('Error', cls=DjangoJSONEncoder)
        return HttpResponse(data,content_type='application/json')
    else:
        raise Http404("Passes does not exist")