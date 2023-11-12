from datacenter.models import Schoolkid, Lesson
from datacenter.models import Chastisement, Commendation, Mark
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random


def fix_marks(schoolkid_name):
    try:
        child = Schoolkid.objects.filter(
            full_name__contains=schoolkid_name).get()
        bad_marks = Mark.objects.filter(schoolkid__id=child.id,
                                        points__in=[2, 3])
        bad_marks.update(points=5)
    except ObjectDoesNotExist:
        print("Такого ученика не существует.")
    except MultipleObjectsReturned:
        print('Существует несколько учеников с таким именем.')


def remove_chastisements(schoolkid_name):
    try:
        child = Schoolkid.objects.filter(
            full_name__contains=schoolkid_name).get()
        Chastisement.objects.filter(schoolkid__id=child.id).delete()
    except ObjectDoesNotExist:
        print("Такого ученика не существует.")
    except MultipleObjectsReturned:
        print('Существует несколько учеников с таким именем.')


def create_commendation(schoolkid_name, subject_title):
    try:
        child = Schoolkid.objects.filter(
            full_name__contains=schoolkid_name).get()
        child_lessons = Lesson.objects.filter(
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
            subject__title=subject_title)
        lesson = random.choice(child_lessons)
        with open('commendations.txt', encoding='utf-8') as f:
            commendations = f.read().splitlines()
        comm_text = random.choice(commendations)
        Commendation.objects.create(schoolkid=child,
                                    created=lesson.date,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher,
                                    text=comm_text)
    except ObjectDoesNotExist:
        print("Такого ученика не существует.")
    except MultipleObjectsReturned:
        print('Существует несколько учеников с таким именем.')
