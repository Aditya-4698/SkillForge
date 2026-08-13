from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.db.models import Avg, Count, Q
from django.contrib import messages
from .models import Skill,Goal, Project, Milestone, Activity, GoalTask, Roadmap, RoadmapStep, Challenge, Note, Profile
from datetime import date
from django.utils import timezone
from .forms import SkillForm, GoalForm, ProjectForm, MilestoneForm, GoalTaskForm, SignupForm, LoginForm, RoadmapForm, RoadmapStepForm, ChallengeForm, NoteForm, ProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):

    # ==============================
    # USER DATA
    # ==============================

    skills = Skill.objects.filter(
        user=request.user
    )

    goals = Goal.objects.filter(
        skill__user=request.user
    )

    tasks = GoalTask.objects.filter(
        goal__skill__user=request.user
    )

    all_projects = Project.objects.filter(
        skill__user=request.user
    )

    pending_tasks_list = GoalTask.objects.filter(
        goal__skill__user=request.user,completed=False
    ).order_by("-created_at")[:5]

    recent_completed_tasks = GoalTask.objects.filter(
        goal__skill__user=request.user,completed=True
    ).order_by("-completed_at")[:5]


    # ==============================
    # LATEST PROJECTS
    # ==============================

    projects = all_projects.order_by(
        "-created_at"
    )[:4]


    # ==============================
    # RECENT ACTIVITIES
    # ==============================

    activities = Activity.objects.filter(
        Q(project__skill__user=request.user) |
        Q(roadmap__skill__user=request.user) |
        Q(challenge__skill__user=request.user) |
        Q(note__user=request.user)
    ).select_related(
        "project",
        "roadmap",
        "challenge",
        "note"
    ).order_by(
        "-created_at"
    )[:4]


    # ==============================
    # SKILLS
    # ==============================

    total_skills = skills.count()


    # Most Active Skill

    most_active_skill = (
        skills
        .annotate(
            project_count=Count("projects")
        )
        .order_by(
            "-project_count",
            "-progress"
        )
        .first()
    )


    # Average Skill Progress

    if total_skills > 0:

        average_progress = sum(
            skill.progress
            for skill in skills
        ) / total_skills

    else:

        average_progress = 0


    # ==============================
    # GOALS
    # ==============================

    total_goals = goals.count()


    completed_goals = goals.filter(
        completed=True
    ).count()


    active_goals = goals.filter(
        completed=False
    ).count()


    # ==============================
    # GOAL STATUS
    # ==============================

    overdue_goals = 0

    deadline_soon_goals = 0

    on_track_goals = 0


    for goal in goals:

        if goal.status == "Overdue":

            overdue_goals += 1

        elif goal.status == "Deadline Soon":

            deadline_soon_goals += 1

        elif goal.status == "On Track":

            on_track_goals += 1


    # ==============================
    # TASKS
    # ==============================

    total_tasks = tasks.count()


    completed_tasks = tasks.filter(
        completed=True
    ).count()


    pending_tasks = tasks.filter(
        completed=False
    ).count()


    # ==============================
    # RECENT TASKS
    # ==============================

    recent_tasks = (
        tasks
        .select_related("goal")
        .order_by("-created_at")[:5]
    )


    # ==============================
    # TASK PROGRESS
    # ==============================

    if total_tasks > 0:

        task_progress = round(
            (
                completed_tasks /
                total_tasks
            ) * 100
        )

    else:

        task_progress = 0


    # ==============================
    # PROJECTS
    # ==============================

    total_projects = all_projects.count()


    completed_projects = all_projects.filter(
        progress=100
    ).count()


    in_progress_projects = all_projects.filter(
        progress__lt=100
    ).count()


    # ==============================
    # OVERDUE PROJECTS
    # ==============================

    overdue_projects = sum(
        1
        for project in all_projects
        if project.is_overdue
    )


    # ==============================
    # RENDER DASHBOARD
    # ==============================

    return render(
        request,
        "skills/dashboard.html",
        {

            # ==========================
            # SKILLS
            # ==========================

            "skills":
                skills,

            "total_skills":
                total_skills,

            "most_active_skill":
                most_active_skill,

            "average_progress":
                round(
                    average_progress
                ),


            # ==========================
            # GOALS
            # ==========================

            "goals":
                goals,

            "total_goals":
                total_goals,

            "completed_goals":
                completed_goals,

            "active_goals":
                active_goals,

            "overdue_goals":
                overdue_goals,

            "deadline_soon_goals":
                deadline_soon_goals,

            "on_track_goals":
                on_track_goals,


            # ==========================
            # TASKS
            # ==========================

            "tasks":
                tasks,

            "recent_tasks":
                recent_tasks,

            "total_tasks":
                total_tasks,

            "completed_tasks":
                completed_tasks,

            "pending_tasks":
                pending_tasks,

            "task_progress":
                task_progress,


            # ==========================
            # PROJECTS
            # ==========================

            "projects":
                projects,

            "total_projects":
                total_projects,

            "completed_projects":
                completed_projects,

            "in_progress_projects":
                in_progress_projects,

            "overdue_projects":
                overdue_projects,


            # ==========================
            # ACTIVITIES
            # ==========================

            "activities":
                activities,

            "pending_tasks_list": pending_tasks_list,

            "recent_completed_tasks": recent_completed_tasks,

        }
    )



