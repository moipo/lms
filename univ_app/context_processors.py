from .forms import PictureForm

def get_profile_picture_form(request):
    picture_form = PictureForm
    return {"picture_form": picture_form}