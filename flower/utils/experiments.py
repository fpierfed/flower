"""
Experiment Related Views

This module contains functionality to fetch experiments form the application DB.
"""
import datetime
import time


def iter_experiments(app, limit=None, type=None, worker=None, state=None,
                     sort_by=None, received_start=None, received_end=None,
                     started_start=None, started_end=None):
    i = 0
    experiments = app.db.experiments_by_timestamp()
    if sort_by is not None:
        experiments = sort_experiments(experiments, sort_by)
    convert = lambda x: time.mktime(
        datetime.datetime.strptime(x, '%Y-%m-%d %H:%M').timetuple()
    )

    for uuid, experiment in experiments:
        if type and experiment.name != type:
            continue
        if worker and experiment.worker and \
           experiment.worker.hostname != worker:
            continue
        if state and experiment.state != state:
            continue
        if received_start and experiment.received < convert(received_start):
            continue
        if received_end and experiment.received > convert(received_end):
            continue
        if started_start and experiment.started < convert(started_start):
            continue
        if started_end and experiment.started > convert(started_end):
            continue

        yield uuid, experiment
        i += 1
        if i == limit:
            break


def sort_experiments(experiments, sort_by):
    assert sort_by.lstrip('-') in ('name', 'state', 'received', 'started')
    reverse = False
    if sort_by.startswith('-'):
        sort_by = sort_by.lstrip('-')
        reverse = True
    for experiment in sorted(experiments, key=lambda x: getattr(x[1], sort_by),
                             reverse=reverse):
        yield experiment


def get_experiment_by_id(app, experiment_id):
    return app.db.experiment_by_id(experiment_id)
