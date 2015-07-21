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
            img = handle_uploaded_file(f=request.FILES['file'], shapes=data['shapes'], colours=data['colours'], size=data['size'])
            response = HttpResponse(content_type="image/png")
            img.save(response, "PNG")
            return response
    else:
        form = UploadFileForm()

    return render(request, 'generator/pattern.html', {'form': form})
