
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import CreateProjectForm, CreateUserForm, LoginForm, CreateTaskForm, MessageForm, ProfileForm, UpdateProjectForm, UpdateTaskForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Project, Task, Profile
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Trang chủ
def home(request):
    return render(request, 'index.html')

# Đăng ký người dùng
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()
            profile = Profile.objects.create(user=current_user)
            messages.success(request, "User registration was successful!")
            return redirect('my_login')
    context = {'form': form}
    return render(request, 'register.html', context=context)

# Đăng nhập người dùng
def my_login(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("mypage")
            else:
                context = {'form': form, 'error': 'Invalid username or password'}
                return render(request, 'login.html', context)
        else:
            form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'my_login.html', context=context)

#- My page:
def mypage(request):
    return render(request, 'profile/mypage.html')

# Dashboard người dùng

@login_required(login_url='my_login')
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print(form.errors)  # In ra lỗi nếu form không hợp lệ
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'profile/dashboard.html', context=context)


# Quản lý hồ sơ người dùng
@login_required(login_url='my_login')
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)
    profile = Profile.objects.get(user=request.user)
    form_2 = UpdateProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        form_2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid():
            user_form.save()
            return redirect("dashboard")

        if form_2.is_valid():
            form_2.save()
            return redirect("dashboard")

    user_form = UpdateUserForm(instance=request.user)
    context = {'user_form': user_form, 'form_2': form_2 }
    return render(request, 'profile/profile_management.html', context=context)

# Xóa tài khoản người dùng
@login_required(login_url='my_login')
def deleteAccount(request):
    if request.method == 'POST':
        deleteUser = User.objects.get(username=request.user)
        deleteUser.delete()
        return redirect("")
    return render(request, 'profile/delete_account.html')

# Tạo task mới

@login_required(login_url='my_login')
def createTask(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user)
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, request.FILES, project=project)
        if form.is_valid():
            task_title = form.cleaned_data.get('title')
            task_content = form.cleaned_data.get('content')
            analysis = analyze_task_content(task_title, task_content)
            if "The content does not match the title" in analysis:
                # Display a warning with the AI's explanation and suggestion
                messages.warning(request, f"The task content may need improvement. {analysis}")
                return render(request, 'profile/create_task.html', {'form': form, 'project': project})
            else:
                # Save the task if the content is appropriate
                task = form.save(commit=False)
                task.project = project
                task.save()
                form.save_m2m()  # Save many-to-many data
                return redirect('view_tasks', project_id=project.id)
    else:
        form = CreateTaskForm(project=project)
    context = {'form': form, 'project': project}
    return render(request, 'profile/create_task.html', context)
# Xem tasks

@login_required(login_url='my_login')
def viewTasks(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user)
    
    # Lấy giá trị của priority và member từ request GET
    selected_priority = request.GET.get('priority', '')
    selected_member = request.GET.get('member', '')
    
    # Lọc tasks dựa trên priority và member được chọn
    tasks = Task.objects.filter(project=project)
    
    if selected_priority:
        tasks = tasks.filter(priority=selected_priority)
    
    if selected_member:
        tasks = tasks.filter(members__id=selected_member)
    
    # Chuẩn bị danh sách tasks cùng với các thành viên của chúng
    tasks_with_members = []
    for task in tasks:
        members = task.members.all()
        tasks_with_members.append({'task': task, 'members': members})
    
    # Lấy tất cả người dùng liên quan đến project hiện tại
    all_users = project.users.all()

    context = {
        'tasks_with_members': tasks_with_members,
        'selected_priority': selected_priority,
        'selected_member': selected_member,
        'all_users': all_users,
        'project': project,
    }
    
    return render(request, 'profile/view_tasks.html', context)
