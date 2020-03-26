from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse
from panel.models import Content, Category


class BlogForm(forms.ModelForm):
    # created_at = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Content
        fields = ("title", "slug", "is_static_url", "body", "category", "published")
        widgets = {"body": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.fields["body"].required = False
        # self.fields['category'].required = False
        # self.helper.form_action = reverse('panel:category_add')
        # self.helper.add_input(Submit('submit', 'Save'))


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "is_static_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_action = reverse("panel:category_add")
        self.helper.add_input(Submit("submit", "Save Category"))


class StaticForm(forms.ModelForm):
    # created_at = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Content
        fields = ("title", "slug", "is_static_url", "body")
        widgets = {"body": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.fields["body"].required = False
        # self.fields['category'].required = False
        # self.helper.form_action = reverse('panel:category_add')
        # self.helper.add_input(Submit('submit', 'Save'))
