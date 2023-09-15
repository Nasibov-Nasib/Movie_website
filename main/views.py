from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from .models import *
import sqlite3
import json
import requests
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail

db = sqlite3.connect('bazasites3.db' ,  check_same_thread=False)
db2 = sqlite3.connect('db.sqlite3' ,  check_same_thread=False)
sql2 = db2.cursor()

sql = db.cursor()
sql.execute(""" CREATE TABLE IF NOT EXISTS tmdb(
            kinoadi TEXT,
            poster TEXT,
            category TEXT,
            runtime TEXT,
            vote TEXT,
            overview TEXT,
            foto TEXT
            

            
            
            ) """)

sql.execute(""" CREATE TABLE IF NOT EXISTS videocdn(
            kinoadi1 TEXT,
            url TEXT,
            il TEXT
            
            
            
            
            ) """)
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



# def post_list(request):
  
#     return render(request, 'main/posts.html', {'numbers': numbers})



def axtar(request):
    x = request.POST['sorgu']
    mykino=Kinodata.objects.filter(Q(ad__contains=x)).distinct()
    
    data={'mykino':mykino,'x':x}
    return render(request,'main/axtar.html',data)
    
def about(request):
    return render(request,'main/about.html')

def contacts(request):
    
    # if request.method =='POST':
    #     message = request.POST['message']
    #     name = request.POST['name']
    #     email = request.POST['email']
    #     subject = request.POST['subject']
    #     daxil_et = Contactus(message=message,name=name,email=email,subject=subject)
    #     daxil_et.save()
    if request.method =='POST':
        msg = request.POST['messages']
        name = request.POST['name']
        email = request.POST['email']
        sbjct = request.POST['subject']

        subject= request.POST['name'], request.POST['subject'], request.POST['email']  
        message = "Hörmetli, "+ name+ " göndərdiyiniz "+ sbjct+ " -email müraciətə baxilacaq. Tezlikle sizə geri dönüş ediləcək. Köməyə ehtiyacınız varsa, lütfən, marketinq sualları üçün [e-poçt və telefon nömrəsi] ilə və ya mühasibat sualları üçün [e-poçt və telefon nömrəsi] ilə əlaqə saxlayın."
        
        email_from = settings.EMAIL_HOST_USER
        qebul_eden = [email,]
        qebul = ["horadiztorpag2017@gmail.com",]
        
        send_mail(sbjct,message,email_from,qebul_eden)
        
        send_mail(subject, msg, email_from, qebul)

    return render(request,'main/contacts.html')






def videocdn(request):
    x=0
    while x <5000:

        x+=1 
        response = requests.get('https://videocdn.tv/api/movies?api_token=YypuEI5zC5gcJdwWoYiDtqzD4xYfAyol&page='+str(x)+'')
            
        data = response.text
            
        data  = json.loads(data)
        # print('Kino sayi: '+str(len(data['data'])))
        i=0
        while i< 19:
            
            kinoadi = data['data'][i]['orig_title']
            url = data['data'][i]['media'][0]['path']
            il = data['data'][i]['released']

            i+=1

            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO videocdn VALUES (?,?,?)",(kinoadi,url,il))
            db.commit()
            sql.close
            
            if i==20:
                break
    return HttpResponseRedirect(reverse('yenikino'))
    
def addkino(request):
    spage =Cronsettings.objects.get(id=1)
    p = spage.page
    y= spage.year
    if p>=30:
        #send email 
        sql2.execute(f'UPDATE main_cronsettings SET year=year+{1}')
        sql2.execute(f'UPDATE main_cronsettings SET page={1}')
    
    stop = p + 5
    dsay = 0
    
    while p<=stop:
        p+=1
        dsay+=1
        #print(x)
        response = requests.get('https://api.themoviedb.org/3/discover/movie?primary_release_date.gte='+str(y)+'-01-01&primary_release_date.lte='+str(y)+'-12-31&api_key=bfcf5c690b26e9b5ca2633b37551c638&page='+str(p))
        data = response.text
        #print(data)
        data  = json.loads(data)
        #seh = data['page']
        #kino_sayi= data['results']
        i = 0
        while(i<len(data['results'])):
            original_title = data['results'][i]['original_title']
            overview = data['results'][i]['overview']
            try: 
                poster = data['results'][i]['poster_path']
                poster= "https://image.tmdb.org/t/p/original/"+poster
            except: TypeError, IntegrityError
            vote_average = data['results'][i]['vote_average']
            release_date = data['results'][i]['release_date']
            dil=data['results'][i]['original_language']
            
            try:
                if len(data['results'])>0:
                    foto = 'https://image.tmdb.org/t/p/original'+data['results'][i]['backdrop_path']
                else:
                    foto = "1"
            except: TypeError

            movie_id = data['results'][i]['id']
            response2 = requests.get('https://api.themoviedb.org/3/movie/' + str(movie_id) + '/videos?api_key=7cfd8250d36c989c76d178509c4f118f')
            data2 = response2.text
            data2  = json.loads(data2)
            # print(data2)
            #treyler qisa videolar
            if len(data2["results"])>0:
                treyler = data2['results'][0]['key'] 
                treyler = "https://www.youtube.com/watch?v="+treyler
            else:
                treyler="https://www.youtube.com/watch?v="+treyler

            #kateqoriya
            
            response3 = requests.get('https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key=7cfd8250d36c989c76d178509c4f118f')
            data3 = response3.text
            data3  = json.loads(data3)

            try:
                if len(data3['genres'][0]['name'])>0:
                    cat = data3['genres'][0]['name']
            except: IndexError
           
            if data3['runtime']>0:
                vaxt = data3['runtime']
            else:
                vaxt = "1"

            #print(original_title)
            #print(overview)
            #print(video)
            
            if sql.fetchone() is  None:
                
                sql.execute(f"INSERT INTO tmdb VALUES (?,?,?,?,?,?,?)",(original_title,poster,cat,vaxt,vote_average,overview,foto))
            db.commit()
            sql.close
            i+=1
            
       
        if dsay==5:
            sql2.execute(f'UPDATE main_cronsettings SET page=page+{5}')
            db2.commit()
            break
    
       
   
    
        
    
    return HttpResponseRedirect(reverse('yenikino'))

