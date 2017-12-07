from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, FormView
from django.core.exceptions import ObjectDoesNotExist

from scheduler.forms import CompanyForm
from scheduler.models.company_m import CompanyInfo
from scheduler.string_name import FIELD, DATE, TERM, NAME
from scheduler.tables import CompanyTable
from scheduler.views.common_v import request_table_config


class CompanyFormView(FormView):
    template_name = 'home_t.html'
    form_class = CompanyForm
    object_list = None

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        self.object_list = CompanyInfo.objects.all()

        table = CompanyTable(self.object_list)
        request_table_config(request, table)
        context['form'] = form
        context['table'] = table
        context['is_update'] = False
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form, request, **kwargs)
        else:
            return self.form_invalid(form, request, **kwargs)

    def form_valid(self, form, request, **kwargs):
        # save
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['is_update'] = False

        company_data = form.save(commit=False)
        name = form.cleaned_data[NAME]
        field_of = form.cleaned_data[FIELD]
        term = form.cleaned_data[TERM]
        date = form.cleaned_data[DATE]
        company_data.name = name
        company_data.field_of = field_of
        company_data.term = term
        company_data.date = date
        company_data.save()

        return redirect('home')

    def form_invalid(self, form, request, **kwargs):
        context = self.get_context_data(**kwargs)

        self.object_list = CompanyInfo.objects.all()

        table = CompanyTable(self.object_list)
        request_table_config(request, table)
        context['form'] = form
        context['table'] = table
        context['is_update'] = False

        return self.render_to_response(context)


class CompanyUpdateView(UpdateView):
    template_name = 'home_t.html'
    form_class = CompanyForm
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)

        table = CompanyTable(CompanyInfo.objects.all())
        request_table_config(request, table)
        context['form'] = form
        context['table'] = table
        context['is_update'] = True
        context['show_add_company_panel'] = True
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form()

        if 'cancel' in request.POST:
            return redirect('home')

        if form.is_valid():
            return self.form_valid(form, request, **kwargs)
        else:
            return self.form_invalid(form, request, **kwargs)

    def get_object(self, queryset=None):
        obj = CompanyInfo.objects.get(id=self.kwargs['company_id'])
        return obj

    def form_valid(self, form, request, **kwargs):

        if 'delete' in request.POST:
            try:
                CompanyInfo.objects.get(id=self.object.id).delete()
            except ObjectDoesNotExist:
                pass
        elif 'edit' in request.POST:
            company_data = CompanyInfo.objects.get(id=self.object.id)
            company_data.name = form.cleaned_data[NAME]
            company_data.field_of = form.cleaned_data[FIELD]
            company_data.term = form.cleaned_data[TERM]
            company_data.date = form.cleaned_data[DATE]
            company_data.save()

        return redirect('home')

    def form_invalid(self, form, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['is_update'] = True

        object = CompanyInfo.objects.all()

        table = CompanyTable(object)
        request_table_config(request, table)
        context['table'] = table
        context['is_update'] = True

        return self.render_to_response(context)