def signup(request):

    if request.method == "POST":

        form = SignupForm(
            request.POST
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                "Account Added Successfully!"
            )

            return redirect(
                "home"
            )

    else:

        form = SignupForm()


    return render(
        request,
        "skills/signup.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        form = LoginForm(
            request.POST
        )

        if form.is_valid():

            user = form.cleaned_data["user"]

            login(
                request,
                user
            )

            messages.success(
                request,
                "Welcome Back!"
            )

            return redirect(
                "home"
            )

    else:

        form = LoginForm()


    return render(
        request,
        "skills/login.html",
        {
            "form": form
        }
    )

def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out sussessfully!"
    )

    return redirect(
        "login"
    )


@login_required
def goals(request):

    goals = list(
        Goal.objects.filter(
            skill__user=request.user
        ).select_related("skill")
    )

    status_filter = request.GET.get(
        "status",
        "all"
    )

    sort = request.GET.get(
        "sort",
        "latest"
    )

    #----------
    # STATUS FILTER
    #____________

    if status_filter == "completed":

        goals = [
            goal 
            for goal in goals
            if goal.completed
        ]

    elif status_filter == "active":

        goals = [
            goal
            for goal in goals
            if not goal.completed
        ]

    elif status_filter == "overdue":

        goals = [
            goal 
            for goal in goals
            if goal.status == "Overdue"
        ]

    elif status_filter == "soon":

        goals = [
            goal
            for goal in goals
            if goal.status == "Deadline Soon"
        ]

    #--------------
    #Sort
    #--------------

    if sort == "progress":

        goals.sort(
            key=lambda goal:
                goal.current_progress,
            reverse=True
        )

    elif sort == "deadline":

        goals.sort(
            key=lambda goal:
                goal.deadline
                if goal.deadline
                else date.max
        )

    else:

        goals.sort(
            key=lambda goal:
                goal.created_at,
            reverse=True
        )

    return render(
        request,
        "skills/goals.html",
        {
            "goals":goals,
            "current_status":status_filter,
            "current_sort": sort,
        }
    )

@login_required
def skills_home(request):

    skills = Skill.objects.filter(
        user=request.user
    )

    total_skills = skills.count()

    avergae_progress = skills.aggregate(
        Avg("progress")
    )["progress__avg"]

    advanced_skills = skills.filter(
        level = "Advanced"
    ).count()

    learning_skills = skills.exclude(
        level="Advanced"
    ).count()

    if avergae_progress is None:
        avergae_progress = 0

    return render(
        request, "skills/skills_home.html",
        {
            "skills":skills,
            "total_skills": total_skills,
            "average_progress": round(
                avergae_progress
            ),
            "advanced_skills":advanced_skills,
            "learning_skills":learning_skills
        }
    )


@login_required
def add_skill(request):

    if request.method == "POST":

        form = SkillForm(request.POST)

        if form.is_valid():

            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()

            messages.success(
                request,
                "Skill added successfully!"
            )

            return redirect("skills_home")

    else:

        form = SkillForm()

    return render(
        request,
        "skills/add_skill.html",
        {
            "form": form
        }
    )


