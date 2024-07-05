'''from django import forms



class PermissionsForm(forms.Form):
    view = forms.BooleanField(label='Может просматривать', initial=False, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    add = forms.BooleanField(label='Может добавлять', initial=False, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    change = forms.BooleanField(label='Может изменять', initial=False, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    delete = forms.BooleanField(label='Может удалять', initial=False, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))


class FormsList:
    def __init__(self, form_class):
        self.__form_class = form_class

    def set_init_data(self, initial_data):
        self.__forms_list = []
        for initial_data in initial_data:
            self.__forms_list.append({
                'title':initial_data['title'],
                'form': self.__form_class(initial=initial_data['data'], prefix=initial_data['prefix'])
            })

    def set_post_data(self, titles, post_data):
        self.__forms_list = []
        for title in titles:
            self.__forms_list.append({
                'title':title[1],
                'form':self.__form_class(post_data,prefix=title[0])
            })

    def get_forms_list(self):
        return self.__forms_list

    def is_valid(self):
        self.__cleaned_data = []
        for form in self.__forms_list:
            if form['form'].is_valid():
                self.__cleaned_data.append({
                    'prefix':form['form'].prefix,
                    'data':form['form'].cleaned_data
                })
            else:
                return False
        return True

    def get_cleabed_data(self):
        return self.__cleaned_data'''
