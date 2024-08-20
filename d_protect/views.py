from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Create_Acc
from .models import Employee
from django.core.files.storage import FileSystemStorage

# Create your views here.

def home_page(request):
    return render(request,template_name='home.html')

def Create_Accs(request):
    if User.objects.exists():
        return render(request, 'Create_Acc.html', {'Result': 'An account has already been created. No further accounts can be created!'})

    if request.method == "POST":
        username = request.POST.get('email')  
        password = request.POST.get('password')
        name = request.POST.get('nm')

        try:
            user = User.objects.create_user(username=username, password=password, first_name=name)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('../accounts/login/')  

        except IntegrityError:
            return render(request, 'Create_Acc.html', {'Result': 'Email ID already exists. Please try another email.'})
        except Exception as ex:
            return render(request, 'Create_Acc.html', {'Result': f'An error occurred: {ex}'})
    
    return render(request, 'Create_Acc.html')

# Direct update  Record
def update_emp(request):
        try:
    
            emp_sno = request.POST.get('sno')
            name = request.POST.get('name')
            aadhaar = request.POST.get('aadhaar')
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')
            
            obj=Employee.objects.get(sno=emp_sno)
            
            obj.name = name
            obj.aadhaar = aadhaar
            obj.mobile = mobile
            obj.address = address
            
            
            obj.save()
            return render(request,template_name='update_emp.html',context={'result':'Data Updated Successfully'})
        except Exception as ex:
            return render(request,template_name='update_emp.html',context={'result':ex})
    
        


@login_required
def welcome_dashboard(request):
    return render(request,template_name='welcome.html')

def logout_view(request):
    logout(request)  
    return redirect('home_page_acesss')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            return redirect('/dashboard')  
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


def add_data(request):
    if request.method=='GET':
        return render(request,template_name='add_data.html')
    

@login_required
def add_data(request):
    if request.method == 'GET':
        return render(request,template_name='add_data.html')
    else:
        try:
            name = request.POST.get('name')
            aadhaar = request.POST.get('aadhaar')
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')
            document_f = request.FILES.get('photo') 
            uploaded_files_CDR = request.FILES.getlist('CDR')
            fs=FileSystemStorage()
            filename=fs.save(document_f.name,document_f)
            img_url=fs.url(filename)
        
            cdr_file_paths = []
            cdr_file_names = []
            for cdr_file in uploaded_files_CDR:
                filename_CDR = fs.save(cdr_file.name, cdr_file)
                cdr_file_paths.append(fs.url(filename_CDR))
                cdr_file_names.append(filename_CDR)

            cdr_files_path = ','.join(cdr_file_paths)
            cdr_files_name = ','.join(cdr_file_names)

            obj=Employee(name=name,aadhaar=aadhaar,mobile=mobile,address=address,
                     document_path=img_url,doct_file_name=filename,
                      cdr_files_name=cdr_files_name,
                      cdr_files_path=cdr_files_path
                     )
            obj.save()

            return render(request,template_name='add_data.html',context={'mess':'Data Saved'})  # Redirect to the view_data page after saving
        except Exception as ex:
            return render(request, 'add_data.html', {'error': ex})
        

def data(obj_list):
     processed_records = []
     for obj in obj_list:
        cdr_files_list = obj.cdr_files_path.split(',') if obj.cdr_files_path else []
        processed_records.append({
            'obj': obj,
            'cdr_files_list': cdr_files_list
        })
     return processed_records

@login_required
def data_display(request):
    obj_list = Employee.objects.all()
    records = data(obj_list)
    return render(request, 'display.html', {'processed_records':records})

# For Deleting the Record
@login_required
def Employee_Delete(request):
    if request.method=='GET':
        return render(request,template_name='Employee_delete.html')
    else:
        try:
            emp_sno=request.POST.get('sno')
            obj=Employee.objects.get(sno=emp_sno)
            obj.delete()
            return render(request,template_name='Employee_delete.html',context={'result':'Record Deleted Successfully'})
        except:
            return render(request,template_name='Employee_delete.html',context={'result':'This Serail Number does not Exist'})
        

