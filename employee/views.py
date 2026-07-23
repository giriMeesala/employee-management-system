from .models import Employee
from .forms import EmployeeForm
import base64
import cv2
import numpy as np
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from employee.face.detector import detect_faces
#redirect() -> to send the user to another page after any operation done(you are in home page when you click add_employee it redirect to next page), this improves user experience
#(get_object_or_404) -> lets assume, we have only 5 employees when we try to update an employee at id = 6, it returns ("error 404 page not found")

# Create your views here.
@login_required
def home(request):

    total_employees = Employee.objects.count()

    total_departments = Employee.objects.values(
        "department"
    ).distinct().count()

    average_salary = Employee.objects.aggregate(
        Avg("salary")
    )["salary__avg"]

    recent_employees = Employee.objects.order_by(
        "-id"
    )[:5]

    context = {

        "total_employees": total_employees,

        "total_departments": total_departments,

        "average_salary": average_salary,

        "recent_employees": recent_employees,

    }

    return render(request, "home.html", context)



@login_required
def employee_list(request):

    search = request.GET.get("search")

    if search:
        employees = Employee.objects.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(department__icontains=search)
        )
    else:
        employees = Employee.objects.all()

    # Total employees (or search results)
    total_employees = employees.count()

    # Pagination
    paginator = Paginator(employees, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "employee_list.html", {
        "page_obj": page_obj,
        "total_employees": total_employees,
        "search": search,
    })



@login_required
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("employee_list")
        
    else:
        form = EmployeeForm()

    return render(request, "add_employee.html", {
        "form": form
    })



@login_required
def edit_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        form = EmployeeForm(request.POST, request.FILES, instance=employee)       #(instance=employee) -> Update Existing employee. without this it creates new employee

        if form.is_valid():
            form.save()
            return redirect("employee_list")

    else:
        form = EmployeeForm(instance=employee)

    return render(request, "edit_employee.html", {
        "form": form
    })



@login_required
def delete_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")

    return render(request, "delete_employee.html", {
        "employee": employee
    })



@login_required
def employee_details(request, id):

    employee = get_object_or_404(Employee, id=id)

    return render(request, "employee_details.html", {
        "employee": employee
    })



def login_user(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the user entered an email
        if "@" in username_or_email:

            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                username = username_or_email

        else:
            username = username_or_email

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)
            return redirect("home")

        else:

            messages.error(request, "Invalid username/email or password.")

    return render(request, "login.html")



@login_required
def dashboard(request):

    total_employees = Employee.objects.count()

    total_departments = Employee.objects.values(
        "department"
    ).distinct().count()

    average_salary = Employee.objects.aggregate(
        Avg("salary")
    )["salary__avg"]

    recent_employees = Employee.objects.order_by(
        "-id"
    )[:5]

    department_data = Employee.objects.values(
        "department"
    ).annotate(
        total=Count("id")
    )

    context = {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "average_salary": average_salary,
        "recent_employees": recent_employees,
        "department_data": department_data,
    }

    return render(request, "dashboard.html", context)


@login_required
def logout_user(request):

    logout(request)

    messages.success(request, "You have been logged out successfully.")

    return redirect("login")



@login_required
def register_face(request):
    return render(request, "face/register_face.html")



@csrf_exempt
@login_required
def receive_frame(request):

    if request.method == "POST":

        data = json.loads(request.body)

        image = data["image"]

        image = image.split(",")[1]

        image_bytes = base64.b64decode(image)

        np_array = np.frombuffer(
            image_bytes,
            np.uint8
        )

        frame = cv2.imdecode(
            np_array,
            cv2.IMREAD_COLOR
        )

        print("Before face detection")

        faces = detect_faces(frame)

        print("After face detection")

        print("Faces detected:", len(faces))

        cv2.imwrite(
            "media/last_frame.jpg",
            frame
        )

        return JsonResponse({

            "status": "success",

            "message": f"Faces detected: {len(faces)}"

        })

    return JsonResponse({

        "status": "error"

    })