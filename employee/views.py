from .models import Employee
from .forms import EmployeeForm
from django.shortcuts import render, redirect, get_object_or_404
#redirect() -> to send the user to another page after any operation done(you are in home page when you click add_employee it redirect to next page), this improves user experience
#(get_object_or_404) -> lets assume, we have only 5 employees when we try to update an employee at id = 6, it returns ("error 404 page not found")

# Create your views here.
def home(request):
    return render(request, "home.html")

def employee_list(request):
    employees = Employee.objects.all()

    return render(request, "employee_list.html", {
        "employees" : employees
    })



def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("employee_list")
        
    else:
        form = EmployeeForm()

    return render(request, "add_employee.html", {
        "form": form
    })



def edit_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        form = EmployeeForm(request.POST, instance=employee)       #(instance=employee) -> Update Existing employee. without this it creates new employee

        if form.is_valid():
            form.save()
            return redirect("employee_list")

    else:
        form = EmployeeForm(instance=employee)

    return render(request, "edit_employee.html", {
        "form": form
    })