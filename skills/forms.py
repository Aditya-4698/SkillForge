from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Skill,Goal,Project,Milestone, GoalTask, Roadmap, RoadmapStep, Challenge, Note, Profile

class SignupForm(forms.ModelForm):

    password = forms.CharField(
        label= "Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password"
            }
        )
    )

    confirm_password= forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password"
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter username"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email"
                }
            ),
        }

        def clean_username(self):
            username = self.clean_data["username"]

            if User.objects.filter(
                username=username
            ).exists():

                raise forms.ValidationError(
                    "Username already exists."
                )
            return username

        def clean(self):

            cleaned_data = super().clean()

            password = cleaned_data.get(
                "password"
            )

            confirm_password = cleaned_data.get(
                "confirm_password"
            )

            if(
                password
                and confirm_password
                and password != confirm_password
            ):
                raise forms.ValidationError(
                    "Password do not match"
                )
            return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder": "Enter your Username",
                "autocomplete": "username"
            }
        )
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
                "autocomplete": "current-password",
            }
        )
    )

    def clean(self):

        cleaned_data = super().clean()
        username = cleaned_data.get(
            "username"
        )

        password = cleaned_data.get(
            "password"
        )

        if username and password:
            user = authenticate(
                username=username,
                password=password
            )

            if user is None:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            cleaned_data["user"] = user

        return cleaned_data



class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill

        fields = [
            "name",
            "description",
            "progress",
            "level",
        ]

        labels = {
            "name": "Skill Name",
            "description": "Description",
            "progress": "Progress (%)",
            "level": "Level",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Python",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe the Skills...",
                    "rows": 4,
                }
            ),

            "progress": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                    "placeholder": "0 - 100",
                }
            ),

            "level": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }




class GoalForm(forms.ModelForm):

    class Meta:
        model = Goal

        fields=[
            "title",
            "description",
            "current_progress",
            "target_progress",
            "deadline"
        ]

        labels={
            "title": "Goal Title",
            "description": "Description",
            "current_progress": "Current Progress (%)",
            "target_progress": "Target Progress (%)",
            "deadline": "Deadline"
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placehonder": "e.g. Become Django Expert",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your learning goals..",
                }
            ),

            "current_progress": forms.NumberInput(
                    attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                    "placeholder": "0 - 100",
                }
            ),

            "target_progress": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                    "placeholder": "0 - 100",
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()
        current = cleaned_data.get(
            "current_progress"
        )

        target = cleaned_data.get(
            "target_progress"
        )

        if (
            current is not None and target is not None and current > target
        ):
            raise forms.ValidationError(
                "Current progress cannot be greater than target progress."
            )

        return cleaned_data



class ProjectForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = [
            "skill",
            "title",
            "description",
            "resource_link",
            "status",
            "progress",
            "priority",
            "deadline",
        ]

        labels = {
            "skill": "Skill",
            "title": "Project",
            "description": "Description",
            "resource_link": "Project URL",
            "status": "Status",
            "progress": "Progress (%)",
            "priority": "Priority",
            "deadline": "Deadline",
        }

        widgets = {

            "skill": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter project title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter project description"
                }
            ),

            "resource_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/username/project"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "progress": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                    "placeholder": "0 - 100"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user:

            self.fields["skill"].queryset = Skill.objects.filter(
                user=user
            )




class MilestoneForm(forms.ModelForm):

    class Meta:

        model = Milestone

        fields = [
            "title",
            "description",
        ]

        labels = {
            "title": "Milestone Title",
            "description": "Description",
        }

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter milestone title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe this milestone...",
                }
            ),

        }


class GoalTaskForm(forms.ModelForm):

    class Meta:

        model = GoalTask

        fields = [
            "title",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title..."
                }
            ),

        }


class RoadmapForm(forms.ModelForm):

    class Meta:

        model = Roadmap

        fields = [
            "skill",
            "title",
            "description",
        ]

        labels = {
            "skill": "Skill",
            "title": "Roadmap Title",
            "description": "Description",
        }

        widgets = {
            "skill": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter roadmap title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placceholder": "Describe the roadmap",
                    "rows": 4
                }
            ),
        }


class RoadmapStepForm(forms.ModelForm):

    class Meta:

        model = RoadmapStep

        fields = [
            "title",
            "description",
            "order",
        ]

        labels = {
            "title": "Step Title",
            "description" : "Description",
            "order": "Step Order",
        }

        widgets = {

            "title": forms.TextInput(
                attrs= {
                    "class": "form-control",
                    "placeholder": "Each step title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "placeholder": "Describe this learning step",
                    "rows": 4
                }
            ),

            "order": forms.NumberInput(
                attrs= {
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "Enter step order",
                }
            ),
        }



class ChallengeForm(forms.ModelForm):

    class Meta:

        model = Challenge

        fields = [
            "skill",
            "title",
            "description",
            "difficulty",
            "target",
        ]

        labels = {
            "skill": "Skill",
            "title": "Challenge Title",
            "description": "Description",
            "difficulty": "Difficulty",
            "target": "Target",
        }

        widgets = {

            "skill": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Challenge Title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe this challenge...",
                    "rows": 4
                }
            ),

            "difficulty": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "target": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "Enter target"
                }
            ),
        }


class NoteForm(forms.ModelForm):

    class Meta:

        model = Note

        fields = [
            "title",
            "content",
            "attachment",
        ]

        labels = {
            "title": "Note Title",
            "content": "Note Content",
            "attachment": "Attachment",
        }

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter note title"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your note here...",
                    "rows": 4
                }
            ),

            "attachment": forms.ClearableFileInput(
                    attrs={
                        "class": "form-control",
                        "accept": ".pdf",
                    }
                ),
            }

        def clean_attachment(self):

            attachment = self.cleaned_data.get(
                "attachment"
            )

            if attachment:

                # ==============================
                # PDF CHECK
                # ==============================

                if not attachment.name.lower().endswith(".pdf"):

                    raise forms.ValidationError(
                        "Only PDF files are allowed."
                    )


                # ==============================
                # FILE SIZE CHECK
                # ==============================

                max_size = 5 * 1024 * 1024  # 5 MB

                if attachment.size > max_size:

                    raise forms.ValidationError(
                        "PDF size must be less than 5 MB."
                    )

            return attachment


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(
        label="Email Address",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address"
            }
        )
    )

    class Meta:

        model = Profile

        fields = [
            "email",
            "bio",
            "profile_image"
        ]

        labels = {
            "email": "Email Address",
            "bio": "Bio",
            "profile_image": "Profile Image",
        }

        widgets = {

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tell something about yourself..."
                }
            ),

            "profile_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:

            self.fields["email"].initial = self.instance.user.email