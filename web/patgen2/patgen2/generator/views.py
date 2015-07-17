from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
from utils import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            img = handle_uploaded_file(request.FILES['file'])
            return HttpResponse(img, content_type="image/jpeg")
    else:
        form = UploadFileForm()

    return render(request, 'generator/pattern.html', {'form': form})
