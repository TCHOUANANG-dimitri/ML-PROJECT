from django.db import models


class Filiere(models.Model):
  code = models.CharField(max_length=20, unique=True)
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.code


class Subject(models.Model):
  filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="subjects")
  name = models.CharField(max_length=150)
  level = models.PositiveSmallIntegerField()
  speciality = models.CharField(max_length=100, blank=True)
  hours_cm = models.PositiveSmallIntegerField(default=0)
  hours_td = models.PositiveSmallIntegerField(default=0)
  hours_tp = models.PositiveSmallIntegerField(default=0)

  def __str__(self):
    return f"{self.name} ({self.filiere.code} L{self.level})"


class Room(models.Model):
  name = models.CharField(max_length=100, unique=True)
  capacity = models.PositiveIntegerField()

  def __str__(self):
    return self.name


class Teacher(models.Model):
  matricule = models.CharField(max_length=50, unique=True)
  name = models.CharField(max_length=100)
  filieres = models.CharField(max_length=200)
  subjects = models.CharField(max_length=300)
  speciality = models.CharField(max_length=100, blank=True)
  hours_planned = models.FloatField(default=0)
  hours_done = models.FloatField(default=0)

  @property
  def hours_remaining(self):
    return max(self.hours_planned - self.hours_done, 0)

  def __str__(self):
    return self.name


class TimetableEntry(models.Model):
  DAY_CHOICES = [
      ("Lundi", "Lundi"),
      ("Mardi", "Mardi"),
      ("Mercredi", "Mercredi"),
      ("Jeudi", "Jeudi"),
      ("Vendredi", "Vendredi"),
      ("Samedi", "Samedi"),
  ]

  SLOT_CHOICES = [
      ("AM", "07h30 – 11h30"),
      ("PM", "12h30 – 16h30"),
  ]

  day = models.CharField(max_length=10, choices=DAY_CHOICES)
  slot = models.CharField(max_length=2, choices=SLOT_CHOICES)
  filiere = models.CharField(max_length=50)
  level = models.PositiveSmallIntegerField()
  subject = models.CharField(max_length=150)
  session_type = models.CharField(max_length=2, choices=[("CM", "CM"), ("TD", "TD"), ("TP", "TP")])
  room = models.ForeignKey(Room, on_delete=models.PROTECT)
  teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
  date = models.DateField()
  capacity = models.PositiveIntegerField(default=0)

  class Meta:
    unique_together = [("day", "slot", "room"), ("day", "slot", "teacher")]

  def __str__(self):
    return f"{self.subject} {self.day} {self.slot}"