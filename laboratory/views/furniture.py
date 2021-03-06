# encoding: utf-8


'''
Created on 26/12/2016

@author: luisza
'''
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from django_ajax.decorators import ajax
from laboratory.models import Furniture, Laboratory
from laboratory.shelf_utils import get_dataconfig
from laboratory.decorators import check_lab_permissions, user_lab_perms

from .djgeneric import ListView, CreateView, UpdateView, DeleteView


@method_decorator(check_lab_permissions, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_lab_perms(perm="report"), name='dispatch')
class FurnitureReportView(ListView):
    model = Furniture
    template_name = "laboratory/report_furniture_list.html"

    def get_queryset(self):
        return Furniture.objects.filter(labroom__laboratory=self.lab)


@method_decorator(check_lab_permissions, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_lab_perms(perm="admin"), name='dispatch')
class FurnitureCreateView(CreateView):
    model = Furniture
    fields = ("labroom", "name", "type")

    def get_form(self, form_class=None):
        form = super(FurnitureCreateView, self).get_form(form_class=form_class)
        if self.lab is not None:
            form.fields['labroom'].choices = ((x.pk, x) for x in
                                              get_object_or_404(Laboratory, pk=self.lab).rooms.all())
        return form

    def get_success_url(self):
        return reverse_lazy('laboratory:furniture_update',
                            args=(self.lab, self.object.pk))

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        lab = get_object_or_404(Laboratory, pk=self.lab)
        context['object_list'] = self.model.objects.filter(
            labroom__in=lab.rooms.all()).order_by('labroom')
        return context


class FurnitureForm(forms.ModelForm):
    dataconfig = forms.CharField(
        widget=forms.HiddenInput,
        validators=[RegexValidator(
            r'^[\[\],\s"\d]*$',
            message=_("Invalid format in shelf dataconfig "),
            code='invalid_format')])

    class Meta:
        model = Furniture
        fields = ("labroom", "name", "type", 'dataconfig')


@method_decorator(check_lab_permissions, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_lab_perms(perm="admin"), name='dispatch')
class FurnitureUpdateView(UpdateView):
    model = Furniture
    success_url = "/"
    form_class = FurnitureForm

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['dataconfig'] = self.build_configdata()
        return context

    def get_dataconfig(self):
        dataconfig = self.object.dataconfig
        return get_dataconfig(dataconfig)

    def build_configdata(self):
        dataconfig = self.get_dataconfig()
        row = len(dataconfig)
        if row > 0:
            col = len(dataconfig[0])
        else:
            col = 0
        return render_to_string('laboratory/dataconfig.html',
                                {'dataconfig': dataconfig,
                                 'obj': self.object,
                                 'col': col,
                                 'row': row,
                                 'laboratory': self.lab})

    def get_success_url(self):
        return reverse_lazy('laboratory:furniture_create',
                            args=(self.lab,))


@method_decorator(check_lab_permissions, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_lab_perms(perm="admin"), name='dispatch')
class FurnitureDelete(DeleteView):
    model = Furniture
    success_url = "/"

    def get_success_url(self):
        return reverse_lazy('laboratory:furniture_create', args=(self.lab,))


@login_required
def list_furniture_render(request, lab_pk=None):
    var = request.GET.get('namelaboratoryRoom', '0')

    if var:
        furnitures = Furniture.objects.filter(
            labroom__laboratory=lab_pk, labroom=var)
    else:
        furnitures = Furniture.objects.filter(labroom__laboratory=lab_pk)
    return render_to_string(
        'laboratory/furniture_list.html',
        context={
            'object_list': furnitures,
            'laboratory': lab_pk,
            'request': request
        })


@login_required
@ajax
def list_furniture(request, lab_pk):
    return {
        'inner-fragments': {
            '#furnitures': list_furniture_render(request, lab_pk),
            '.jsmessage': "<script>see_prototype_shelf_field();</script>"

        },
    }
