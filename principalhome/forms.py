from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    subject = forms.TextInput()
    expiry_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    audience = forms.ChoiceField(choices = [(1, "Teachers"), (2, "Students"), (3, "All")], widget=forms.RadioSelect, required=True)
    message = forms.Textarea()

    class Meta:
        model = Announcement
        fields = ['subject', 'expiry_date', 'audience', 'message']