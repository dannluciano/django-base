from django_tasks import task


@task()
def calculate_meaning_of_life() -> int:
    return 42


@task()
def calculate_complex_task() -> None:
    import time

    time.sleep(10)
