from django.contrib.auth.models import User
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from adminhome.models import Teacher 
from .models import Assignment, Attendance
from django.forms import formset_factory

class AddassignForm(forms.ModelForm):
    class_number = forms.IntegerField()
    subject = forms.CharField(max_length = 20)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    due_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    assignment_file = forms.FileField()

    class Meta:
        model = Assignment
        fields = ['class_number', 'subject', 'start_date', 'due_date', 'assignment_file']

class AttendanceForm(forms.ModelForm):
    # date = forms.DateTimeField(label='Date', widget=forms.TextInput(attrs={'class':'datetime-input'}))

    class Meta:
        model = Attendance
        exclude = ['school', 'absent_on', 'name', 'roll_no', 'study']

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(AttendanceForm, self).__init__(*args, **kwargs)

        choices = [(1, 'Present'), (2, 'Absent')]

        for roll_no in extra:
            self.fields[roll_no] = forms.ChoiceField(
            label= roll_no,
            choices=choices,
            widget=forms.RadioSelect(),
        )

    def extra_responses(self):

        for name, value in self.cleaned_data.items():
            yield (self.fields[name].label, value)
