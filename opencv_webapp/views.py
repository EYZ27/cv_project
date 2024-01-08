from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face


def first_view(request):
  return render(request, 'opencv_webapp/first_view.html', {})


def simple_upload(request):

  if request.method == 'POST':  # 이미지가 들어왔으면
    form = SimpleUploadForm(request.POST, request.FILES)

    if form.is_valid():
      myfile = request.FILES['image']  # 메모리에 업로드 되어 있는 유저 이미지 파일
	  # 데이터베이스를 사용하지 않을 때 사용하는 filesystemstorage
      fs = FileSystemStorage()
      # fs.save('경로명을 포함할 파일 저장 시 활용할 이름', 파일 객체 자체)
      filename = fs.save(myfile.name, myfile)  # 저장이 끝난 물리적인 파일의 이름
      uploaded_file_url = fs.url(filename)  # 저장이 끝난 물리적인 파일로 접근 가능한 url
      context = {'form': form, 'uploaded_file_url': uploaded_file_url}
      return render(request, 'opencv_webapp/simple_upload.html', context)

  else:  # 아직 이미지가 안들어왔으면
    form = SimpleUploadForm()
    context = {'form': form}
    return render(request, 'opencv_webapp/simple_upload.html', context)


def detect_face(request):

  if request.method == 'POST':
    form = ImageUploadForm(request.POST, request.FILES)

    if form.is_valid():
      post = form.save(commit=False)
      post.save()

      imageURL = settings.MEDIA_URL + form.instance.document.name

      cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)

      return render(request, 'opencv_webapp/detect_face.html', {'form': form, 'post': post})

  else:  # GET 요청의 경우 처리
    form = ImageUploadForm()
    context = {'form': form}
    return render(request, 'opencv_webapp/detect_face.html', context)
