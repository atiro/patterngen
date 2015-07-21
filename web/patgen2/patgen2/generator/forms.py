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
    colours = forms.ChoiceField(choices=[(x, x) for x in range(5,50)], initial='20')
    size = forms.ChoiceField(choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25')], initial='20')
