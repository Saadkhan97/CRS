from django.shortcuts import render
# from .forms import *
import re
from .main import ocr
from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
import io
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from django.core.files.base import ContentFile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def index(request):
    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_user')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            print(username,password)
            user = None
            admin_user = authenticate(request, username=username, password=password)
            if not admin_user:
                try:
                    user = UserInformation.objects.get(username=username,password1=password)
                except:
                    messages.info(request, 'Username OR password is incorrect')              
            if user is not None or admin_user is not None:
                global user_id
                user_id = user
                if user and user.role not in ['Verifier','Reviewer']:
                    return redirect('user_dashboard')
                elif admin_user and admin_user.is_superuser:
                    return redirect('books_admin')
                else:
                    return redirect('dashboard_admin')
            else:
                messages.info(request, 'Username OR password is incorrect')
            
        context = {}
        return render(request, 'VSapp/login_temp.html', context)


def register(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        try:
            obj = UserInformation.objects.create(username=username,email=email,password1=password,role=role)
            obj.save()
            user = UserInformation.objects.last()
            return redirect('login')
        except Exception as error:
            messages.info(request, 'Error occured in signup ')

    return render(request,'VSapp/register_temp.html')


def logoutp(request):
    logout(request)
    return redirect('login')

def user_dashboard(request):
    global user_id
    hadith_data = Hadith_Text_Image.objects.filter(user_id=user_id.id)
    context = {'hadith_data':hadith_data}
    return render(request,'VSapp/main_dashboard.html',context)

def upload_data(request):
    global user_id
    image_text= ""
    print(request.POST)
    
    if request.method=="POST":
        if request.POST['extract_text']:
            print("MINE",request.POST)
        if request.POST.get('c'):
            try:
                hadith_text = request.POST.get('hadith_text')
                print("s",user_id)
                obj = Hadith_Text_Image.objects.create(user_id=user_id.id,hadith_text=hadith_text)
                obj.save()
                return redirect('user_dashboard')
            except Exception as error:
                print(error)
        if request.POST.get('extract_text'):
            try:
                extract_text = request.POST.get('extract_text')
                urdu_translation = request.POST.get('urdu_translation')
                english_translation = request.POST.get('english_translation')
                hadith_url = request.POST.get('hadith_url')
                print("s",user_id)
                obj = Hadith_Text_Image.objects.create(user_id=user_id.id,hadith_text=extract_text,urdu_translation=urdu_translation,englist_translation=english_translation,url=hadith_url)
                obj.save()
                return redirect('user_dashboard')
            except Exception as error:
                print(error)

        if request.FILES['my_files']:
            a=request.FILES['my_files']
            new=ImgSaveFile.objects.create(userid=user_id.id,image_file=a)
            new.save()
            s=ImgSaveFile.objects.last()
            # print(s.file.path)
            paths=s.image_file.path
            image_text = ocr(paths)
            with open('D:/FINAL_DEFENDING/HVS/CRS/file.txt', 'r', encoding='utf-8') as myfile:
                image_text = myfile.read()
                data = re.search("(?<=\[)[^]]+(?=\])",image_text)
                # print(data.group())
                image_text = data.group()
                print('SAAD',image_text)
    print('data',image_text)
    context = {}
    if image_text:
        context = {'image_text':image_text} 
    return render(request,'VSapp/file_upload_screen.html',context)

def dashboard_admin(request):
    global user_id
    if request.method=="POST":
        try:
            hadith_text = request.POST.get('hadith_text')
            # print("s",user_id)
            obj = Hadith_Text_Image.objects.create(user_id=user_id.id,hadith_text=hadith_text)
            obj.save()
            return redirect('dashboard')
        except Exception as error:
            print(error)
    if user_id.role == 'Reviewer':
        hadith_data = Hadith_Text_Image.objects.filter(reviewer_id=user_id.id)
        print("RR",hadith_data)
        context = {'hadith_data':hadith_data}
        return render(request,'VSapp/dashboard_analyzer.html',context)
    else:        
        hadith_data = Hadith_Text_Image.objects.filter(verifier_id=user_id.id)
        print('VH',hadith_data)
        context = {'hadith_data':hadith_data} 
        return render(request,'VSapp/dashboard_verifier.html',context)

def hadith_text(request,pk):
    global user_id
    if request.method == 'POST':
        if user_id.role == 'Verifier':
            # print(request.POST.get('id'))
            ids = request.POST.get('id')
            hadith_text = request.POST.get('hadith_text')
            englist_translation = request.POST.get('english_translation')
            urdu_translation = request.POST.get('urdu_translation')
            hadith_url = request.POST.get('hadith_url')
            status = request.POST.get('v_status')
            object = Hadith_Text_Image.objects.get(id=ids)
            object.verification_status = status 
            object.hadith_status = 'Approved' if status == 'Verified' else 'Wrong'
            object.hadith_text = hadith_text
            object.url = hadith_url
            object.urdu_translation = urdu_translation
            object.englist_translation = englist_translation
            object.save()
            return redirect('dashboard_admin')
        if user_id.role == 'Reviewer':
            # print(request.POST.get('id'))
            ids = request.POST.get('id')
            hadith_text = request.POST.get('hadith_text')
            englist_translation = request.POST.get('english_translation')
            urdu_translation = request.POST.get('urdu_translation')
            hadith_url = request.POST.get('hadith_url')
            object = Hadith_Text_Image.objects.get(id=ids)
            object.hadith_text = hadith_text
            object.url = hadith_url
            object.hadith_status = 'Reviewed'
            object.urdu_translation = urdu_translation
            object.englist_translation = englist_translation
            object.save()
            return redirect('dashboard_admin')

    hadith_data = Hadith_Text_Image.objects.filter(id=pk)

    if user_id.role == 'Verifier':
        # print(hadith_data.hadith_text)
        context = {'hadith_data':hadith_data}
        return render(request,'VSapp/file_upload_screen_verifier.html',context)
    else:
        # print(hadith_data.hadith_text)
        context = {'hadith_data':hadith_data}
        return render(request,'VSapp/file_upload_screen_reviewer.html',context)



def download_pdf(request,pk):
    print(pk)
    hadith_text = Hadith_Text_Image.objects.get(id=int(pk))
    # Create a file-like buffer to receive PDF data.
    # buffer = io.BytesIO()
    # pdfmetrics.registerFont(TTFont('Nastaliq', 'D:/FINAL_DEFENDING/HVS/CRS/urdu.ttf'))
    # pdfmetrics.registerFont(TTFont('ArabicFont', 'D:/FINAL_DEFENDING/HVS/CRS/arabic.ttf'))
    # Create the PDF object, using the buffer as its "file."
    # Generate the PDF
    response = HttpResponse(content_type='application/pdf; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'

    # Create a PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Use a font that supports Arabic, for example, "Arial"
    pdf.setFont("Arial", 12)

    # Your Arabic text
    arabic_text = u'مرحبا بالعالم'

    # Draw the Arabic text on the PDF
    pdf.drawString(100, 700, arabic_text)

    # Save the PDF content
    pdf.save()

    # Get the PDF content from the buffer and attach it to the response
    pdf_bytes = buffer.getvalue()
    buffer.close()
    response.write(pdf_bytes)

    return response

def books_admin(request):
    pdfmetrics.registerFont(TTFont('Nastaliq', 'D:/FINAL_DEFENDING/HVS/CRS/urdu.ttf'))
    pdfmetrics.registerFont(TTFont('Naskh', 'D:/FINAL_DEFENDING/HVS/CRS/arabic.ttf'))
    # Create the PDF object, using the buffer as its "file."
    # Generate the PDF
    if request.method == 'POST':
        # print(request.POST)
        books_data = Book_Table.objects.last()
        hadith = Hadith_Text_Image.objects.filter(book_id=0,hadith_status='Approved')
        hadith_count = request.POST.get('page_count')
        if books_data:
            new_book_number = books_data.id + 1
        else:
            new_book_number = 0
        buffer = io.BytesIO()
        x = 100
        y = 600
        line_spacing = 20    
        p = canvas.Canvas(buffer)
        if hadith:
            for object in hadith:
                # Positioning the text in the PDF
                # Urdu Translation
                p.drawString(x, y, "Original Text:")
                y -= line_spacing
                p.setFont('Naskh', 12) 
                p.drawString(x, y, object.hadith_text)
                y -= line_spacing * 2  # Add extra spacing after Urdu translation

                # English Translation
                p.drawString(x, y, "English Translation:")
                y -= line_spacing
                p.drawString(x, y, object.englist_translation)
                y -= line_spacing * 2  # Add extra spacing after English translation
                # Original Text
                p.drawString(x, y, "Urdu Translation:")
                p.setFont('Nastaliq', 12) 
                y -= line_spacing
                p.drawString(x, y, object.urdu_translation)
                p.showPage()
                y -= 50
            p.save()
            
            book_name = 'Book' + str(new_book_number) + '.pdf'
            book = Book_Table.objects.create(book_name=book_name)
            book.book_files.save(book_name,ContentFile(buffer.getvalue()))
            new_book_number += 1
            for had in hadith:
                print(had.book_id)
                obj = Hadith_Text_Image.objects.get(id=int(had.id))
                obj.book_id = str(book.id)
                obj.save()
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    books = Book_Table.objects.all()
    context = {'books':books}
    return render(request,'VSapp/dashboard_admin.html',context)

def user_books(request):
    books = Book_Table.objects.all()
    context = {'books':books}
    return render(request,'VSapp/user_book_page.html',context)
