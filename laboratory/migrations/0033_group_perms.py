# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-28 14:49
from __future__ import unicode_literals

from django.db import migrations

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from django.db import migrations


def set_perms(group,perms):
    if not hasattr(perms,'__iter__'):
         group.permissions.add(perms)
    else:
         for perm in perms:
            group.permissions.add(perm)
    
    
def load_group_perms(apps, schema_editor):
  
    perms_student =[ # reservations
        "add_reservation","view_reservation",
        ]
    
    perms_professor = [  # reservations
        "add_reservation","view_reservation",
        # Procedure
        "view_procedure","view_procedurestep","view_procedurerequiredobject",
        "view_procedureobservations","add_procedureobservations","change_procedureobservations",
        "delete_procedureobservations","add_procedure","change_procedure","delete_procedure","add_procedurestep",
        "change_procedurestep","delete_procedurestep","add_procedurerequiredobject","change_procedurerequiredobject",
        "delete_procedurerequiredobject",
        ]
        
    perms_laboratory = [ # reservations
        "add_reservation","change_reservation","delete_reservation","add_reservationtoken",
        "change_reservationtoken","delete_reservationtoken","view_reservation",
        
        # objets 
        "add_shelfobject","change_shelfobject","delete_shelfobject",
        "add_object","change_object","delete_object","add_objectfeatures",
        "change_objectfeatures","delete_objectfeatures","view_procedurerequiredobject",
        "add_procedurerequiredobject","change_procedurerequiredobject","delete_procedurerequiredobject",
        
        # muebles
        "add_furniture","change_furniture","delete_furniture",

        ]

        
    
    GLaboratory = Group(name='Laboratory Administrator')
    GLaboratory.save()
    GProfessor = Group(name='Professor')
    GProfessor.save()
    GStudent = Group(name='Student')
    GStudent.save()
 
    
    # add perms to student
    # puede ver y hacer reservaciones
    perms = Permission.objects.filter(codename__in=perms_student)
    set_perms(GStudent,perms)
    
    # add perms to Professor
    # 1. Puede hacer reservaciones
    # 2. Puede administrar procedientos
    # (3). No aprueba reservaciones
    # 4. Puede calcular soluciones
    perms = Permission.objects.filter(codename__in=perms_professor)
    set_perms(GProfessor,perms)   
    # add perms to Laboratories Administrator    
    # 1. Puede administrar reservaciones
    # 2. Agregar Objectos
    # 3. Agregar stantes
    # 4. Administrar estructura de lab
    perms=Permission.objects.filter(codename__in=perms_laboratory)
    set_perms(GLaboratory,perms)   
    


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0032_auto_20180216_1502'),
    ]

    operations = [
         migrations.RunPython(load_group_perms),
    ]