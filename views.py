from django.shortcuts import render#, redirect
#from .models import Task
#from .forms import TaskForm



def index(request):
    return HttpResponse('<h4>Добро пожаловать на сайт от компании Likefi</h4>')


def index(request):
    #tasks = Task.objects.all()
    return render(request,'main/index.html')#, {'title': 'Главная страница сайта ', 'tasks':tasks})

def about(request):
    return render(request,'main/about.html')

def contacts(request):
    #task = Task.object.order_by('-id')
   # error = ''
   # if request.method == 'POST':
       # form = TaskForm(request.POST)
      #  if form.is_valid():
          #  return form.save()
          #  redirect('/')
        #else:
           # error = 'Форма была неверной'
   # form = TaskForm()
   # context = {
       # 'form':form,
       # 'error':error


   # }
    return render(request,'main/contacts.html')