@login_required
def edit_skill(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    if request.method == "POST":

        form = SkillForm(
            request.POST,
            instance=skill
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Skill updated successfully!"
            )

            return redirect("skills_home")

    else:

        form = SkillForm(
            instance=skill
        )

    return render(
        request,
        "skills/edit_skill.html",
        {
            "form": form,
            "skill": skill
        }
    )


@login_required
def delete_skill(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    skill.delete()

    messages.success(
        request,
        "Skill deleted successfully"
    )

    return redirect("skills_home")


@login_required
def skill_detail(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    return render(
        request,
        "skills/skill_detail.html",
        {
            "skill": skill
        }
    )


@login_required
def add_goal(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    if request.method == "POST":

        form = GoalForm(request.POST)

        if form.is_valid():

            goal = form.save(commit=False)
            goal.skill = skill
            goal.save()

            messages.success(
                request,
                "Learning Goal added successfully!"
            )

            return redirect(
                "skill_detail",
                skill_id=skill.id
            )

    else:

        form = GoalForm()

    return render(
        request,
        "skills/add_goal.html",
        {
            "form": form,
            "skill": skill,
        }
    )


@login_required
def edit_goal(request, skill_id, goal_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    goal = get_object_or_404(
        Goal,
        id=goal_id,
        skill=skill
    )

    if request.method == "POST":

        form = GoalForm(
            request.POST,
            instance=goal
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Learning goal updated successfully!"
            )

            return redirect(
                "skill_detail",
                skill_id=skill.id
            )

    else:

        form = GoalForm(
            instance=goal
        )

    return render(
        request,
        "skills/edit_goal.html",
        {
            "form": form,
            "skill": skill,
            "goal": goal
        }
    )


@login_required
def delete_goal(request, skill_id, goal_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    goal = get_object_or_404(
        Goal,
        id=goal_id,
        skill=skill
    )

    goal.delete()

    messages.success(
        request,
        "Learning Goal Deleted Successfully!"
    )

    return redirect(
        "skill_detail",
        skill_id=skill_id
    )


@login_required
def complete_goal(request, skill_id, goal_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    goal = get_object_or_404(
        Goal,
        id=goal_id,
        skill=skill
    )

    goal.completed = True
    goal.save()

    messages.success(
        request,
        "Learning Goal Completed 🥳"
    )

    return redirect(
        "skill_detail",
        skill_id=skill_id
    )

@login_required
def undo_goal(request, skill_id, goal_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    goal = get_object_or_404(
        Goal,
        id=goal_id,
        skill=skill
    )

    goal.completed = False
    goal.save()

    goal.update_progress()
    goal.skill.update_progress()

    messages.success(
        request,
        "Learning Goal marked as pending."
    )

    return redirect("goals")



@login_required
def projects(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    )

    skill_id = request.GET.get(
        "skill",
        ""
    )


    projects = Project.objects.filter(
        skill__user=request.user
    ).select_related(
        "skill"
    )


    if search:

        projects = projects.filter(
            title__icontains=search
        )


    if status:

        projects = projects.filter(
            status=status
        )


    if skill_id:

        projects = projects.filter(
            skill_id=skill_id
        )


    skills = Skill.objects.filter(
        user=request.user
    )


    return render(
        request,
        "skills/projects.html",
        {
            "projects": projects,
            "skills": skills,
            "search": search,
            "selected_status": status,
            "selected_skill": skill_id,
        }
    )


@login_required
def add_project(request):

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            project = form.save(
                commit=False
            )

            if project.skill.user != request.user:

                form.add_error(
                    "skill",
                    "You cannot select this skill."
                )

            else:

                project.save()

                Activity.objects.create(
                    project=project,
                    activity_type="PROJECT_CREATED",
                    message=f"Project '{project.title}' was created."
                )

                messages.success(
                    request,
                    "Project Added Successfully!"
                )

                return redirect(
                    "projects"
                )

    else:

        form = ProjectForm(
            user=request.user
        )

    return render(
        request,
        "skills/add_project.html",
        {
            "form": form
        }
    )


@login_required
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    return render(
        request,
        "skills/project_detail.html",
        {
            "project":project
        }
    )


@login_required
def edit_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project,
            user=request.user
        )

        if form.is_valid():

            updated_project = form.save(
                commit=False
            )

            if updated_project.skill.user != request.user:

                form.add_error(
                    "skill",
                    "You cannot select this skill."
                )

            else:

                updated_project.save()

                Activity.objects.create(
                    project=updated_project,
                    activity_type="PROJECT_UPDATED",
                    message=f"Project '{project.title}' was updated."
                )

                messages.success(
                    request,
                    "Project Updated Successfully!"
                )

                return redirect(
                    "project_detail",
                    project_id=project.id
                )

    else:

        form = ProjectForm(
            instance=project,
            user=request.user
        )

    return render(
        request,
        "skills/edit_project.html",
        {
            "form": form,
            "project": project,
        }
    )


@login_required
def delete_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    if request.method == "POST":
        project.delete()

        messages.success(
            request,
            "Project Deleted Successfully!"
        )

        return redirect(
            "projects"
        )

    return render(
        request,
        "skills/delete_project.html",
        {
            "project":project
        }
    )



@login_required
def add_milestone(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    if request.method == "POST":

        form = MilestoneForm(
            request.POST
        )

        if form.is_valid():

            milestone = form.save(
                commit=False
            )

            milestone.project = project

            milestone.save()

            Activity.objects.create(
                project=project,
                activity_type="MILESTONE_CREATED",
                message=f"Milestone '{milestone.title}' was added."
            )

            messages.success(
                request,
                "MileStone Added Successfully🥳🎉"
            )

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:

        form = MilestoneForm()


    return render(
        request,
        "skills/add_milestone.html",
        {
            "form": form,
            "project": project,
        }
    )


@login_required
def complete_milestone(request, project_id, milestone_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    milestone = get_object_or_404(
        Milestone,
        id=milestone_id,
        project=project
    )

    if request.method == "POST":

        milestone.completed = True
        milestone.completed_at = timezone.now()
        milestone.save()

        project.update_progress()

        Activity.objects.create(
            project=project,
            activity_type="MILESTONE_COMPLETED",
            message=f"Milestone '{milestone.title}' was completed."
        )

        return redirect(
            "project_detail",
            project_id=project.id
        )

    return redirect(
        "project_detail",
        project_id=project.id
    )


@login_required
def undo_milestone(request, project_id, milestone_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    milestone = get_object_or_404(
        Milestone,
        id=milestone_id,
        project=project
    )

    if request.method == "POST":

        milestone.completed = False
        milestone.completed_at = None
        milestone.save()

        project.update_progress()

        Activity.objects.create(
            project=project,
            activity_type="MILESTONE_UNDONE",
            message=f"Milestone '{milestone.title}' was marked as pending."
        )

    return redirect(
        "project_detail",
        project_id=project.id
    )


@login_required
def edit_milestone(request, project_id, milestone_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    milestone = get_object_or_404(
        Milestone,
        id=milestone_id,
        project=project
    )

    if request.method == "POST":

        form = MilestoneForm(
            request.POST,
            instance=milestone
        )

        if form.is_valid():

            form.save()

            Activity.objects.create(
                project=project,
                activity_type="MILESTONE_UPDATED",
                message=f"Milestone '{milestone.title}' was updated."
            )

            messages.success(
                request,
                "Milestone Updated Successfully!"
            )

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:

        form = MilestoneForm(
            instance=milestone
        )

    return render(
        request,
        "skills/edit_milestone.html",
        {
            "form": form,
            "project": project,
            "milestone": milestone,
        }
    )


@login_required
def delete_milestone(request, project_id, milestone_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        skill__user=request.user
    )

    milestone = get_object_or_404(
        Milestone,
        id=milestone_id,
        project=project
    )

    if request.method == "POST":

        milestone_title = milestone.title

        milestone.delete()

        Activity.objects.create(
            project=project,
            activity_type="MILESTONE_DELETED",
            message=f"Milestone '{milestone_title}' was deleted."
        )

        project.update_progress()

        messages.success(
            request,
            "Milestone Deleted Successfully!"
        )

        return redirect(
            "project_detail",
            project_id=project.id
        )

    return render(
        request,
        "skills/delete_milestone.html",
        {
            "project": project,
            "milestone": milestone,
        }
    )


@login_required
def goal_detail(request, goal_id):

    goal = get_object_or_404(
        Goal,
        id=goal_id,
        skill__user=request.user
    )

    return render(
        request,
        "skills/goal_detail.html",
        {
            "goal": goal
        }
    )

@login_required
def add_goal_task(request, goal_id):

    goal = get_object_or_404(
        Goal,
        id=goal_id,
        skill__user=request.user
    )

    if request.method == "POST":

        form = GoalTaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)
            task.goal = goal
            task.save()

            goal.update_progress()
            goal.skill.update_progress()

            messages.success(
                request,
                "Task added successfully!"
            )

            return redirect(
                "goal_detail",
                goal_id=goal.id
            )

    else:

        form = GoalTaskForm()

    return render(
        request,
        "skills/add_goal_task.html",
        {
            "form": form,
            "goal": goal,
        }
    )


@login_required
def toggle_goal_task(request, task_id):

    task = get_object_or_404(
        GoalTask,
        id=task_id,
        goal__skill__user=request.user
    )

    if request.method == "POST":

        if task.completed:
            # UNDO
            task.completed = False
            task.completed_at = None

            messages.success(
                request,
                "Task marked as pending."
            )

        else:
            # COMPLETE
            task.completed = True
            task.completed_at = timezone.now()

            messages.success(
                request,
                "Task completed successfully! 🎉"
            )

        task.save()

        # Update goal progress
        task.goal.update_progress()

        # Update skill progress
        task.goal.skill.update_progress()

    return redirect(
        "goal_detail",
        goal_id=task.goal.id
    )


@login_required
def edit_goal_task(request, task_id):

    task = get_object_or_404(
        GoalTask,
        id=task_id,
        goal__skill__user=request.user
    )

    if request.method == "POST":

        form = GoalTaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            task.goal.update_progress()
            task.goal.skill.update_progress()

            messages.success(
                request,
                "Task updated successfully!"
            )

            return redirect(
                "goal_detail",
                goal_id=task.goal.id
            )

    else:

        form = GoalTaskForm(
            instance=task
        )

    return render(
        request,
        "skills/edit_goal_task.html",
        {
            "form": form,
            "task": task,
            "goal": task.goal,
        }
    )


@login_required
def delete_goal_task(request, task_id):

    task = get_object_or_404(
        GoalTask,
        id=task_id,
        goal__skill__user=request.user
    )

    goal_id = task.goal.id

    if request.method == "POST":

        goal=task.goal
        task.delete()
        goal.update_progress()

        messages.success(
            request,
            "Task deleted successfully!"
        )

        return redirect(
            "goal_detail",
            goal_id=goal_id
        )

    return render(
        request,
        "skills/delete_goal_task.html",
        {
            "task": task,
            "goal": task.goal,
        }
    )


@login_required
def complete_task(request, skill_id, goal_id, task_id):

    task = get_object_or_404(
        GoalTask,
        id=task_id,
        goal_id=goal_id,
        goal__skill_id=skill_id,
        goal__skill__user=request.user
    )

    task.completed = True
    task.completed_at = timezone.now()
    task.save()

    task.goal.update_progress()
    task.goal.skill.update_progress()

    messages.success(
        request,
        "Task completed successfully! 🎉"
    )

    return redirect("tasks")


@login_required
def undo_task(request, skill_id, goal_id, task_id):

    task = get_object_or_404(
        GoalTask,
        id=task_id,
        goal_id=goal_id,
        goal__skill_id=skill_id,
        goal__skill__user=request.user
    )

    task.completed = False
    task.completed_at = None
    task.save()

    task.goal.update_progress()
    task.goal.skill.update_progress()

    messages.success(
        request,
        "Task marked as pending."
    )

    return redirect("tasks")


@login_required
def edit_task(request, skill_id, goal_id, task_id):

    task = get_object_or_404(
        GoalTask,
        id=task_id,
        goal_id=goal_id,
        goal__skill_id=skill_id,
        goal__skill__user=request.user
    )

    if request.method == "POST":

        form = GoalTaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            task.goal.update_progress()
            task.goal.skill.update_progress()

            messages.success(
                request,
                "Task updated successfully!"
            )

            return redirect("tasks")

    else:

        form = GoalTaskForm(
            instance=task
        )

    return render(
        request,
        "skills/edit_goal_task.html",
        {
            "form": form,
            "task": task,
            "goal": task.goal,
        }
    )



@login_required
def delete_task(request, skill_id, goal_id, task_id):

    task = get_object_or_404(
        GoalTask,
        id=task_id,
        goal_id=goal_id,
        goal__skill_id=skill_id,
        goal__skill__user=request.user
    )

    if request.method == "POST":

        goal = task.goal

        task.delete()

        goal.update_progress()
        goal.skill.update_progress()

        messages.success(
            request,
            "Task deleted successfully!"
        )

        return redirect("tasks")

    return render(
        request,
        "skills/delete_goal_task.html",
        {
            "task": task,
            "goal": task.goal,
        }
    )


@login_required
def add_task(request, skill_id, goal_id):
    return add_goal_task(request, goal_id)

@login_required
def tasks(request):

    # ==========================================
    # ALL USER TASKS
    # ==========================================

    all_tasks = GoalTask.objects.filter(
        goal__skill__user=request.user
    ).select_related(
        "goal",
        "goal__skill"
    )


    # ==========================================
    # SEARCH
    # ==========================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    tasks = all_tasks

    if search:

        tasks = tasks.filter(
            title__icontains=search
        )


    # ==========================================
    # STATUS FILTER
    # ==========================================

    current_status = request.GET.get(
        "status",
        "all"
    )

    if current_status == "pending":

        tasks = tasks.filter(
            completed=False
        )

    elif current_status == "completed":

        tasks = tasks.filter(
            completed=True
        )


    # ==========================================
    # SORT
    # ==========================================

    current_sort = request.GET.get(
        "sort",
        "latest"
    )

    if current_sort == "oldest":

        tasks = tasks.order_by(
            "created_at"
        )

    elif current_sort == "completed":

        tasks = tasks.order_by(
            "-completed",
            "-created_at"
        )

    elif current_sort == "pending":

        tasks = tasks.order_by(
            "completed",
            "-created_at"
        )

    else:

        tasks = tasks.order_by(
            "-created_at"
        )


    # ==========================================
    # STATISTICS
    # ==========================================

    total_tasks = all_tasks.count()

    completed_tasks = all_tasks.filter(
        completed=True
    ).count()

    pending_tasks = all_tasks.filter(
        completed=False
    ).count()


    # ==========================================
    # RENDER
    # ==========================================

    return render(
        request,
        "skills/tasks.html",
        {
            "tasks": tasks,

            "total_tasks":
                total_tasks,

            "completed_tasks":
                completed_tasks,

            "pending_tasks":
                pending_tasks,

            "current_status":
                current_status,

            "current_sort":
                current_sort,

            "search":
                search,
        }
    )



@login_required
def roadmaps(request):

    roadmaps = Roadmap.objects.filter(
        skill__user=request.user
    ).select_related(
        "skill"
    )

    return render(
        request,
        "skills/roadmaps.html",
        {
            "roadmaps": roadmaps
        }
    )


@login_required
def add_roadmap(request):

    if request.method == "POST":

        form = RoadmapForm(
            request.POST
        )

        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

        if form.is_valid():

            roadmap = form.save(
                commit=False
            )

            if roadmap.skill.user != request.user:

                form.add_error(
                    "skill",
                    "You cannot select this skill."
                )

            else:

                roadmap.save()

                # ==============================
                # CREATE ACTIVITY
                # ==============================

                Activity.objects.create(
                    roadmap=roadmap,
                    activity_type="ROADMAP_CREATED",
                    message=f'Roadmap "{roadmap.title}" was created.'
                )

                messages.success(
                    request,
                    "Roadmap added successfully!"
                )

                return redirect(
                    "roadmaps"
                )

    else:

        form = RoadmapForm()

        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

    return render(
        request,
        "skills/add_roadmap.html",
        {
            "form": form
        }
    )


@login_required
def roadmap_detail(request, roadmap_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    return render(
        request,
        "skills/roadmap_detail.html",
        {
            "roadmap": roadmap
        }
    )


@login_required
def edit_roadmap(request, roadmap_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    if request.method == "POST":

        form = RoadmapForm(
            request.POST,
            instance=roadmap
        )

        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

        if form.is_valid():

            updated_roadmap = form.save(
                commit=False
            )

            if updated_roadmap.skill.user != request.user:

                form.add_error(
                    "skill",
                    "You cannot select this skill."
                )

            else:

                updated_roadmap.save()

                # ==============================
                # CREATE ACTIVITY
                # ==============================

                Activity.objects.create(
                    roadmap=updated_roadmap,
                    activity_type="ROADMAP_UPDATED",
                    message=f'Roadmap "{updated_roadmap.title}" was updated.'
                )

                messages.success(
                    request,
                    "Roadmap updated successfully!"
                )

                return redirect(
                    "roadmap_detail",
                    roadmap_id=roadmap.id
                )

    else:

        form = RoadmapForm(
            instance=roadmap
        )

        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

    return render(
        request,
        "skills/edit_roadmap.html",
        {
            "form": form,
            "roadmap": roadmap
        }
    )


@login_required
def delete_roadmap(request, roadmap_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    if request.method == "POST":

        roadmap.delete()

        messages.success(
            request,
            "Roadmap deleted successfully!"
        )

        return redirect(
            "roadmaps"
        )

    return render(
        request,
        "skills/delete_roadmap.html",
        {
            "roadmap": roadmap
        }
    )


@login_required
def add_roadmap_step(request, roadmap_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    if request.method == "POST":

        form = RoadmapStepForm(
            request.POST
        )

        if form.is_valid():

            step = form.save(
                commit=False
            )

            step.roadmap = roadmap
            step.save()

            Activity.objects.create(
                roadmap=roadmap,
                activity_type="ROADMAP_STEP_CREATED",
                message=f'Roadmap step "{step.title}" was added to "{roadmap.title}".'
            )

            messages.success(
                request,
                "Roadmap step added successfully!"
            )

            return redirect(
                "roadmap_detail",
                roadmap_id=roadmap.id
            )

    else:

        form = RoadmapStepForm()

    return render(
        request,
        "skills/add_roadmap_step.html",
        {
            "form": form,
            "roadmap": roadmap,
        }
    )



@login_required
def edit_roadmap_step(request, roadmap_id, step_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    step = get_object_or_404(
        RoadmapStep,
        id=step_id,
        roadmap=roadmap
    )

    if request.method == "POST":

        form = RoadmapStepForm(
            request.POST,
            instance=step
        )

        if form.is_valid():

            updated_step = form.save()

            Activity.objects.create(
                roadmap=roadmap,
                activity_type="ROADMAP_STEP_UPDATED",
                message=f'Roadmap step "{updated_step.title}" was updated in "{roadmap.title}".'
            )

            messages.success(
                request,
                "Roadmap step updated successfully!"
            )

            return redirect(
                "roadmap_detail",
                roadmap_id=roadmap.id
            )

    else:

        form = RoadmapStepForm(
            instance=step
        )

    return render(
        request,
        "skills/edit_roadmap_step.html",
        {
            "form": form,
            "roadmap": roadmap,
            "step": step,
        }
    )



@login_required
def delete_roadmap_step(request, roadmap_id, step_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    step = get_object_or_404(
        RoadmapStep,
        id=step_id,
        roadmap=roadmap
    )

    if request.method == "POST":

        step.delete()

        messages.success(
            request,
            "Roadmap step deleted successfully!"
        )

        return redirect(
            "roadmap_detail",
            roadmap_id=roadmap.id
        )

    return render(
        request,
        "skills/delete_roadmap_step.html",
        {
            "roadmap": roadmap,
            "step": step,
        }
    )



@login_required
def complete_roadmap_step(request, roadmap_id, step_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    step = get_object_or_404(
        RoadmapStep,
        id=step_id,
        roadmap=roadmap
    )

    step.completed = True
    step.completed_at = timezone.now()

    step.save()

    Activity.objects.create(
        roadmap=roadmap,
        activity_type="ROADMAP_STEP_COMPLETED",
        message=f'Roadmap step "{step.title}" was completed in "{roadmap.title}".'
    )

    messages.success(
        request,
        "Roadmap step completed! 🎉"
    )

    return redirect(
        "roadmap_detail",
        roadmap_id=roadmap.id
    )



@login_required
def undo_roadmap_step(request, roadmap_id, step_id):

    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        skill__user=request.user
    )

    step = get_object_or_404(
        RoadmapStep,
        id=step_id,
        roadmap=roadmap
    )

    step.completed = False
    step.completed_at = None

    step.save()

    Activity.objects.create(
        roadmap=roadmap,
        activity_type="ROADMAP_STEP_UNDONE",
        message=f'Roadmap step "{step.title}" was marked as pending in "{roadmap.title}".'
    )


    messages.success(
        request,
        "Roadmap step marked as pending."
    )

    return redirect(
        "roadmap_detail",
        roadmap_id=roadmap.id
    )


@login_required
def challenges(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        "all"
    )

    sort = request.GET.get(
        "sort",
        "latest"
    )

    challenges = Challenge.objects.filter(
        skill__user=request.user
    ).select_related(
        "skill"
    )

    # ==============================
    # SEARCH
    # ==============================

    if search:

        challenges = challenges.filter(
            title__icontains=search
        )


    # ==============================
    # STATUS FILTER
    # ==============================

    if status == "completed":

        challenges = challenges.filter(
            completed=True
        )

    elif status == "pending":

        challenges = challenges.filter(
            completed=False
        )


    # ==============================
    # SORT
    # ==============================

    if sort == "oldest":

        challenges = challenges.order_by(
            "created_at"
        )

    elif sort == "completed":

        challenges = challenges.order_by(
            "-completed",
            "-created_at"
        )

    elif sort == "pending":

        challenges = challenges.order_by(
            "completed",
            "-created_at"
        )

    else:

        challenges = challenges.order_by(
            "-created_at"
        )


    # ==============================
    # STATISTICS
    # ==============================

    all_challenges = Challenge.objects.filter(
        skill__user=request.user
    )

    total_challenges = all_challenges.count()

    completed_challenges = all_challenges.filter(
        completed=True
    ).count()

    pending_challenges = all_challenges.filter(
        completed=False
    ).count()


    # ==============================
    # RENDER
    # ==============================

    return render(
        request,
        "skills/challenges.html",
        {
            "challenges": challenges,

            "search": search,

            "current_status": status,

            "current_sort": sort,

            "total_challenges":
                total_challenges,

            "completed_challenges":
                completed_challenges,

            "pending_challenges":
                pending_challenges,
        }
    )


@login_required
def add_challenge(request):

    if request.method == "POST":

        form = ChallengeForm(
            request.POST
        )

        # Sirf current user's skills
        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

        if form.is_valid():

            challenge = form.save(
                commit=False
            )

            # Security check
            if challenge.skill.user != request.user:

                form.add_error(
                    "skill",
                    "You cannot select this skill."
                )

            else:

                challenge.save()

                Activity.objects.create(
                    challenge=challenge,
                    activity_type="CHALLENGE_CREATED",
                    message=f'Challenge "{challenge.title}" was created.'
                )

                messages.success(
                    request,
                    "Challenge added successfully! 🎯"
                )

                return redirect(
                    "challenges"
                )

    else:

        form = ChallengeForm()

        # Sirf current user's skills
        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

    return render(
        request,
        "skills/add_challenge.html",
        {
            "form": form
        }
    )

@login_required
def challenge_detail(request, challenge_id):

    challenge = get_object_or_404(
        Challenge,
        id=challenge_id,
        skill__user=request.user
    )

    return render(
        request,
        "skills/challenge_detail.html",
        {
            "challenge":challenge
        }
    )


@login_required
def edit_challenge(request, challenge_id):

    challenge = get_object_or_404(
        Challenge,
        id=challenge_id,
        skill__user=request.user
    )

    if request.method == "POST":

        form = ChallengeForm(
            request.POST,
            instance=challenge
        )

        # Only user's skills
        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

        if form.is_valid():

            updated_challenge = form.save(
                commit=False
            )

            if updated_challenge.skill.user != request.user:

                form.add_error(
                    "skill",
                    "You cannot select this skill."
                )

            else:

                updated_challenge.save()

                Activity.objects.create(
                    challenge=updated_challenge,
                    activity_type="CHALLENGE_UPDATED",
                    message=f'Challenge "{updated_challenge.title}" was updated.'
                )

                messages.success(
                    request,
                    "Challenge updated successfully!"
                )

                return redirect(
                    "challenge_detail",
                    challenge_id=challenge.id
                )

    else:

        form = ChallengeForm(
            instance=challenge
        )

        form.fields["skill"].queryset = Skill.objects.filter(
            user=request.user
        )

    return render(
        request,
        "skills/edit_challenge.html",
        {
            "form": form,
            "challenge": challenge
        }
    )


@login_required
def delete_challenge(request, challenge_id):

    challenge = get_object_or_404(
        Challenge,
        id=challenge_id,
        skill__user=request.user
    )

    if request.method == "POST":

        challenge.delete()

        Activity.objects.create(
            challenge=challenge,
            activity_type="CHALLENGE_DELETED",
            message=f'Challenge "{challenge.title}" was deleted.'
        )

        messages.success(
            request,
            "Challenge deleted successfully."
        )

        return redirect(
            "challenges"
        )

    return render(
        request,
        "skills/delete_challenge.html",
        {
            "challenge": challenge
        }
    )


@login_required
def complete_challenge(request, challenge_id):

    challenge = get_object_or_404(
        Challenge,
        id=challenge_id,
        skill__user=request.user
    )

    if request.method == "POST":

        challenge.completed = True
        challenge.completed_at = timezone.now()
        challenge.save()

        Activity.objects.create(
            challenge=challenge,
            activity_type="CHALLENGE_COMPLETED",
            message=f'Challenge "{challenge.title}" was completed.'
        )

        messages.success(
            request,
            "Challenge completed successfully 🎉"
        )

    return redirect(
        "challenge_detail",
        challenge_id=challenge.id
    )


@login_required
def undo_challenge(request, challenge_id):

    challenge = get_object_or_404(
        Challenge,
        id=challenge_id,
        skill__user=request.user
    )

    if request.method == "POST":

        challenge.completed = False
        challenge.completed_at = None

        challenge.save()

        Activity.objects.create(
            challenge=challenge,
            activity_type="CHALLENGE_UNDONE",
            message=f'Challenge "{challenge.title}" was marked as pending.'
        )

        messages.success(
            request,
            "Challenge marked as pending."
        )

    return redirect(
        "challenge_detail",
        challenge_id=challenge.id
    )


@login_required
def notes(request):

    notes = Note.objects.filter(
        user = request.user
    ).order_by(
        "-updated_at"
    )

    return render(
        request,
        "skills/notes.html",
        {
            "notes":notes
        }
    )


@login_required
def add_note(request):

    if request.method == "POST":

        form = NoteForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            note = form.save(
                commit=False
            )

            note.user = request.user

            note.save()

            Activity.objects.create(
                note=note,
                activity_type="NOTE_CREATED",
                message=f'Note "{note.title}" was created.'
            )

            messages.success(
                request,
                "Note added successfully!"
            )

            return redirect(
                "notes"
            )

    else:

        form = NoteForm()

    return render(
        request,
        "skills/add_note.html",
        {
            "form": form
        }
    )


@login_required
def note_detail(request, note_id):

    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    return render(
        request,
        "skills/note_detail.html",
        {
            "note":note
        }
    )


@login_required
def edit_note(request, note_id):

    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    if request.method == "POST":

        form = NoteForm(
            request.POST,
            request.FILES,
            instance=note
        )

        if form.is_valid():

            updated_note = form.save()

            Activity.objects.create(
                note=updated_note,
                activity_type="NOTE_UPDATED",
                message=f'Note "{updated_note.title}" was updated.'
            )

            messages.success(
                request,
                "Note updated successfully!"
            )

            return redirect(
                "note_detail",
                note_id=note.id
            )

    else:

        form = NoteForm(
            instance=note
        )

    return render(
        request,
        "skills/edit_note.html",
        {
            "form": form,
            "note": note
        }
    )


@login_required
def delete_note(request, note_id):

    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    if request.method == "POST":

        Activity.objects.create(
            note=note,
            activity_type="NOTE_DELETED",
            message=f'Note "{note.title}" was deleted.'
        )

        note.delete()

        messages.success(
            request,
            "Note deleted successfully"
        )

        return redirect(
            "notes"
        )

    return render(
        request,
        "skills/delete_note.html",
        {
            "note":note
        }
    )



@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "skills/profile.html",
        {
            "profile": profile
        }
    )



@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            # Update User email
            email = form.cleaned_data["email"]

            request.user.email = email
            request.user.save(
                update_fields=["email"]
            )

            messages.success(
                request,
                "Profile updated successfully!"
            )

            return redirect(
                "profile"
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "skills/edit_profile.html",
        {
            "form": form,
            "profile": profile,
        }
    )