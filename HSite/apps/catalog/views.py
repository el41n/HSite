from django.shortcuts import render
from django.http import HttpResponse
from .models.cpu.cpu import CPU
from .models.cpu.architecture import Architecture
from .forms import MotherboardForm, MemoryForm, PowerBlockForm
from .models.memory.memory import Memory
from .models.hardware import Vendor
from .models.motherboard.chipset import Chipset
from .models.power_block.power_block import PowerBlock
from .forms import CPUForm
from django.views.generic import ListView
from .models.motherboard.motherboard import Motherboard
from .models.pc_set import PCSet
from .models.parser.parser import Parser


def index(request):
    p = Parser("https://komp.1k.by", "https://komp.1k.by/utility-cpu/")
    return HttpResponse('ok')


def main(request):
    cpu = CPU.objects.count()
    motherboard = Motherboard.objects.count()
    ram = Memory.objects.count()
    power = PowerBlock.objects.count()
    return render(request, 'main_page.html', context={'cpu': cpu, 'motherboard': motherboard, 'ram': ram,
                                                      'power': power})


def save_pc_form(request):
    if request.method == 'POST':
        models = request.POST.getlist('model')
        vendors = request.POST.getlist('vendor')
        cpu_date = {'model': models[0], 'architecture': request.POST.get('architecture'), 'vendor': vendors[0]}
        motherboard_date = {'model': models[1], 'vendor': vendors[1], 'chipset': request.POST.get('chipset')}
        memory_date = {'model': models[2], 'vendor': vendors[2], 'volume': request.POST.get('volume')}
        power_date = {'model': models[3]}
        cpu_form = CPUForm(cpu_date)
        moth_form = MotherboardForm(motherboard_date)
        memory_form = MemoryForm(memory_date)
        power_form = PowerBlockForm(power_date)
        if cpu_form.is_valid() and moth_form.is_valid() and memory_form.is_valid() and power_form.is_valid():
            pc_set = PCSet(cpu_id=models[0], motherboard_id=models[1], memory_id=models[2], power_id=models[3])
            response = pc_set.save()
            return render(request, 'form_response.html', {'response': response})
        return HttpResponse("Error")


def load_architectures(request):
    vendor_id = request.GET.get('vendor')
    architecture = Architecture.objects.filter(cpu__vendor=vendor_id)
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


def load_memory_volume(request):
    info = request.GET.get('vendor')
    mem_type = Motherboard.objects.get(pk=info).memory_type
    volumes = set(Memory.objects.filter(type=mem_type).values_list('volume', flat=True))
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


class PCSetView(ListView):
    model = PCSet
    template_name = 'set_list.html'

