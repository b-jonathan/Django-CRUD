#!C:/Users/user/AppData/Local/Programs/Python/Python310/python.exe

from itertools import product
from queue import Empty
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate  
from django.contrib.auth.forms import AuthenticationForm
from datetime import date,datetime
from django.views.generic import View
from .models import Companies, Complain, Products, ComplainCategory, ComplainDetails, IcCapa, IcProblemanalysis
from .forms import ComplainForm, DetailForm, CapaForm, PAForm
  
  
def main(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    return redirect("/complains")

def loginRequest(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}.")
        return redirect("/complains")
      else:
        messages.error(request,"Invalid username or password.")
    else:
      messages.error(request,"Invalid username or password.")
  form = AuthenticationForm()
  return render(request=request, template_name="login.html", context={"login_form":form})

def logoutView(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    logout(request)
    return redirect("/login")
  
def showComplains(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
    ctype = ['IC','NCR']
    allcomplains = Complain.objects.all().values()
    allinfolist = []
    for complain in allcomplains:
      details = ComplainDetails.objects.filter(complain_id = complain['id']).values('product_id','complaincategory_id')
      complain['articles'] = []
      for detail in details:
        detail['product_id'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
        detail['complaincategory_id'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
        complain['articles'].append(detail)
        
      complain['complain_type'] = ctype[complain['complain_type']-1]
      complain['month'] = roman[complain['document_date'].month]
      complain['year'] = complain['document_date'].year
      complain['document_date'] = complain['document_date'].strftime("%Y-%m-%d")
      complain['customer_id'] = Companies.objects.filter(id = complain['customer_id']).values_list('name',flat=True)[0]
      allinfolist.append(complain)
    template = loader.get_template('complainlist.html')
    context = {
      'allcomplains': allinfolist,
    }
    return HttpResponse(template.render(context,request))

class FilteredComplains(View):
  def get(self,request):
    if not request.user.is_authenticated:
      return redirect("/login")
    else:
      roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
      ctype = ['IC','NCR']
      if request.GET.get('periodic') != " ":
        if request.GET.get('periodic') == 'Monthly':
          startdate = datetime(date.today().year,date.today().month,1)
          enddate = datetime.now()
          startdate = startdate.strftime("%Y-%m-%d")
          enddate = enddate.strftime("%Y-%m-%d")
        if request.GET.get('periodic') == 'Yearly':
          enddate = datetime.now()
          startdate = datetime(date.today().year,1,1)
          startdate = startdate.strftime("%Y-%m-%d")
          enddate = enddate.strftime("%Y-%m-%d")
      else:
        if request.GET.get('startdate') != "":
          startdate = datetime.strptime(request.GET.get('startdate'),"%Y-%m-%d")
        else:
          startdate = datetime.strptime("1990-01-01","%Y-%m-%d")
          
        if request.GET.get('enddate') != "":
          enddate = datetime.strptime(request.GET.get('enddate'),"%Y-%m-%d")
        else:
          enddate = datetime.now()
      filteredcomplains = Complain.objects.filter(document_date__range =(startdate,enddate)).values()
      filteredinfolist = []
      for complain in filteredcomplains:
        details = ComplainDetails.objects.filter(complain_id = complain['id']).values('product_id','complaincategory_id')
        complain['articles'] = []
        for detail in details:
          detail['product_id'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
          detail['complaincategory_id'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
          complain['articles'].append(detail)
        complain['complain_type'] = ctype[complain['complain_type']-1]
        complain['month'] = roman[complain['document_date'].month]
        complain['year'] = complain['document_date'].year
        complain['customer_id'] = Companies.objects.filter(id = complain['customer_id']).values_list('name',flat=True)[0]
        filteredinfolist.append(complain)
      data = {
        'filteredcomplains': filteredinfolist,
        'test':startdate,
        'test2':enddate,
      }
      return JsonResponse(data)
    
  
def showDetails(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
    ctype = ['IC','NCR']
    alldetails = ComplainDetails.objects.all().values()
    allinfolist = []
    for detail in alldetails:
      complain = Complain.objects.filter(id = detail['complain_id']).values('customer_id','complain_type','nomor_document','document_date','notes')[0]
      complain['complain_type'] = ctype[complain['complain_type']-1]
      complain['customer_id'] = Companies.objects.filter(id = complain['customer_id']).values_list('name',flat=True)[0]
      detail['product_id'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
      detail['complaincategory_id'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
      detail['month'] = roman[complain['document_date'].month]
      detail['year'] = complain['document_date'].year
      detail.update(complain)
      allinfolist.append(detail)
    template = loader.get_template('detaillist.html')
    context = {
      'alldetails': allinfolist
    }
    return HttpResponse(template.render(context,request))

class FilteredArticles(View):
  def get(self,request):
    if not request.user.is_authenticated:
      return redirect("/login")
    else:
      roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
      ctype = ['IC','NCR']
      if request.GET.get('periodic') != " ":
        if request.GET.get('periodic') == 'Monthly':
          startdate = datetime(date.today().year,date.today().month,1)
          enddate = datetime.now()
        if request.GET.get('periodic') == 'Yearly':
          enddate = datetime.now()
          startdate = datetime(date.today().year,1,1)
      else:
        if request.GET.get('startdate') != "":
          startdate = datetime.strptime(request.GET.get('startdate'),"%Y-%m-%d")
        else:
          startdate = datetime.strptime("1990-01-01","%Y-%m-%d")
          
        if request.GET.get('enddate') != "":
          enddate = datetime.strptime(request.GET.get('enddate'),"%Y-%m-%d")
        else:
          enddate = datetime.now()
      #filtereddetails = ComplainDetails.objects.filter(document_date__range =(startdate,enddate)).values()
      alldetails = ComplainDetails.objects.all().values()
      filteredinfolist = []
      for detail in alldetails:
        complain = Complain.objects.filter(id = detail['complain_id']).values('customer_id','complain_type','nomor_document','document_date','notes')[0]
        if startdate <= datetime.combine(complain['document_date'],datetime.min.time()) and enddate >= datetime.combine(complain['document_date'],datetime.min.time()):
          complain['complain_type'] = ctype[complain['complain_type']-1]
          complain['customer_id'] = Companies.objects.filter(id = complain['customer_id']).values_list('name',flat=True)[0]
          detail['product_id'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
          detail['complaincategory_id'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
          detail.update(complain)
          filteredinfolist.append(detail)
      data = {
        'filteredarticles': filteredinfolist
      }
      return JsonResponse(data)


def showAnalysis(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
    ctype = ['IC','NCR']
    allpa = IcProblemanalysis.objects.all().values()
    painfolist = []
    for pa in allpa:
      complain = Complain.objects.filter(id = pa['complain_id']).values('complain_type','nomor_document','document_date')[0]
      detail = ComplainDetails.objects.filter(id = pa['complaindetail_id']).values('product_id','complaincategory_id','complain_description')[0]
      pa['product_name'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
      pa['complaincategory'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
      pa['complain_description'] = detail['complain_description']   
      pa['complain_type'] = ctype[complain['complain_type']-1]
      pa['nomor_document'] = complain['nomor_document']
      pa['month'] = roman[complain['document_date'].month]
      pa['year'] = complain['document_date'].year
      pa['document_date'] = complain['document_date'].strftime("%Y-%m-%d")
      painfolist.append(pa)
    
    allcapa = IcCapa.objects.all().values()
    capainfolist = []
    for capa in allcapa:
      complain = Complain.objects.filter(id = capa['complain_id']).values('complain_type','nomor_document','document_date')[0]
      detail = ComplainDetails.objects.filter(id = capa['complaindetail_id']).values('product_id','complaincategory_id','complain_description')[0]
      capa['product_name'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
      capa['complaincategory'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
      capa['complain_description'] = detail['complain_description']   
      capa['complain_type'] = ctype[complain['complain_type']-1]
      capa['nomor_document'] = complain['nomor_document']
      capa['month'] = roman[complain['document_date'].month]
      capa['year'] = complain['document_date'].year
      capa['document_date'] = complain['document_date'].strftime("%Y-%m-%d")
      capa['duedate'] = capa['duedate'].strftime("%Y-%m-%d")
      capainfolist.append(capa)
    template = loader.get_template('analysislist.html')
    context = {
      'allpa': painfolist,
      'allcapa':capainfolist
    }
    return HttpResponse(template.render(context,request))

class FilteredAnalysis(View):
  def get(self,request):
    if not request.user.is_authenticated:
      return redirect("/login")
    else:
      roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
      ctype = ['IC','NCR']
      if request.GET.get('periodic') != " ":
        if request.GET.get('periodic') == 'Monthly':
          startdate = datetime(date.today().year,date.today().month,1)
          enddate = datetime.now()
          startdate = startdate.strftime("%Y-%m-%d")
          enddate = enddate.strftime("%Y-%m-%d")
        if request.GET.get('periodic') == 'Yearly':
          enddate = datetime.now()
          startdate = datetime(date.today().year,1,1)
          startdate = startdate
          enddate = enddate
      else:
        if request.GET.get('startdate') != "":
          startdate = datetime.strptime(request.GET.get('startdate'),"%Y-%m-%d")
        else:
          startdate = datetime.strptime("1990-01-01","%Y-%m-%d")
          
        if request.GET.get('enddate') != "":
          enddate = datetime.strptime(request.GET.get('enddate'),"%Y-%m-%d")
        else:
          enddate = datetime.now()
      allpa = IcProblemanalysis.objects.all().values()
      filteredpalist = []
      for pa in allpa:
        complain = Complain.objects.filter(id = pa['complain_id']).values('complain_type','nomor_document','document_date')[0]
        if startdate <= datetime.combine(complain['document_date'],datetime.min.time()) and enddate >= datetime.combine(complain['document_date'],datetime.min.time()):
          detail = ComplainDetails.objects.filter(id = pa['complaindetail_id']).values('product_id','complaincategory_id','complain_description')[0]
          pa['product_name'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
          pa['complaincategory'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
          pa['complain_description'] = detail['complain_description']   
          pa['complain_type'] = ctype[complain['complain_type']-1]
          pa['nomor_document'] = complain['nomor_document']
          pa['month'] = roman[complain['document_date'].month]
          pa['year'] = complain['document_date'].year
          pa['document_date'] = complain['document_date'].strftime("%Y-%m-%d")
          filteredpalist.append(pa)
          
      allcapa = IcCapa.objects.all().values()
      filteredcapalist = []
      for capa in allcapa:
        complain = Complain.objects.filter(id = capa['complain_id']).values('complain_type','nomor_document','document_date')[0]
        if startdate <= datetime.combine(complain['document_date'],datetime.min.time()) and enddate >= datetime.combine(complain['document_date'],datetime.min.time()):
          detail = ComplainDetails.objects.filter(id = pa['complaindetail_id']).values('product_id','complaincategory_id','complain_description')[0]
          capa['product_name'] = Products.objects.filter(id = detail['product_id']).values_list('name',flat=True)[0]
          capa['complaincategory'] = ComplainCategory.objects.filter(id = detail['complaincategory_id']).values_list('name',flat=True)[0]
          capa['complain_description'] = detail['complain_description']   
          capa['complain_type'] = ctype[complain['complain_type']-1]
          capa['nomor_document'] = complain['nomor_document']
          capa['month'] = roman[complain['document_date'].month]
          capa['year'] = complain['document_date'].year
          capa['document_date'] = complain['document_date'].strftime("%Y-%m-%d")
          capa['duedate'] = capa['duedate'].strftime("%Y-%m-%d")
          filteredcapalist.append(capa)
      data = {
        'filteredpalist': filteredpalist,
        'filteredcapalist': filteredcapalist,
      }
      return JsonResponse(data)

def createComplains(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    form = ComplainForm()
    allcompanies = Companies.objects.filter(status = 1).values()
    return render(request,'createcomplain.html',{'form': form,'allcompanies': allcompanies})  

def detailView(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    allcategories = ComplainCategory.objects.all().values()
    request.session['temp_details'] = []
    request.session['temp_id'] = 0
    if request.method == "POST":
      request.session['customer_id'] = Companies.objects.filter(name = request.POST['customer_id']).values_list('id',flat=True)[0]
      context = {
          'complain_type': request.POST['complain_type'],
          'customer_id': request.session['customer_id'],
          'nomor_document':request.POST['nomor_document'],
          'document_date':request.POST['document_date'],
          'created_by':request.user.id,
          'created_date':date.today().strftime("%Y-%m-%d"),
          'updated_by':request.user.id,
          'updated_date':date.today().strftime("%Y-%m-%d"),
          'status':1,
          'notes':request.POST['notes'],
        }
      request.session["general_info"] = context
      complain_form = ComplainForm(context)
      companyproducts = Products.objects.filter(customer_id = context['customer_id'], status = 1).values()
      if complain_form.is_valid():
        data = {
          'customer_name': request.POST['customer_id'],
          'companyproducts': companyproducts,
          'allcategories':allcategories,
          'allprocesses': sorted(['seaming','cutting','slitting','printing']),
        }
        return render(request,'createdetails.html',data)
      else: 
        return redirect("/complains/create")
    else:
      try:
        data ={
          'customer_name'
        }
        return render(request,'createdetails.html',data)
      except:
        return redirect("/complains/create")    

class CreateDetails(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        temp_id = request.session['temp_id']
        product_name = request.GET.get('product_name', None)
        product_id = Products.objects.filter(name = product_name).values_list('id',flat=True)[0]
        process_name = request.GET.get('process_name', None)
        complain_category = request.GET.get('complain_category', None)
        complaincategory_id = ComplainCategory.objects.filter(name = complain_category).values('id')[0]
        complain_description = request.GET.get('complain_description', None)
        quantity = request.GET.get('quantity', None)
        no = {'temp_id':temp_id,'product_id':product_id,'product_name':product_name,'process_name':process_name,'complain_category':complain_category,'complaincategory_id':complaincategory_id,'complain_description':complain_description,'quantity':quantity,'status':1}
        
        
        if request.session['temp_details'] == []:
          myTemporaryList = []
        else:
          myTemporaryList = request.session['temp_details']
        
        request.session['temp_id'] = temp_id + 1
        
        myTemporaryList.append(no);  
        
        request.session['temp_details'] = myTemporaryList
        
        data = {
          'temp_detail':no,
          'temp_list':myTemporaryList
        }
        return JsonResponse(data)

def saveComplains(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    if request.method == "POST" and request.session['temp_details'] != []:
      try:
        general_info = request.session["general_info"]
      except:
        return redirect("/complains/create")
      try:
        temp_details = request.session["temp_details"]
      except:
        return redirect("/complains/create/details")

      status = 0
      if ComplainForm(general_info).is_valid():
        ComplainForm(general_info).save()
        status += 1
      for detail in temp_details:
        clean_details = {
          'complain_id': Complain.objects.latest('id').id,
          'product_id':detail['product_id'],
          'process_name':detail['process_name'],
          'complaincategory_id': ComplainCategory.objects.filter(name = detail['complain_category']).values_list('id',flat=True)[0],
          'complain_description':detail['complain_description'],
          'quantity':detail['quantity'],
          'status':detail['status'],
        }
        if DetailForm(clean_details).is_valid():
          DetailForm(clean_details).save()
          status += 1

      if status == len(temp_details)+1:
        del request.session['temp_details']
        del request.session['general_info']

      return redirect("/complains")
      '''
      context = {
        'general_info': general_info,
        'temp_details':temp_details,
        'status':status,
        'clean_details':clean_details,
      }
      return render(request,'savecomplain.html',context)
      '''
    else:
      if request.session['temp_details'] == []:
        return redirect("/complains/create/details")
      else:
        return redirect("/complains/create")

class UpdateDetails(View):
    def  get(self, request):
      if not request.user.is_authenticated:
         return redirect("/login")
      else:
        temp_id = request.GET.get('id',None) 
        temp_id = int(temp_id)
        product_name = request.GET.get('product_name', None)
        product_id = Products.objects.filter(name = product_name).values_list('id',flat=True)[0]
        process_name = request.GET.get('process_name', None)
        complain_category = request.GET.get('complain_category', None)
        complaincategory_id = ComplainCategory.objects.filter(name = complain_category).values_list('id',flat=True)[0]
        complain_description = request.GET.get('complain_description', None)
        quantity = request.GET.get('quantity', None)
        no = {'temp_id':temp_id,'product_id':product_id,'product_name':product_name,'process_name':process_name,'complain_category':complain_category,'complaincategory_id':complaincategory_id,'complain_description':complain_description,'quantity':quantity,'status':1}
        if request.GET.get('updatetype') == "beforedb":
          #temp_id is row id
          myTemporaryList = request.session['temp_details'] 
          index = next((i for i, detail in enumerate(myTemporaryList) if detail['temp_id'] == temp_id), None)
          myTemporaryList[index] = no  
          request.session['temp_details'] = myTemporaryList
          
        elif request.GET.get('updatetype') == "afterdb":
          #temp_id is detail_id
          detail = ComplainDetails.objects.get(id=temp_id)
          detail.product_id = product_id
          detail.process_name = process_name
          detail.complaincategory_id = complaincategory_id
          detail.complain_description = complain_description
          detail.quantity = quantity
          detail.save() 
          complain = Complain.objects.get(id=detail.complain_id)
          complain.updated_date = date.today()
          complain.updated_by = request.user.id
          complain.save()
        data = {
          'detail':no,
          'id': temp_id
        }
        return JsonResponse(data)
      
class DeleteDetails(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        cid = int(request.GET.get('id', None))
        myTemporaryList = request.session['temp_details']    
        myTemporaryList.pop(cid)
        request.session['temp_details'] = myTemporaryList
        data = {
            'deleted': True
        }
        return JsonResponse(data)
      
def complainsView(request,id):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
    ctype = ['IC','NCR']
    analysis_categories = ['Man','Machine','Method','Material','Environment']
    allcategories = ComplainCategory.objects.all().values()
    complain = Complain.objects.filter(id = id).values()[0]
    companyproducts = Products.objects.filter(customer_id = complain['customer_id'], status = 1).values()
    complain['complain_type'] = ctype[complain['complain_type']-1]
    complain['customer_id'] = Companies.objects.filter(id = complain['customer_id']).values_list('name',flat=True)[0]
    complain['month'] = roman[complain['document_date'].month]
    complain['year'] = complain['document_date'].year
    
    articles = ComplainDetails.objects.filter(complain_id = id).values()
    for article in articles:
      article['product_name'] = Products.objects.filter(id = article['product_id']).values_list('name',flat=True)[0]
      article['complain_category'] = ComplainCategory.objects.filter(id = article['complaincategory_id']).values_list('name',flat=True)[0]

    allpa = IcProblemanalysis.objects.filter(complain_id = id).values()
    for pa in allpa:
      pa['complain_description'] = ComplainDetails.objects.filter(id = pa['complaindetail_id']).values_list('complain_description',flat=True)[0]
      
    allcapa = IcCapa.objects.filter(complain_id = id).values()
    for capa in allcapa:
      capa['duedate'] = capa['duedate'].strftime("%Y-%m-%d")
      capa['complain_description'] = ComplainDetails.objects.filter(id = capa['complaindetail_id']).values_list('complain_description',flat=True)[0]
    
    if  request.user.groups.filter(name='Supervisor').exists() and request.user.groups.filter(name='QC').exists():
      access = 1
    else:
      access = 0
    context ={
      'complain':complain,
      'companyproducts':companyproducts,
      'analysis_categories':analysis_categories,
      'articles':articles,
      'allpa':allpa,
      'allcapa':allcapa,
      'allcategories':allcategories,
      'access' : access,
      'allprocesses': sorted(['seaming','cutting','slitting','printing']),
    }
    return render(request,'complainview.html', context)

#for Problem Analysis
def createAnalysis(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
    ctype = ['IC','NCR']
    allcomplains = Complain.objects.all().values('id','nomor_document','complain_type','document_date')
    for complain in allcomplains:
      complain_type = ctype[complain["complain_type"]-1]
      month = roman[complain["document_date"].month]
      year = complain["document_date"].year
      complain.update({'complain_type':complain_type,'month':month,'year':year})
    data = {
      'allcomplains': allcomplains,   
      }
    return render(request,'createanalysis.html', data) 

def problemAnalysisView(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    analysis_categories = ['Man','Machine','Method','Material','Environment']
    ctype = ['IC','NCR']
    request.session['temp_problemanalysis'] = []
    request.session['temp_capa'] = []
    request.session['capa_id'] = 0
    request.session['pa_id'] = 0
    roman = ['','I','II','III','IV','V','VI','VII','IX','X','XI','XII']
    if request.method == "POST":
      request.session['id'] = request.POST['id']
      nomor_document = Complain.objects.filter(id = request.session['id']).values_list('nomor_document',flat=True)[0]
      complain_type = ctype[Complain.objects.filter(id = request.session['id']).values_list('complain_type',flat=True)[0]-1]
      month_year = Complain.objects.filter(id = request.session['id']).values_list('document_date',flat=True)[0]
      data = {
        'analysis_categories': analysis_categories,
        'complain_details': ComplainDetails.objects.filter(complain_id = request.session['id']).values('id','complain_description'),
        'month_year':{'month':roman[month_year.month],'year':month_year.year},
        'nomor_document': nomor_document,
        'complain_type': complain_type
      }
      return render(request,'createproblemanalysis.html',data)
    else:
      return redirect("/analysis/create")
    
    

class CreateProblemAnalysis(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        pa_id = request.session['pa_id']
        complaindetail_id = request.GET.get('complain_detail_pa', None)
        complain_description = ComplainDetails.objects.filter(id = complaindetail_id).values_list('complain_description',flat=True)[0]
        analysis_category = request.GET.get('analysis_category', None)
        analysis_description = request.GET.get('analysis_description', None)
        no = {'temp_id':pa_id,'complain_description':complain_description,'complaindetail_id':complaindetail_id,'analysis_category':analysis_category,'analysis_description':analysis_description}
      
        
        if request.session['temp_problemanalysis'] == []:
          myTemporaryList = []
        else:
          myTemporaryList = request.session['temp_problemanalysis']
        
        request.session['pa_id'] = pa_id + 1
        
        myTemporaryList.append(no);  
        
        request.session['temp_problemanalysis'] = myTemporaryList
        
        data = {
          'temp_problemanalysis':no,
          'temp_list':myTemporaryList
        }
        return JsonResponse(data)

class UpdateProblemAnalysis(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        pa_id = request.GET.get('id',None)
        pa_id = int(pa_id)
        complain_description = request.GET.get('complain_description_pa', None)
        complaindetail_id = ComplainDetails.objects.filter(complain_description = complain_description).values_list('id',flat=True)[0]
        analysis_category = request.GET.get('analysis_category', None)
        analysis_description = request.GET.get('analysis_description', None)
        no = {'temp_id':pa_id,'complain_description':complain_description,'complaindetail_id':complaindetail_id,'analysis_category':analysis_category,'analysis_description':analysis_description}
        if request.GET.get('updatetype') == "beforedb":
          myTemporaryList = request.session['temp_problemanalysis'] 
          index = next((i for i, analysis in enumerate(myTemporaryList) if analysis['temp_id'] == pa_id), None)
          myTemporaryList[index] = no  
          request.session['temp_problemanalysis'] = myTemporaryList
        elif request.GET.get('updatetype') == "afterdb":
          pa = IcProblemanalysis.objects.get(id=pa_id)
          pa.complaindetail_id = complaindetail_id
          pa.analysis_category = analysis_category
          pa.analysis_description = analysis_description
          pa.save() 
          complain = Complain.objects.get(id=pa.complain_id)
          complain.updated_date = date.today()
          complain.updated_by = request.user.id
          complain.save()
        data = {
          'detail':no,
          'id': pa_id
        }
        return JsonResponse(data)
    
class DeleteProblemAnalysis(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        cid = int(request.GET.get('id', None))
        myTemporaryList = request.session['temp_problemanalysis']    
        myTemporaryList.pop(cid)
        request.session['temp_problemanalysis'] = myTemporaryList
        data = {
            'deleted': True
        }
        return JsonResponse(data)

#for CAPA   

class CreateCapa(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        capa_id = request.session['capa_id']
        complaindetail_id = request.GET.get('complain_description_capa', None)
        complain_description = ComplainDetails.objects.filter(id = complaindetail_id).values_list('complain_description',flat=True)[0]
        corrective_action = request.GET.get('corrective_action', None)
        perventive_action = request.GET.get('perventive_action', None)
        pic = request.GET.get('pic', None)
        duedate = request.GET.get('duedate', None)
        no = {'temp_id':capa_id,'complain_description':complain_description,'complaindetail_id':complaindetail_id,'corrective_action':corrective_action,'perventive_action':perventive_action,'pic':pic,'duedate':duedate,'verifikasi':0}
        
        
        if request.session['temp_capa'] == []:
          myTemporaryList = []
        else:
          myTemporaryList = request.session['temp_capa']
        
        request.session['capa_id'] = capa_id + 1
        
        myTemporaryList.append(no);  
        
        request.session['temp_capa'] = myTemporaryList
        
        data = {
          'temp_capa':no,
          'temp_list':myTemporaryList
        }
        return JsonResponse(data)

class UpdateCapa(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        capa_id = request.GET.get('id',None)
        capa_id = int(capa_id)
        complain_description = request.GET.get('complain_description_capa', None)
        complaindetail_id = ComplainDetails.objects.filter(complain_description = complain_description).values_list('id',flat=True)[0]
        corrective_action = request.GET.get('corrective_action', None)
        perventive_action = request.GET.get('perventive_action', None)
        pic = request.GET.get('pic', None)
        duedate = request.GET.get('duedate', None)
        verifikasi = request.GET.get('verifikasi', None)
        no = {'temp_id':capa_id,'complain_description':complain_description ,'complaindetail_id':complaindetail_id,'corrective_action':corrective_action,'perventive_action':perventive_action,'pic':pic,'duedate':duedate,'verifikasi':0}
        
        if request.GET.get('updatetype') == "beforedb":
          myTemporaryList = request.session['temp_capa'] 
          index = next((i for i, analysis in enumerate(myTemporaryList) if analysis['temp_id'] == capa_id), None)
          myTemporaryList[index] = no  
          request.session['temp_capa'] = myTemporaryList
        elif request.GET.get('updatetype') == "afterdb":
          capa = IcCapa.objects.get(id=capa_id)
          capa.complaindetail_id = complaindetail_id
          capa.corrective_action = corrective_action
          capa.perventive_action = perventive_action
          capa.pic = pic
          capa.duedate = duedate
          capa.verifikasi = verifikasi
          capa.save() 
          complain = Complain.objects.get(id=capa.complain_id)
          complain.updated_date = date.today()
          complain.updated_by = request.user.id
          complain.save()
        data = {
          'detail':no,
          'id': capa_id
        }
        return JsonResponse(data)
      
class DeleteCapa(View):
    def  get(self, request):
      if not request.user.is_authenticated:
        return redirect("/login")
      else:
        cid = int(request.GET.get('id', None))
        myTemporaryList = request.session['temp_capa']    
        myTemporaryList.pop(cid)
        request.session['temp_capa'] = myTemporaryList
        data = {
            'deleted': True
        }
        return JsonResponse(data)
      

def saveAnalysis(request):
  if not request.user.is_authenticated:
    return redirect("/login")
  else:
    if request.method == "POST":
      try:
        temp_problemanalysis = request.session["temp_problemanalysis"]
      except:
        return redirect("/analysis/create/problemanalysis")
      try:
        temp_capa = request.session["temp_capa"]
      except:
        return redirect("/complains/create/capa")

      status = 0
      for detail in temp_problemanalysis:
        clean_details = {
          'complain_id': request.session['id'],
          'complaindetail_id':detail['complaindetail_id'],
          'analysis_category':detail['analysis_category'],
          'analysis_description': detail['analysis_description'],
        }
        if PAForm(clean_details).is_valid():
          PAForm(clean_details).save()
          status += 1
          
      for detail in temp_capa:
        clean_details = {
          'complain_id': request.session['id'],
          'complaindetail_id':detail['complaindetail_id'],
          'corrective_action':detail['corrective_action'],
          'perventive_action': detail['perventive_action'],
          'pic': detail['pic'],    
          'duedate': detail['duedate'], 
          'verifikasi': 0,
          }
        if CapaForm(clean_details).is_valid():
          CapaForm(clean_details).save()
          status += 1

      if status == len(temp_problemanalysis)+len(temp_capa):
        del request.session['temp_problemanalysis']
        del request.session['temp_capa']
      return redirect("/complains/")
    else:
      return redirect("/analysis/create")