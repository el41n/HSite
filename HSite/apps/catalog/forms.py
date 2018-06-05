from django import forms

from .models.cpu.cpu import CPU
from .models.motherboard.motherboard import Motherboard
from .models.memory.memory import Memory
from .models.power_block.power_block import PowerBlock
from .models.hardware import Vendor


def model_valid(Model):
    def func(func):
        def wrapper(model_id, *args):
            if Model.objects.filter(id=model_id).exists():
                return func(model_id, *args)
            else:
                return False
        return wrapper
    return func


def vendor_valid(Model):
    def func(func):
        def wrapper(model_id, vendor_id, *args):
            if Model.objects.filter(id=model_id, vendor_id=vendor_id).exists():
                return func(model_id, vendor_id, *args)
            else:
                return False
        return wrapper
    return func


class CPUForm(forms.ModelForm):
    class Meta:
        model = CPU
        fields = ('vendor', 'architecture', 'model')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vend_id = set(CPU.objects.values_list('vendor_id', flat=True))
        choice = ((i, Vendor.objects.get(pk=i).vendor) for i in vend_id)
        self.fields['vendor'] = forms.ChoiceField(choices=choice)
        self.fields['architecture'] = forms.ChoiceField()
        self.fields['architecture'].widget.attrs.update({'id': 'id_cpu_architecture'})
        self.fields['model'] = forms.ChoiceField()
        self.fields['model'].widget.attrs.update({'id': 'id_cpu_model'})

    def is_valid(self):
        @model_valid(CPU)
        @vendor_valid(CPU)
        def architecture_valid(model_id, vendor_id, architecture_id):
            return CPU.objects.filter(id=model_id, architecture_id=architecture_id).exists()
        validity = architecture_valid(self.data['model'], self.data['vendor'], self.data['architecture'])
        return validity

    def clean(self):
        cpu_architecture = self.data.get('cpu_architecture')


class MotherboardForm(forms.ModelForm):
    class Meta:
        model = Motherboard
        fields = ('vendor', 'chipset', 'model')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chipset'] = forms.ChoiceField()
        self.fields['chipset'].widget.attrs.update({'id': 'id_motherboard_chipset'})
        self.fields['vendor'] = forms.ChoiceField()
        self.fields['vendor'].widget.attrs.update({'id': 'id_motherboard_vendor'})
        self.fields['model'] = forms.ChoiceField()
        self.fields['model'].widget.attrs.update({'id': 'id_motherboard_model'})

    def is_valid(self):
        @model_valid(Motherboard)
        @vendor_valid(Motherboard)
        def chipset_valid(model_id, vendor_id, chipset_id):
            return Motherboard.objects.filter(id=model_id, chipset_id=chipset_id).exists()
        validity = chipset_valid(self.data['model'], self.data['vendor'], self.data['chipset'])
        return validity


class PowerBlockForm(forms.ModelForm):
    class Meta:
        model = PowerBlock
        fields = ['model']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'] = forms.ChoiceField()
        self.fields['model'].widget.attrs.update({'id': 'id_pb_model'})

    def is_valid(self):
        @model_valid(PowerBlock)
        def true(model):
            return True
        validity = true(self.data['model'])
        return validity


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['volume', 'vendor', 'model']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['volume'] = forms.ChoiceField()
        self.fields['volume'].widget.attrs.update({'id': 'id_memory_volume'})
        self.fields['vendor'] = forms.ChoiceField()
        self.fields['vendor'].widget.attrs.update({'id': 'id_memory_vendor'})
        self.fields['model'] = forms.ChoiceField()
        self.fields['model'].widget.attrs.update({'id': 'id_memory_model'})

    def is_valid(self):
        @model_valid(Memory)
        @vendor_valid(Memory)
        def volume_valid(model_id, vendor_id, volume):
            return Memory.objects.filter(id=model_id, volume=volume).exists()
        validity = volume_valid(self.data['model'], self.data['vendor'], self.data['volume'])
        return validity