def delete1(self):
    Kinodata.objects.all().delete()
    return HttpResponseRedirect(reverse('yenikino'))

def index(request):

    # if request.method == 'POST':
        
    #     if 'ok' in request.POST:
            
    #         s = 'he'
    
   
    blok7 = Kinodata.objects.all().order_by('-id')[54:72]
    blok01 = Kinodata.objects.all().raw('SELECT * FROM main_Kinodata GROUP BY category    ')
    blok2 = Kinodata.objects.all().order_by("?")[1:9]
    blok3 = Kinodata.objects.all().order_by('-id')[9:27]
    blok = Kinodata.objects.all().order_by('-id')
    blok4= Kinodata.objects.all().order_by('-id')[27:36]
    blok5= Kinodata.objects.all().order_by('-id')[36:42]
    blok6= Kinodata.objects.all().order_by('-id')[42:54]
    kat = Kinodata.objects.raw('SELECT * FROM main_kinodata WHERE kateqoriya ')
    # news = Kinodata.objects.filter(kateqoriya=kat).distinct()
    
    blok8 = Kinodata.objects.all().distinct().order_by("?")
    nsay = Kinodata.objects.values_list("ad").count()

    # numbers_list = range(1,nsay)
    page = request.GET.get('page', 1)
    paginator = Paginator(blok8, per_page=6)
    
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
        
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
        
    # if 'axtar' in request.POST:
    
    #     x = request.POST['sorgu']
    #     blok2=Kinodata.objects.filter(Q(ad__contains=x))
    #     data={'x':x,'blok2':blok2}
    #     return render(request,'main/index.html',data) 
        
    context = {"nsay":nsay, 'blok01':blok01,'numbers': numbers, 'blok':blok,'blok2':blok2,'blok3':blok3,'blok4':blok4,'blok5':blok5,'blok6':blok6,'blok7':blok7,'blok8':blok8}
    return render(request,('main/index.html'),context)

# def ajaxloader(request):
    

def details(request,id):
    
    if request.method=='POST':
        
        
        message = request.POST['message']
        comment_id = request.POST['id']
        daxil_et = Comment(message=message,comment_id=comment_id)
        daxil_et.save()
    my_kino=Kinodata.objects.filter(id=id)
    comments = Comment.objects.filter(comment_id=id).order_by('-id')
    com = Comment.objects.filter(comment_id=id).order_by('-id').count()
    blok6= Kinodata.objects.all().order_by('-id')[42:54]
    blok7 = Kinodata.objects.all().order_by('-id')[54:58]
    blok01 = Kinodata.objects.all().raw('SELECT * FROM main_Kinodata GROUP BY category    ')


    template = loader.get_template("main/details.html")
    data = {"my_kino": my_kino,'comments':comments,'id':id,'com':com,'blok6':blok6,'blok7':blok7,'blok01':blok01}
    return HttpResponse(template.render(data,request))


def category(request, id):
    r = Kinodata.objects.get(id=id)
    kat = r.category
    news = Kinodata.objects.filter(category=kat)
    
    return render(request,('main/category.html'),{"news":news})

def yenikino(request):
    my_kino=Kinodata.objects.all()
    nsay = Kinodata.objects.values_list("ad").count()
    template = loader.get_template("main/yenikino.html")
    blok = Kinodata.objects.all().order_by('-id')
    sql.execute("SELECT * FROM tmdb, videocdn WHERE  tmdb.kinoadi =  videocdn.kino GROUP BY kinoadi, kino ")
    for x in sql:     
        
        
        add = Kinodata(ad=x[0] ,video_link= x[8] ,foto = x[6] , il = x[9] ,category=x[2],runtime=x[3], reytinq=x[4], poster =x[1], melumat=x[5])
        add.save()

        
    data = {"my_kino": my_kino, 'nsay':nsay,'blok':blok}
    return HttpResponse(template.render(data,request))