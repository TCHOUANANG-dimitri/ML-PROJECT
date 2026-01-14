import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enspd_ai.settings')
django.setup()

from core.models import Room, Teacher

# Create sample rooms
Room.objects.all().delete()
r1 = Room.objects.create(id=1, name="Amphi A", capacity=220)
r2 = Room.objects.create(id=2, name="Amphi B", capacity=180)
r3 = Room.objects.create(id=3, name="Salle Info 1", capacity=40)
print(f"Rooms created: {Room.objects.count()}")

# Create sample teachers
Teacher.objects.all().delete()
t1 = Teacher.objects.create(id=1, name="Dr. N. Talla", matricule="ENS-001", speciality="IA", hours_planned=120, hours_done=0)
t2 = Teacher.objects.create(id=2, name="Pr. M. Mbarga", matricule="ENS-002", speciality="Maths", hours_planned=160, hours_done=0)
print(f"Teachers created: {Teacher.objects.count()}")
print("Done!")
