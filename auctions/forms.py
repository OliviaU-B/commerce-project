from django import forms

categories = (
    (1, "Fashion"),
    (2, "Toys"),
    (3, "Homeware"),
    (4, "Electronics"),
)

class NewListingForm(forms.Form):
    listing_name = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.DecimalField(decimal_places=2, initial="0.99")
    image = forms.URLField(required="False")
    category = forms.TypedChoiceField(required="False", choices=categories, coerce=str)