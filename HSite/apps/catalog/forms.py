from django import forms

from .models.cpu.cpu import CPU
from .models.motherboard.motherboard import Motherboard
from .models.memory.memory import Memory
from .models.power_block.power_block import PowerBlock


class CPUForm(forms.ModelForm):
    class Meta:
        model = CPU
        fields = ('vendor', 'architecture', 'model')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['architecture'] = forms.ChoiceField()
        self.fields['architecture'].widget.attrs.update({'id': 'id_cpu_architecture'})
        self.fields['model'] = forms.ChoiceField()
        self.fields['model'].widget.attrs.update({'id': 'id_cpu_model'})


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


class PowerBlockForm(forms.ModelForm):
    class Meta:
        model = PowerBlock
        fields = ['model']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['power_capacity'] = forms.ChoiceField()
        # self
        # self.fields['vendor'] = forms.ChoiceField()
        self.fields['model'] = forms.ChoiceField()
        self.fields['model'].widget.attrs.update({'id': 'id_pb_model'})


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

