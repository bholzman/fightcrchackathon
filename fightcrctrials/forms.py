from django import forms

class ContactUsForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Your first name', strip=True)
    last_name = forms.CharField(max_length=50, label='Your last name', strip=True)
    user_class = forms.ChoiceField(
        label='I am a',
        choices=(
            ('patient / survivor', 'patient / survivor'),
            ('caregiver', 'caregiver'),
            ('family member / friend of patient', 'family member / friend of patient'),
            ('medical professional', 'medical professional'),
            ('other', 'other')))
    email = forms.EmailField(label='Your email address')

    comment = forms.CharField(widget=forms.Textarea)
