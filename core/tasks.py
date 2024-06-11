from django_tasks import task


@task()
def calculate_meaning_of_life() -> int:
    return 42
