from django import forms

# place form definition here

SHAPES_CHOICES = (
    ('squares', 'Squares'),
    ('triangles', 'Triangles'),
)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    shapes = forms.ChoiceField(widget=forms.RadioSelect, choices=SHAPES_CHOICES, initial='squares')
