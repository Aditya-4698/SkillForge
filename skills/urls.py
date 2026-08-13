from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "",
        views.skills_home,
        name="skills_home"
    ),

    path(
        "add/",
        views.add_skill,
        name="add_skill"
    ),

    path(
        "edit/<int:skill_id>/",
        views.edit_skill,
        name="edit_skill"
    ),

    path(
        "delete/<int:skill_id>/",
        views.delete_skill,
        name="delete_skill"
    ),

    path(
        "<int:skill_id>/",
        views.skill_detail,
        name="skill_detail"
    ),

    path(
        "<int:skill_id>/goals/add/",
        views.add_goal,
        name="add_goal"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/edit/",
        views.edit_goal,
        name="edit_goal"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/delete/",
        views.delete_goal,
        name="delete_goal"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/complete/",
        views.complete_goal,
        name="complete_goal"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/undo/",
        views.undo_goal,
        name="undo_goal"
    ),

    path(
        "goals/",
        views.goals,
        name="goals"
    ),

    path(
        "projects/",
        views.projects,
        name="projects"
    ),

    path(
        "projects/add/",
        views.add_project,
        name="add_project"
    ),

    path(
        "projects/<int:project_id>/",
        views.project_detail,
        name="project_detail"
    ),

    path(
        "project/<int:project_id>/edit/",
        views.edit_project,
        name="edit_project"
    ),

    path(
        "project/<int:project_id>/delete/",
        views.delete_project,
        name="delete_project"
    ),

    path(
        "projects/<int:project_id>/milestones/add/",
        views.add_milestone,
        name="add_milestone"
    ),

    path(
        "projects/<int:project_id>/milestones/<int:milestone_id>/complete/",
        views.complete_milestone,
        name="complete_milestone"
    ),

    path(
        "projects/<int:project_id>/milestones/<int:milestone_id>/undo/",
        views.undo_milestone,
        name="undo_milestone"
    ),

    path(
        "projects/<int:project_id>/milestones/<int:milestone_id>/edit/",
        views.edit_milestone,
        name="edit_milestone"
    ),

    path(
        "projects/<int:project_id>/milestones/<int:milestone_id>/delete/",
        views.delete_milestone,
        name="delete_milestone"
    ),
    

    path(
        "goals/<int:goal_id>/",
        views.goal_detail,
        name="goal_detail"
    ),

    # =========================================================
    # GOAL TASKS
    # =========================================================

    path(
        "goals/<int:goal_id>/tasks/add/",
        views.add_goal_task,
        name="add_goal_task"
    ),

    path(
        "goal-tasks/<int:task_id>/toggle/",
        views.toggle_goal_task,
        name="toggle_goal_task"
    ),

    path(
        "goal-tasks/<int:task_id>/edit/",
        views.edit_goal_task,
        name="edit_goal_task"
    ),

    path(
        "goal-tasks/<int:task_id>/delete/",
        views.delete_goal_task,
        name="delete_goal_task"
    ),


    # =========================================================
    # SKILL → GOAL → TASK
    # Existing HTML uses these names
    # =========================================================

    path(
        "<int:skill_id>/goals/<int:goal_id>/tasks/add/",
        views.add_task,
        name="add_task"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/tasks/<int:task_id>/complete/",
        views.complete_task,
        name="complete_task"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/tasks/<int:task_id>/undo/",
        views.undo_task,
        name="undo_task"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/tasks/<int:task_id>/edit/",
        views.edit_task,
        name="edit_task"
    ),

    path(
        "<int:skill_id>/goals/<int:goal_id>/tasks/<int:task_id>/delete/",
        views.delete_task,
        name="delete_task"
    ),

    path(
        "tasks/",
        views.tasks,
        name="tasks"
    ),

    #=========
    #Roadmap
    #=========

        path(
        "roadmaps/",
        views.roadmaps,
        name="roadmaps"
    ),

    path(
        "roadmaps/add/",
        views.add_roadmap,
        name="add_roadmap"
    ),

    path(
        "roadmaps/<int:roadmap_id>/",
        views.roadmap_detail,
        name="roadmap_detail"
    ),

    path(
        "roadmaps/<int:roadmap_id>/edit/",
        views.edit_roadmap,
        name="edit_roadmap"
    ),

    path(
        "roadmaps/<int:roadmap_id>/delete/",
        views.delete_roadmap,
        name="delete_roadmap"
    ),

    # =============
    # ROADMAP STEPS
    # =============

    path(
        "roadmaps/<int:roadmap_id>/steps/add/",
        views.add_roadmap_step,
        name="add_roadmap_step"
    ),

    path(
        "roadmaps/<int:roadmap_id>/steps/<int:step_id>/complete/",
        views.complete_roadmap_step,
        name="complete_roadmap_step"
    ),

    path(
        "roadmaps/<int:roadmap_id>/steps/<int:step_id>/undo/",
        views.undo_roadmap_step,
        name="undo_roadmap_step"
    ),

    path(
        "roadmaps/<int:roadmap_id>/steps/<int:step_id>/edit/",
        views.edit_roadmap_step,
        name="edit_roadmap_step"
    ),

    path(
        "roadmaps/<int:roadmap_id>/steps/<int:step_id>/delete/",
        views.delete_roadmap_step,
        name="delete_roadmap_step"
    ),

    path(
        "challenges/",
        views.challenges,
        name="challenges"
    ),

    path(
        "challenges/add/",
        views.add_challenge,
        name="add_challenge"
    ),

    path(
        "challenges/<int:challenge_id>/",
        views.challenge_detail,
        name="challenge_detail"
    ),

    path(
        "challenges/<int:challenge_id>/edit/",
        views.edit_challenge,
        name="edit_challenge"
    ),

    path(
        "challenges/<int:challenge_id>/delete/",
        views.delete_challenge,
        name="delete_challenge"
    ),

    path(
        "challenges/<int:challenge_id>/complete/",
        views.complete_challenge,
        name="complete_challenge"
    ),

    path(
        "challenges/<int:challenge_id>/undo/",
        views.undo_challenge,
        name="undo_challenge"
    ),

    path(
        "notes/",
        views.notes,
        name="notes"
    ),

    path(
        "notes/add/",
        views.add_note,
        name="add_note"
    ),

    path(
        "notes/<int:note_id>/",
        views.note_detail,
        name="note_detail"
    ),

    path(
        "notes/<int:note_id>/edit/",
        views.edit_note,
        name="edit_note"
    ),

    path(
        "notes/<int:note_id>/delete/",
        views.delete_note,
        name="delete_note"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),


    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html"
    ),
    name="password_reset"
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ),
    name="password_reset_done"
),

path(
    "password-reset-confirm/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
    ),
    name="password_reset_confirm"
),

path(
    "password-reset-complete/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ),
    name="password_reset_complete"
),

]