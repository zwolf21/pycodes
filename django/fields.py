import csv
from io import StringIO
from django.forms.fields import MultipleChoiceField
from django.utils.text import capfirst
from django.core import validators
from django.core import exceptions
from django.db import models
from django.utils.six import text_type, string_types


def list_to_csv(lst=None):	
	output = StringIO()
	w = csv.writer(output)
	w.writerow(sorted(lst) or [])
	return output.getvalue().strip()

def csv_to_list(csvalue):
	output = StringIO(str(csvalue))
	for row in csv.reader(output):
		return row
	return []


class CSVMultipleChoiceField(models.CharField):
    
    def __init__(self, choices,  *args, **kwargs):
        kwargs['max_length'] = len(list_to_csv([e[0] for e in choices]))
        super(CSVMultipleChoiceField, self).__init__(choices=choices, *args, **kwargs)
    
    def contribute_to_class(self, cls, name, **kwargs):
        super(CSVMultipleChoiceField, self).contribute_to_class(cls, name, **kwargs)
        class Descriptor(object):
            def __init__(self, field, *args, **kwargs):
                super(Descriptor, self).__init__(*args, **kwargs)
                self.field = field
            
            def __get__(self, obj, type=None):
                if obj:
                    return obj.__dict__[self.field.name]
                return self

            def __set__(self, obj, value):
                obj.__dict__[self.field.name] = self.field.to_python(value)
            
            def __eq__(self, other):
                super(Descriptor, self).__eq__(other)

        setattr(cls, self.name, Descriptor(self))

    def validate(self, value, model_instance):
        if not self.editable:
            return

        if self.choices and value:
            choices = []

            for option_key, option_value in self.choices:
                if isinstance(option_value, (list, tuple, set)):
                    for optgroup_key, optgroup_value in option_value:
                        choices.append(optgroup_key)
                else:
                    choices.append(option_key)

            choices = [text_type(choice) for choice in choices]

            for val in value:
                if val and val not in choices:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % val)

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'])

        if not self.blank and value in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])
    
    def to_python(self, value):
        if isinstance(value, string_types):
            return csv_to_list(value)
        return value

    def get_prep_value(self, value):
        if isinstance(value, string_types):
            value = [value]
        ret = list_to_csv(value)
        return ret
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, form_class=MultipleChoiceField, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()

        if self.choices:
            include_blank = (self.blank or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)

            for k in list(kwargs):
                if k not in ('choices', 'required',
                             'widget', 'label', 'initial', 'help_text',
                             'error_messages', 'show_hidden_initial'):
                    del kwargs[k]
        defaults.update(kwargs)
        return form_class(**defaults)