#  For Updating the table recored
from django.shortcuts import render, get_object_or_404
@login_required
def Employee_update(request):
    try:
        emp_sno = request.POST.get('sno')
        
        obj = Employee.objects.get(sno=emp_sno)
        
        # Handle single document file
        document_f = request.FILES.get('photo')
        if document_f:
            fs = FileSystemStorage()
            filename = fs.save(document_f.name, document_f)
            img_url = fs.url(filename)
            obj.document_path = img_url
            obj.doct_file_name = filename
        
        # Handle multiple CDR files
        uploaded_files_CDR = request.FILES.getlist('CDR')
        if uploaded_files_CDR:
            cdr_file_paths = []
            cdr_file_names = []
            
            fs = FileSystemStorage()
            for cdr_file in uploaded_files_CDR:
                filename_CDR = fs.save(cdr_file.name, cdr_file)
                cdr_file_paths.append(fs.url(filename_CDR))
                cdr_file_names.append(filename_CDR)
            
            cdr_files_path = ','.join(cdr_file_paths)
            cdr_files_name = ','.join(cdr_file_names)
            
            obj.cdr_files_name = cdr_files_name
            obj.cdr_files_path = cdr_files_path
        else:
            if not obj.cdr_files_path:
                obj.cdr_files_path = ''  
            if not obj.cdr_files_name:
                obj.cdr_files_name = ''  
        
        obj.save()
        return render(request, 'Employee_update.html', {'result': 'Data Updated Successfully'})
    except Employee.DoesNotExist:
        return render(request, 'Employee_update.html', {'result': 'This Serial Number Does Not Exist'})
        


# For Delete the select row in the display.html

def delete_record(request):
    emp_sno=request.GET.get('empid')
    obj = Employee.objects.all()
    obj=Employee.objects.get(sno=emp_sno)
    obj.delete()
    obj = Employee.objects.all()
    record = data(obj)
    return render(request, 'display.html',{'processed_records': record})



# For Updating Selected Row 

def update_record(request):
    emp_sno=request.GET.get('empid')    
    obj=Employee.objects.filter(sno=emp_sno).values()
    return render(request,template_name='Update_emp.html',context={'Record':obj[0]})



# For Add CDR files on the Webpage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def add_more_files(request):
    if request.method == 'POST':
        emp_sno = request.POST.get('serial_number')
        employee = Employee.objects.get(sno=emp_sno)

        # Handle multiple CDR files
        uploaded_files_CDR = request.FILES.getlist('CDR')
        if uploaded_files_CDR:
            fs = FileSystemStorage()
            cdr_file_paths = employee.cdr_files_path.split(',') if employee.cdr_files_path else []
            cdr_file_names = employee.cdr_files_name.split(',') if employee.cdr_files_name else []
            
            for cdr_file in uploaded_files_CDR:
                filename_CDR = fs.save(cdr_file.name, cdr_file)
                cdr_file_paths.append(fs.url(filename_CDR))
                cdr_file_names.append(filename_CDR)
            
            # Update the employee record
            employee.cdr_files_path = ','.join(cdr_file_paths)
            employee.cdr_files_name = ','.join(cdr_file_names)
            employee.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# For DElete particular cdr file 

# def del_Prti_fl(request):
#     emp_sno=request.GET.get('sno')
#     emp_file=request.GET.get('file')
#     obj=Employee.objects.filter(sno=emp_sno,cdr_files_path=emp_file)
#     obj.delete()
#     obj.save()
#     return render(request,template_name='del_Prti_fl.html')
# views.py
# views.py
from django.shortcuts import render, redirect
from .models import Employee

def del_Prti_fl(request):
    if request.method == 'POST':
        emp_sno = request.POST.get('sno')
        emp_file = request.POST.get('file')

        if emp_sno and emp_file:
            try:
                obj = Employee.objects.get(sno=emp_sno, cdr_files_path=emp_file)
                if obj.exists():
                    obj.delete()
                    deleted = True
                else:
                    deleted = False
            except Exception as e:
                deleted = False
        else:
            deleted = False

        return redirect('del_Prti_fl')

    # For GET request, fetch all files
    emp_sno = request.GET.get('sno')
    files = []
    if emp_sno:
        files = Employee.objects.filter(sno=emp_sno).values_list('cdr_files_path', flat=True)
    
    return render(request, 'del_Prti_fl.html', {'files': files})









