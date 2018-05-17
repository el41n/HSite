from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models.cpu.cpu import CPU
from .models.cpu.architecture import Architecture
from .models.parser.intel_parser import IntelParser
from .forms import CPUForm, MotherboardForm, MemoryForm, PowerBlockForm
from .models.memory.memory import Memory
from .models.hardware import Hardware, Vendor
from .models.motherboard.chipset import Chipset
from .models.power_block.power_block import PowerBlock

from django.views.generic import ListView
from .models.motherboard.motherboard import Motherboard

import pdb
# Create your views here.


def index(request):
    a = Architecture.objects.filter(id=2).values_list('id', flat=True)
    print(a[0])
    return HttpResponse('ok')


def main(request):
    cpu = CPU.objects.count()
    motherboard = Motherboard.objects.count()
    ram = Memory.objects.count()
    power = PowerBlock.objects.count()
    return render(request, 'main_page.html', context={'cpu': cpu, 'motherboard': motherboard, 'ram': ram,
                                                      'power': power})


def load(function):
    def wrapper(request):
        info = request.GET.get('vendor')
        return function(request, info)
    return wrapper


def load_architectures(request):
    vendor_id = request.GET.get('vendor')
    architecture = Architecture.objects.all().filter(cpu__vendor=vendor_id)
    architecture = set(architecture)
    return render(request, 'dropdown_architecture_list_options.html', {'architectures': architecture})


def load_models(requset):
    architecture_id = requset.GET.get('architecture')
    models = CPU.objects.filter(architecture_id=architecture_id).order_by('model')
    return render(requset, 'dropdown_model.html', {'models': models})


def load_motherboard_vendors(request):
    model_id = request.GET.get('model')
    socket_id = CPU.objects.get(pk=model_id).socket_id
    motherboard_vendors = Motherboard.objects.filter(socket_id=socket_id)
    v = set(Vendor.objects.filter(hardware__in=motherboard_vendors))
    return render(request, 'dropdown_vendor.html', {'vendors': v})


def load_motherboard_chipsets(request):
    vendor_id = request.GET.get('vendor')
    socket = CPU.objects.get(pk=request.GET.get('cpu')).socket_id
    chipsets_list = Motherboard.objects.filter(vendor_id=vendor_id, socket_id=socket).values_list('chipset', flat=True)
    chipsets = Chipset.objects.filter(pk__in=chipsets_list)
    return render(request, 'dropdown_motherboard_chipset_list_options.html', {'chipsets': chipsets})


def load_motherboard_models(request):
    chipset_id = request.GET.get('chipset')
    vendor = request.GET.get('vendor')
    models = Motherboard.objects.filter(vendor=vendor, chipset_id=chipset_id).order_by('model')
    return render(request, 'dropdown_model.html', {'models': models})

# def processor_list(request):
#     a = IntelArchitecture.objects.all().values_list('architecture', flat=True)
#     str = 'Ivy Bridge'
#     b = list(filter(lambda x: x == str, a))
#     ivy = IntelArchitecture.objects.get(architecture=b[0]).id
#     cp = IntelCPU.objects.all()
#     return render(request, 'processor_list.html', context={'processors': cp})

@load
def load_memory_volume(request, info):
    mem_type = Motherboard.objects.get(pk=info).memory_type
    volumes = Memory.objects.filter(type=mem_type)
    return render(request, 'dropdown_memory_volume.html', {'memories': volumes})


def load_memory_vendors(request):
    volume = request.GET.get('vendor')
    type = Motherboard.objects.get(pk=request.GET.get('type')).memory_type
    vendors = Memory.objects.filter(volume=volume, type=type)
    vend = set()
    for ve in vendors:
        vend.add(ve.vendor.id)
    v = Vendor.objects.all().filter(pk__in=vend)
    return render(request, 'dropdown_vendor.html', {'vendors': v})


def load_memory_models(request):
    vendor = request.GET.get('vendor')
    type = Motherboard.objects.get(pk=request.GET.get('type')).memory_type
    volume = request.GET.get('volume')
    models = Memory.objects.filter(volume=volume, vendor=vendor, type=type)
    return render(request, 'dropdown_model.html', {'models': models})

# def load_power_capacity(request):
#     pass
#
# # def load_power_vendors(request):
# #     pass


def load_power_models(request):
    cpu = request.GET.get('cpu')
    motherboard = request.GET.get('motherboard')
    memory = request.GET.get('memory')
    power = 0
    power += CPU.objects.all().get(pk=cpu).power
    power += Motherboard.objects.all().get(pk=motherboard).power
    power += Memory.objects.all().get(pk=memory).power

    power_models = PowerBlock.objects.all().filter(power_capacity__in=range(power, 4000))

    return render(request, 'dropdown_model.html', context={'models': power_models})


def build(request):
    cpu_form = CPUForm()
    moth_form = MotherboardForm()
    mem_form = MemoryForm()
    pb_form = PowerBlockForm()
    return render(request, 'build1.html', context={'cpu_form': cpu_form, 'moth_form': moth_form,
                                                   'mem_form': mem_form, 'pb_form': pb_form})


class ProcessorList(ListView):
    model = CPU
    template_name = 'processor_list.html'


class MotherboardView(ListView):
    model = Motherboard
    template_name = 'motherboard_list.html'


class MemoryView(ListView):
    model = Memory
    template_name = 'memory_list.html'


class PowerView(ListView):
    model = PowerBlock
    template_name = 'power_list.html'
