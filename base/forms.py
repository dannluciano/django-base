# forms.py
from django import forms
from django.contrib.flatpages.models import FlatPage
from django_prose_editor.widgets import ProseEditorWidget


class FlatPageForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = "__all__"
        widgets = {
            "content": ProseEditorWidget(),
        }
