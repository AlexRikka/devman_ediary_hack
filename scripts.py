from datacenter.models import Schoolkid, Lesson
from datacenter.models import Chastisement, Commendation, Mark
import random


def get_child(schoolkid_name):
    try:
        kid = Schoolkid.objects.filter(
            full_name__contains=schoolkid_name).get()
    except Schoolkid.DoesNotExist:
        raise Exception("Такого ученика не существует.")
    except Schoolkid.MultipleObjectsReturned:
        raise Exception('Существует несколько учеников с таким именем.')
    return kid


def fix_marks(schoolkid_name):
    child = get_child(schoolkid_name)
    bad_marks = Mark.objects.filter(schoolkid__id=child.id,
                                    points__in=[2, 3])
    bad_marks.update(points=5)


def remove_chastisements(schoolkid_name):
    child = get_child(schoolkid_name)
    Chastisement.objects.filter(schoolkid__id=child.id).delete()


def create_commendation(schoolkid_name, subject_title):
    child = get_child(schoolkid_name)
    child_lessons = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subject_title).order_by('date')
    lesson = child_lessons.first()
    with open('commendations.txt', encoding='utf-8') as f:
        commendations = f.read().splitlines()
    comm_text = random.choice(commendations)
    Commendation.objects.create(schoolkid=child,
                                created=lesson.date,
                                subject=lesson.subject,
                                teacher=lesson.teacher,
                                text=comm_text)
