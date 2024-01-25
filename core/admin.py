from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin
from core.models import Pessoa
from core.views import import_csv_file
from django import forms
from django.contrib import admin
from django.core.validators import FileExtensionValidator
from django.template.response import TemplateResponse


class UploadForm(forms.Form):
    file = forms.FileField(
        required=True,
        label="Select a file",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )
    qtd_itens_batched = forms.IntegerField(
        required=True,
        label="Quantity itens per batch",
        min_value=1,
        initial=100,
    )


@admin.register(Pessoa)
class PessoaAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ["nome", "sobrenome", "cpf", "idade"]

    @button()
    def upload(self, request):
        context = self.get_common_context(request, title="Upload")
        if request.method == "POST":
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"]
                qtd_itens_batched = form.cleaned_data["qtd_itens_batched"]
                import_csv_file(file, qtd_itens_batched)
        else:
            form = UploadForm()
        context["form"] = form
        return TemplateResponse(request, "admin_extra_buttons/upload.html", context)
