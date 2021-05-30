from celery.schedules import crontab

from todo.core.celery_app import celery_app


@celery_app.on_after_configure.connect
def setup_repeated_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, test.s('world'), expires=10)

    sender.add_periodic_task(
        crontab(hour=14, minute=30),
        test.s('It is repeated task')
    )
    print('heressssssss')


@celery_app.task
def test(arg):
    print('here')
    print(arg)
    with open('liza.txt', 'w') as f:
        f.write(arg)
