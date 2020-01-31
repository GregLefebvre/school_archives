from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def file_size(value): # add this to some file where you can import it from
    nb_mib = 5
    limit = nb_mib * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed {} MiB.'.format(nb_mib))

class SearchFilesForm(forms.ModelForm):
    school = forms.CharField(label=_("School"), max_length=100)
    page = forms.CharField(widget = forms.HiddenInput(), initial=1)
    class Meta:
        model = FileHomework
        fields = ('title', 'promo', 'subject')

    def __init__(self, *args, **kwargs):
        super(SearchFilesForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False

    def clean(self):
        cleaned_data = super(SearchFilesForm, self).clean()
        school_name = cleaned_data.get('school')

        if school_name:
            if not School.objects.filter(title=school_name).exists():
                self.add_error(
                    "school",
                    "The school must exist!"
                )

class UploadFileForm(forms.ModelForm):
    school = forms.CharField(label=_("School"), max_length=100)
    class Meta:
        model = FileHomework
        fields = ( 'file_pdf', 'title', 'promo', 'subject', 'comment')
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':40}),
        }
    file_pdf = forms.FileField(required=False, validators=[file_size])

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        # self.fields['comment'].widget.attrs['placeholder'] = self.fields['email'].label or 'email@address.nl'

    def clean(self):
        cleaned_data = super(UploadFileForm, self).clean()
        file_pdf = cleaned_data.get('file_pdf')
        school_name = cleaned_data.get('school')

        if file_pdf:
            filename = file_pdf.name
            if not filename.endswith('.pdf'):
                self.add_error(
                    "file_pdf",
                    "The file must be a pdf!"
                )

        if school_name:
            if not School.objects.filter(title=school_name).exists():
                self.add_error(
                    "school",
                    "The school must exist!"
                )

        return cleaned_data
#
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('title', 'comment', 'image', 'video')
#
# class PostLikeForm(forms.ModelForm):
#     class Meta:
#         model = PostLike
#         fields = ('rank',)
#
#     rank = forms.IntegerField(max_value=9, min_value=0)
#
# class PostCommentForm(forms.ModelForm):
#     class Meta:
#         model = PostComment
#         fields = ('content',)
#
#     content = forms.CharField(max_length=255, widget=forms.Textarea)
