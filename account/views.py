# -*- coding: utf-8 -*-
from distutils.command.register import register
from django.shortcuts import render,HttpResponse,redirect
from forms import RegisterForm, DocumentForm, FileStorageForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from models import Document,Book,FileStorage
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.db.models import Q
import re,os
from django import template
from django.views.decorators.csrf import csrf_exempt
import mimetypes
@login_required
def home(request):
    args = {'last_login':request.user.last_login}
    return render(request,'home.html',args)
@login_required
def about(request):
    user = request.user
    request.session['username'] = user.username
    session_user = request.session['username']
    return render(request,'about.html',{'user':user,'session_user':session_user})
@login_required
def profile(request):
    if request.user.is_superuser:
        users = User.objects.all()
    else:
        users = User.objects.filter(username=request.user)
    args = {'users':users}
    return render(request,'profile.html',args)
@login_required
def createUser(request):
    form = RegisterForm()
    if request.method == 'POST':
        frm_user = RegisterForm(request.POST)
        if frm_user.is_valid():
            frm_user.save()
            return redirect('/account/profile')
        else:
            return render(request,'createuser.html',{'form':form})
    else:
        return render(request,'createuser.html',{'form':form})
@login_required
def changePass(request):
    if request.method == 'POST':
        frm_changepass = PasswordChangeForm(request.user,request.POST)
        if frm_changepass.is_valid():
            user = frm_changepass.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your account is updated new password')
            return redirect('/account/profile')
        else:
            messages.error(request,'Error:Cannot change password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request,'changepass.html',{'form':form})
@login_required
def upload_document(request):
    if request.method == 'POST':
        frm_upload = DocumentForm(request.POST,request.FILES)
        if frm_upload.is_valid():
            new_pic = Document()
            new_pic.description = frm_upload.cleaned_data['description']
            new_pic.doc = request.FILES['doc']
            new_pic.save()
            return redirect(list_file_after_uploaded)
    else:
        form = DocumentForm()
        return render(request, 'upload_documents.html',{'form':form})
@login_required
def upload_file(request):
    if request.method == 'POST':
        frm_upload_file = FileStorageForm(request.POST,request.FILES)
        if frm_upload_file.is_valid():
            new_file = FileStorage()
            new_file.description = frm_upload_file.cleaned_data['description']
            new_file.filename = request.FILES['filename']
            new_file.images = request.FILES['images']
            new_file.save()
            return redirect(view_list_files)
    else:
        form = FileStorageForm()
        return render(request, 'upload_images.html',{'form':form})
@login_required
def delete_document(request):
    if request.method == 'POST':
        idDoc = request.POST['txtIdDoc']
        pathImage = request.POST['txtPath']
        convertIdDoc = int(idDoc)
        doc = Document.objects.get(id=convertIdDoc)
        if doc :
            doc.delete()
            os.remove(pathImage)
    return redirect(list_file_after_uploaded)
@login_required
def list_file_after_uploaded(request):
    modelFileUpload = Document.objects.all()
    args = {'list_image':modelFileUpload}
    return render(request, 'list_images.html',args)
@login_required
def loadBook(request):
    bookModel = Book.objects.all()
    return render(request,'book.html',{'book_list':bookModel})
def validateUserLogin(request):
    username = request.GET.get('username',None)
    #username.user_permissions.add('')
    data = {
        'is_taken':User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
@login_required
def viewPermission(request):
    perms = Permission.objects.filter(user=request.user)
    getAllPerms = Permission.objects.exclude(id__in=perms)
    args = {'permList':perms,'user':request.user,'listPerms':getAllPerms}
    return render(request,'permissions.html',args)
def add_perms(request):
    valuePerms = request.POST['listPermission']
    request.user.user_permissions.add(valuePerms)
    return redirect(viewPermission)
def delete_perms(request):
    id_perms = request.POST['txt_perm']
    request.user.user_permissions.remove(id_perms)
    return redirect(viewPermission)
def search_user(request):
    if request.method == 'POST':
        txtInput = request.POST['txtInput']
        if txtInput:
            users = User.objects.filter(Q(username__icontains = txtInput)|Q(first_name__icontains = txtInput)|Q(last_name__icontains = txtInput)|Q(email__icontains = txtInput))
        else:
            users = []
        args = {'users':users,'txtInput':txtInput}
        return render(request,'profile.html',args)
    else:
        return redirect(profile)
def deleteObjectSelected(request):
    if request.method == 'POST':
        txtValue = request.POST['txtValue']
        listCheck = re.compile(":").split(txtValue)
        if txtValue:
            for item in listCheck:
                request.user.user_permissions.remove(item)
    return redirect(viewPermission)
def removeAllPermission(request):
    if request.method == 'POST':
        countItemPerms = request.user.user_permissions.count()
        if countItemPerms > 0:
            request.user.user_permissions.clear()
    return redirect(viewPermission)
def view_list_files(request):
    list_file = FileStorage.objects.all()
    args = {'list_file':list_file}
    return render(request, 'list_documents.html',args)
def download_file(request):
    if request.method == 'POST':
        idFile = request.POST['txtId']
        objectFile = FileStorage.objects.get(id=idFile)
        filename = objectFile.filename.name.split('/')[-1]
        content_file = mimetypes.guess_type(objectFile.filename.path)[0]
        response = HttpResponse(objectFile.filename, content_type=content_file)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    else:
        return redirect(view_list_files)
def print_file(f):
    try:
        return f.read()
    except IOError:
        return ''
@csrf_exempt
def view_file_content(request):
    if request.method == 'POST':
        idFile = request.POST['txtIdFile']
        objects = FileStorage.objects.get(id=idFile)
        filename = objects.filename.path
        if not os.path.isfile(objects.filename.path):
            raise ValueError("File doesn't exist")
        else:
            with open(filename,mode='rb') as pdf:
                response = HttpResponse(pdf.read(),content_type=mimetypes.guess_type(filename)[0])
                response['Content-Disposition'] = 'inline;filename=%s' % filename
                return response
    else:
        return redirect(view_list_files)
register = template.Library()
@register.inclusion_tag('new_template.html')
def test_include():
    list_user = User.objects.all()
    return {'list_user':list_user}
