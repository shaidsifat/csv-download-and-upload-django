from codecs import decode, utf_16_be_decode
import csv
from fileinput import filename
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import customer
from django import forms
from .models import customer
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from io import BytesIO


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'balance')
    actions =['export_as_csv',]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            print(csv_file)
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")#decode('ascii',errors='replace')
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")

                print(fields)
                created = customer.objects.create(
                    id = fields[0],
                    name = fields[1],
                    balance = fields[2],
                    )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
'''
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)
      '''
admin.site.register(customer, CustomerAdmin)