# mlnbook_backend
newborn's multi language book

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).


## 启动服务

同时启动的客户端和服务端

> /admin/dev_mlnbook/mlnbook_backend/venv/bin/supervisord -c /admin/dev_mlnbook/mlnbook_backend/supervisor.conf


进入客户端

> /admin/dev_mlnbook/mlnbook_backend/venv/bin/supervisorctl -c /admin/dev_mlnbook/mlnbook_backend/supervisor.conf

重新加载(默认重启)

> /admin/dev_mlnbook/mlnbook_backend/venv/bin/supervisorctl -c /admin/dev_mlnbook/mlnbook_backend/supervisor.conf reload

重启失败，进程未杀死时。手动kill

> ps -ef | grep 'miniconda3/bin/python' | grep -v grep | awk '{print $2}' | xargs kill

查看某端口占用进程
> lsof -i:2022
> kill -9 xxxxx



## redis

windows可以使用 https://github.com/zkteco-home/redis-windows 直接启动redis.

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

- mlnbook: MLN$2023

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy mlnbook_backend

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd mlnbook_backend
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd mlnbook_backend
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd mlnbook_backend
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

