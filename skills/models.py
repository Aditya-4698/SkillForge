from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Skill(models.Model):

    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    progress = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_progress(self):

        goals = self.goals.all()

        if not goals.exists():
            self.progress = 0

        else:

            total_progress = sum(
                goal.current_progress
                for goal in goals
            )

            self.progress = round(
                total_progress / goals.count()
            )

        self.save(
            update_fields=["progress"]
        )

    @property
    def project_progress(self):

        projects = self.projects.all()

        if not projects.exists():
            return 0

        total_progress = sum(
            project.milestone_progress
            for project in projects
        )

        return round(
            total_progress / projects.count()
        )

    def __str__(self):
        return self.name


class Goal(models.Model):

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="goals"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    target_progress = models.PositiveIntegerField(
        default=100
    )

    current_progress = models.PositiveIntegerField(
        default=0
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # =====================================================
    # STATUS
    # =====================================================

    @property
    def status(self):

        if self.completed:
            return "Completed"

        if not self.deadline:
            return "No Deadline"

        today = timezone.localdate()

        if self.deadline < today:
            return "Overdue"

        days_left = (
            self.deadline - today
        ).days

        if days_left <= 7:
            return "Deadline Soon"

        return "On Track"

    @property
    def goal(self):
        return self

    @property
    def tasks(self):
        return self.goal_tasks
    # =====================================================
    # DAYS REMAINING
    # =====================================================

    @property
    def days_remaining(self):

        if not self.deadline:
            return None

        if self.completed:
            return 0

        today = timezone.localdate()

        return (
            self.deadline - today
        ).days


    # =====================================================
    # DAYS OVERDUE
    # =====================================================

    @property
    def days_overdue(self):

        if not self.deadline:
            return 0

        today = timezone.localdate()

        if self.deadline >= today:
            return 0

        return (
            today - self.deadline
        ).days


    # =====================================================
    # TOTAL TASKS
    # =====================================================

    @property
    def total_tasks(self):

        return self.goal_tasks.count()


    # =====================================================
    # COMPLETED TASKS
    # =====================================================

    @property
    def completed_tasks(self):

        return self.goal_tasks.filter(
            completed=True
        ).count()


    # =====================================================
    # TASK PROGRESS
    # =====================================================

    @property
    def task_progress(self):

        total_tasks = self.total_tasks

        if total_tasks == 0:
            return 0

        completed_tasks = self.completed_tasks

        return round(
            completed_tasks * 100 / total_tasks
        )


    # =====================================================
    # UPDATE PROGRESS
    # =====================================================

    def update_progress(self):

        total = self.goal_tasks.count()

        if total == 0:

            self.current_progress = 0

        else:

            completed = self.goal_tasks.filter(
                completed=True
            ).count()

            self.current_progress = round(
                (completed / total) * 100
            )

        self.save(
            update_fields=[
                "current_progress"
            ]
        )


    # =====================================================
    # OVERALL PROGRESS
    # =====================================================

    @property
    def overall_progress(self):

        if self.goal_tasks.exists():
            return self.task_progress

        return self.current_progress


    # =====================================================
    # TARGET REACHED
    # =====================================================

    @property
    def target_reached(self):

        return (
            self.overall_progress
            >= self.target_progress
        )


    # =====================================================
    # PROGRESS STATUS
    # =====================================================

    @property
    def progress_status(self):

        if self.target_reached:
            return "Completed"

        if self.current_progress > 0:
            return "In Progress"

        return "Not Started"


    # =====================================================
    # SMART STATUS
    # =====================================================

    @property
    def smart_status(self):

        if self.target_reached:
            return "Completed"

        if not self.deadline:
            return "No deadline"

        if self.days_remaining < 0:
            return "Overdue"

        if self.days_remaining <= 7:
            return "Deadline Soon"

        return "On track"


    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return self.title


class GoalTask(models.Model):

    goal=models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goal_tasks"
    )

    title = models.CharField(
        max_length=200
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    

class Project(models.Model):

    STATUS_CHOICES = [
        ("Planning", "Planning"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("On Hold", "On Hold"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    resource_link = models.URLField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Planning"
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="MEDIUM"
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    progress = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def milestone_progress(self):

        total = self.milestones.count()

        if total == 0:
            return 0

        completed = self.milestones.filter(
            completed=True
        ).count()

        return round(
            (completed / total) * 100
        )

    def update_progress(self):

        self.progress = self.milestone_progress

        self.save(
            update_fields=["progress"]
        )

    @property
    def total_milestones(self):
        return self.milestones.count()

    @property
    def completed_milestones(self):
        return self.milestones.filter(
            completed=True
        ).count()

    @property
    def pending_milestones(self):
        return self.milestones.filter(
            completed=False
        ).count()

    @property
    def is_overdue(self):

        if not self.deadline:
            return False

        if self.milestone_progress == 100:
            return False

        return self.deadline < timezone.localdate()

    @property
    def days_remaining(self):

        if not self.deadline:
            return None

        if self.milestone_progress == 100:
            return 0

        return (
            self.deadline - timezone.localdate()
        ).days

    def __str__(self):
        return self.title


class Milestone(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title




class Roadmap(models.Model):

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="roadmaps"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now_add=True
    )


    @property
    def progress(self):

        total_steps = self.steps.count()

        if total_steps == 0:
            return 0

        completed_steps = self.steps.filter(
            completed=True
        ).count()

        return round(
            (completed_steps / total_steps) * 100
        )

    def __str__(self):
        return self.title


class RoadmapStep(models.Model):

    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="steps"
    )

    title = models.CharField(
        max_length=200
    )

    description= models.TextField(
        blank=True
    )

    order = models.PositiveIntegerField(
        default = 1
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title



class Challenge(models.Model):

    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="challenges"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="Easy"
    )

    target = models.PositiveIntegerField(
        default=1
    )

    progress = models.PositiveIntegerField(
        default=0
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Note(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    attachment = models.FileField(
        upload_to="notes/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title



class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    bio = models.TextField(
        blank=True
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username

class Activity(models.Model):

    ACTIVITY_TYPES = [
        ("PROJECT_CREATED", "Project Created"),
        ("PROJECT_UPDATED", "Project Updated"),

        ("MILESTONE_CREATED", "Milestone Created"),
        ("MILESTONE_COMPLETED", "Milestone Completed"),
        ("MILESTONE_UNDONE", "Milestone Undone"),
        ("MILESTONE_UPDATED", "Milestone Updated"),
        ("MILESTONE_DELETED", "Milestone Deleted"),

        ("ROADMAP_CREATED", "Roadmap Created"),
        ("ROADMAP_UPDATED", "Roadmap Updated"),
        ("ROADMAP_DELETED", "Roadmap Deleted"),

        ("ROADMAP_STEP_CREATED", "Roadmap Step Created"),
        ("ROADMAP_STEP_UPDATED", "Roadmap Step Updated"),
        ("ROADMAP_STEP_COMPLETED", "Roadmap Step Completed"),
        ("ROADMAP_STEP_UNDONE", "Roadmap Step Undone"),
        ("ROADMAP_STEP_DELETED", "Roadmap Step Deleted"),

        ("CHALLENGE_CREATED", "Challenge Created"),
        ("CHALLENGE_UPDATED", "Challenge Updated"),
        ("CHALLENGE_DELETED", "Challenge Deleted"),
        ("CHALLENGE_COMPLETED", "Challenge Completed"),
        ("CHALLENGE_UNDONE", "Challenge Undone"),

        ("NOTE_CREATED", "Note Created"),
        ("NOTE_UPDATED", "Note Updated"),
        ("NOTE_DELETED", "Note Deleted"),
    ]

    # ==============================
    # PROJECT
    # ==============================

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True
    )

    # ==============================
    # ROADMAP
    # ==============================

    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True
    )

    # ==============================
    # CHALLENGE
    # ==============================

    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True
    )

    # ==============================
    # NOTE
    # ==============================

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True
    )

    # ==============================
    # ACTIVITY DATA
    # ==============================

    activity_type = models.CharField(
        max_length=40,
        choices=ACTIVITY_TYPES
    )

    message = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.message