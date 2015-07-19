from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
from .utils import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            img = handle_uploaded_file(f=request.FILES['file'], shapes=data['shapes'])
            return HttpResponse(img, content_type="image/jpeg")
    else:
        form = UploadFileForm()

    return render(request, 'generator/pattern.html', {'form': form})
