# coding:utf-8
from django import forms
from DjangoUeditor.widgets import UEditorWidget
from DjangoUeditor.forms import UEditorField, UEditorModelForm
from models import Announcement


class AnnouncementUEditorForm(forms.Form):
    description = UEditorField("内容", initial="请再次填写内容", width=500, height=100, filePath="img/")


class AnnouncementUEditorModelForm(UEditorModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'
