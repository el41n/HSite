from django.urls import path
from . import views
from .views import MotherboardView


urlpatterns = (
    path('', views.index, name='index'),
    path('Catalog/', views.main, name='main'),
    path('Catalog/ProcessorList/', views.ProcessorList.as_view(), name='processor_list'),
    path('Catalog/MotherboardList/', views.MotherboardView.as_view(), name='motherboard_list'),
    path('Catalog/MemoryList/', views.MemoryView.as_view(), name='memory_list'),
    path('Catalog/PowerList/', views.PowerView.as_view(), name='power_list'),
    path('Catalog/BuildList/', views.PCSetView.as_view(), name = 'build_list'),

    path('Catalog/Build/Save', views.save_pc_form,
         name='save_cpu'),

    # path('Catalog/MemoryList/', views.processor_list, name='memory_list'),
    # path('Catalog/PowerBlockList/', views.processor_list, name='power_block_list'),
    path('Catalog/Build/', views.build, name='build'),


    path('Catalog/Build/ajax/load-models/', views.load_models, name='ajax_load_models'),
    path('Catalog/Build/ajax/load-architectures/', views.load_architectures, name='ajax_load_architectures'),

    path('Catalog/Build/ajax/load-motherboard-vendors/', views.load_motherboard_vendors,
         name='ajax_load_motherboard_models'),
    path('Catalog/Build/ajax/load-motherboard-chipsets/', views.load_motherboard_chipsets,
         name='ajax_load_motherboard_chipsets'),
    path('Catalog/Build/ajax/load-motherboard-models/', views.load_motherboard_models,
         name='ajax_load_motherboard_models'),

    path('Catalog/Build/ajax/load-memory-volume/', views.load_memory_volume,
         name='ajax_load_memory_volume'),
    path('Catalog/Build/ajax/load-memory-vendors/', views.load_memory_vendors,
         name='ajax_load_memory_vendors'),
    path('Catalog/Build/ajax/load-memory-models/', views.load_memory_models,
         name='ajax_load_memory_models'),
    #
    # path('Catalog/Build/ajax/load-power-capacity/', views.load_power_capacity,
    #      name='ajax_load_power_capacity'),
    # # path('Catalog/Build/ajax/load-power-vendors/', views.load_power_vendors,
    # #      name='ajax_load_power_vendors'),
    path('Catalog/Build/ajax/load-power-models/', views.load_power_models,
         name='ajax_load_power_models'),
)