# Cập nhật task
"""
@login_required(login_url='my_login')
def updateTask(request, project_id, pk):
    project = get_object_or_404(Project, id=project_id, users=request.user)
    task = get_object_or_404(Task, id=pk, project=project)
    
    if request.method == 'POST':
        
        form = UpdateTaskForm(request.POST, instance=task, project=project)
        if form.is_valid():
            updated_task = form.save(commit=False)
            updated_task.save()
            form.save_m2m()  # Lưu các quan hệ Many-to-Many như members
            return redirect('view_tasks', project_id=project.id)
    else:
        form = UpdateTaskForm(instance=task, project=project)
    
    context = {'form': form, 'project': project}
    return render(request, 'profile/update_task.html', context=context)
"""
@login_required(login_url='my_login')
def updateTask(request, project_id, pk):
    project = get_object_or_404(Project, id=project_id, users=request.user)
    task = get_object_or_404(Task, id=pk, project=project)

    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, request.FILES, instance=task, project=project)
        if form.is_valid():
            task_title = form.cleaned_data.get('title')
            task_content = form.cleaned_data.get('content')
            analysis = analyze_task_content(task_title, task_content)

            if "The content does not match the title" in analysis:
                # Display a warning with the AI's explanation and suggestion
                messages.warning(request, f"The task content may need improvement. {analysis}")
                return render(request, 'profile/update_task.html', {'form': form, 'project': project})
            else:
                # Save the task if the content is appropriate
                updated_task = form.save(commit=False)
                updated_task.save()
                form.save_m2m()  # Save many-to-many data if applicable
                return redirect('view_tasks', project_id=project.id)
        else:
            # Handle form errors if the form is not valid
            messages.error(request, "Please correct the errors below.")
    else:
        form = UpdateTaskForm(instance=task, project=project)

    context = {'form': form, 'project': project}
    return render(request, 'profile/update_task.html', context)
# Xóa task
@login_required(login_url='my_login')
def deleteTask(request, project_id, pk):
    project = get_object_or_404(Project, id=project_id, users=request.user)
    task = get_object_or_404(Task, id=pk, project=project)
    if request.method == 'POST':
        task.delete()
        return redirect('view_tasks', project_id=project.id)
    context = {'task': task, 'project': project}
    return render(request, 'profile/delete_task.html', context)

# Đăng xuất người dùng
def user_logout(request):
    auth.logout(request)
    return redirect("")

# Trang quản lý dự án
@login_required(login_url='my_login')
def projects(request):
    return render(request, 'profile/view_projects.html')

# Tạo dự án mới
@login_required(login_url='my_login')
def createProject(request):
    form = CreateProjectForm()
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            form.save_m2m()
            project.users.add(request.user)
            return redirect('view_projects')
    context = {'form': form}
    return render(request, 'profile/create_project.html', context)

# Xem dự án
@login_required(login_url='my_login')
def viewProjects(request):
    projects = Project.objects.filter(users=request.user)
    context = {'projects': projects}
    return render(request, 'profile/view_projects.html', context)

# Cập nhật dự án
@login_required(login_url='my_login')
def updateProject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = UpdateProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('view_projects')
    else:
        form = UpdateProjectForm(instance=project)
    context = {
        'form': form,
        'project': project
    }
    return render(request, 'profile/update_project.html', context)

# Xóa dự án
@login_required(login_url='my_login')
def deleteProject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('view_projects')
    context = {'project': project}
    return render(request, 'profile/delete_project.html', context)

# Xem hồ sơ người dùng
@login_required
def view_user_dashboard(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    context = {
        'profile': profile
    }
    return render(request, 'profile/view_dashboard.html', context)


#- Group chat
def project_chat(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user)
    messages = project.messages.all().order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.project = project
            message.user = request.user
            message.save()
            return redirect('project_chat', project_id=project.id)
    else:
        form = MessageForm()

    context = {
        'project': project,
        'messages': messages,
        'form': form,
    }
    return render(request, 'profile/project_chat.html', context)



#============================================================================================================================

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Task
from .ai_utils import analyze_task_content, summarize_text  

@login_required(login_url='my_login')
def explain_task_content(request, project_id, task_id):
    task = get_object_or_404(Task, id=task_id, project_id=project_id)
    explanation = summarize_text(task.content)  

    return JsonResponse({'explanation': explanation})



