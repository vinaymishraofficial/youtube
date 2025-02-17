from django import forms

class YouTubeForm(forms.Form):
    url = forms.URLField(label='YouTube URL', max_length=200, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter YouTube URL'}))
    resolution = forms.ChoiceField(choices=[('144', '144p'), ('240', '240p'), ('360', '360p'), ('480', '480p'), ('720', '720p'), ('1080', '1080p')], required=False)
