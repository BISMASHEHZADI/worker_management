from django.shortcuts import render, redirect
from decimal import Decimal
from .models import Worker, SalaryIncrement

def home(request):
    return render(request, 'home.html')

def workers(request):
    return render(request, 'home.html')

def tasks(request):
    return render(request, 'home.html')

def reports(request):
    return render(request, 'home.html')

def worker_entry(request):
    workers_list = Worker.objects.all()
    error_message = None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        cnic = request.POST.get('cnic')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gross_salary = request.POST.get('gross_salary')
        date_of_joining = request.POST.get('date_of_joining')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        photo = request.FILES.get('photo')
        
        # Check if CNIC already exists
        if Worker.objects.filter(cnic=cnic).exists():
            error_message = 'A worker with this CNIC already exists in the system.'
        else:
            worker = Worker(
                name=name,
                father_name=father_name,
                cnic=cnic,
                phone_number=phone_number,
                address=address,
                gross_salary=gross_salary,
                date_of_joining=date_of_joining,
                department=department,
                designation=designation,
                photo=photo
            )
            worker.save()
            return redirect('worker_entry')
    
    return render(request, 'worker_entry.html', {'workers': workers_list, 'error_message': error_message})

def find_worker(request):
    query = request.GET.get('q', '')
    workers = []
    
    if query:
        workers = Worker.objects.filter(
            name__icontains=query
        ) | Worker.objects.filter(
            father_name__icontains=query
        ) | Worker.objects.filter(
            cnic__icontains=query
        ) | Worker.objects.filter(
            phone_number__icontains=query
        ) | Worker.objects.filter(
            address__icontains=query
        ) | Worker.objects.filter(
            department__icontains=query
        ) | Worker.objects.filter(
            designation__icontains=query
        )
    
    return render(request, 'find_worker.html', {'workers': workers, 'query': query})

def worker_detail(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    increments = worker.increments.all().order_by('-year')
    return render(request, 'worker_detail.html', {'worker': worker, 'increments': increments})

def case_manager(request):
    workers_list = Worker.objects.all()
    return render(request, 'case_manager.html', {'workers': workers_list})

def worker_edit(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    error_message = None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        cnic = request.POST.get('cnic')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gross_salary = request.POST.get('gross_salary')
        date_of_joining = request.POST.get('date_of_joining')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        photo = request.FILES.get('photo')
        
        # Check if CNIC already exists (excluding current worker)
        if Worker.objects.filter(cnic=cnic).exclude(id=worker_id).exists():
            error_message = 'A worker with this CNIC already exists in the system.'
        else:
            worker.name = name
            worker.father_name = father_name
            worker.cnic = cnic
            worker.phone_number = phone_number
            worker.address = address
            worker.gross_salary = gross_salary
            worker.date_of_joining = date_of_joining
            worker.department = department
            worker.designation = designation
            if photo:
                worker.photo = photo
            worker.save()
            return redirect('case_manager')
    
    return render(request, 'worker_entry.html', {'worker': worker, 'error_message': error_message, 'is_edit': True})

def worker_delete(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    if request.method == 'POST':
        worker.delete()
        return redirect('case_manager')
    return render(request, 'worker_delete.html', {'worker': worker})

def salary_increment(request):
    workers = Worker.objects.all()
    recent_increments = SalaryIncrement.objects.all().order_by('-created_at')[:10]
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        worker_id = request.POST.get('worker')
        year = request.POST.get('year')
        increment_amount = request.POST.get('increment_amount')
        
        if not worker_id or not year or not increment_amount:
            error_message = 'Please fill all fields.'
        else:
            worker = Worker.objects.get(id=worker_id)
            
            # Create salary increment
            SalaryIncrement.objects.create(
                worker=worker,
                year=year,
                increment_amount=increment_amount
            )
            
            # Update worker's gross salary
            worker.gross_salary += Decimal(increment_amount)
            worker.save()
            
            success_message = f'Increment of PKR {increment_amount} added for {worker.name} in year {year}.'
    
    return render(request, 'salary_increment.html', {
        'workers': workers,
        'recent_increments': recent_increments,
        'error_message': error_message,
        'success_message': success_message
    })
