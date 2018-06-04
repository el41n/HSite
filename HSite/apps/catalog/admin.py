from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models.cpu.cpu import CPU
from .models.cpu.architecture import Architecture
from .models.cpu.codename import CodeName
from .models.motherboard.motherboard import Motherboard
from .models.motherboard.socket import Socket
from .models.motherboard.chipset import Chipset
from .models.motherboard.form_factor import FormFactor
from .models.memory.memory import Memory
from .models.memory.memory_type import MemoryType
from .models.hardware import Vendor
from .models.power_block.power_block import PowerBlock
from .models.pc_set import PCSet


class ChipsetAdmin(admin.ModelAdmin):
    pass

class FormFactorAdmin(admin.ModelAdmin):
    pass

class VendorAdmin(admin.ModelAdmin):
    pass

class MemoryAdmin(admin.ModelAdmin):
    pass

class MemoryTypeAdmin(admin.ModelAdmin):
    pass

class CPUAdmin(admin.ModelAdmin):
    pass

class ArchitectureAdmin(admin.ModelAdmin):
    pass


class CodeNameAdmin(admin.ModelAdmin):
    pass


class MotherboardAdmin(admin.ModelAdmin):
    pass


class SocketAdmin(admin.ModelAdmin):
    pass

from .models.hardware import Hardware


class HardwareAdmin(admin.ModelAdmin):
    pass


class PowerBlockAdmin(admin.ModelAdmin):
    pass


class PCSetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hardware, HardwareAdmin)
admin.site.register(CPU, CPUAdmin)
admin.site.register(Architecture, ArchitectureAdmin)
admin.site.register(CodeName, CodeNameAdmin)
admin.site.register(Motherboard, MotherboardAdmin)
admin.site.register(Socket, SocketAdmin)
admin.site.register(Chipset, ChipsetAdmin)
admin.site.register(FormFactor, FormFactorAdmin)
admin.site.register(MemoryType, MemoryTypeAdmin)
admin.site.register(Memory, MemoryAdmin)

admin.site.register(Vendor, VendorAdmin)

admin.site.register(PowerBlock, PowerBlockAdmin)

admin.site.register(PCSet, PCSetAdmin)





#admin.site.register(models)
