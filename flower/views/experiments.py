from __future__ import absolute_import

import copy
try:
    from itertools import imap
except ImportError:
    imap = map

import celery

from tornado import web

from ..views import BaseHandler
from ..utils.experiments import iter_experiments, get_experiment_by_id
from .. import models


class ExperimentView(BaseHandler):
    @web.authenticated
    def get(self, experiment_id):
        experiment = get_experiment_by_id(self.application, experiment_id)
        if experiment is None:
            raise web.HTTPError(404, "Unknown experiment '%s'" % experiment_id)

        self.render("experiment.html", experiment=experiment)


class ExperimentsView(BaseHandler):
    @web.authenticated
    def get(self):
        app = self.application
        capp = self.application.capp
        limit = self.get_argument('limit', default=None, type=int)
        worker = self.get_argument('worker', None)
        type = self.get_argument('type', None)
        state = self.get_argument('state', None)
        sort_by = self.get_argument('sort', None)
        received_start = self.get_argument('received-start', None)
        received_end = self.get_argument('received-end', None)
        started_start = self.get_argument('started-start', None)
        started_end = self.get_argument('started-end', None)

        worker = worker if worker != 'All' else None
        type = type if type != 'All' else None
        state = state if state != 'All' else None

        experiments = iter_experiments(app, limit=limit, type=type,
                                       worker=worker, state=state,
                                       sort_by=sort_by,
                                       received_start=received_start,
                                       received_end=received_end,
                                       started_start=started_start,
                                       started_end=started_end)
        experiments = imap(self.format_experiment, experiments)
        workers = app.events.state.workers
        seen_experiment_types = models.experiment.experiment_types()
        time = 'natural-time' if app.options.natural_time else 'time'
        if capp.conf.CELERY_TIMEZONE:
            time += '-' + capp.conf.CELERY_TIMEZONE
        params = {k: v[-1] for k, v in self.request.query_arguments.items()}

        self.render("experiments.html", experiments=experiments,
                    experiment_types=seen_experiment_types,
                    all_states=celery.states.ALL_STATES,
                    workers=workers,
                    limit=limit,
                    worker=worker,
                    type=type,
                    state=state,
                    time=time,
                    sort_by=sort_by,
                    params=params,
                    received_start=received_start,
                    received_end=received_end,
                    started_start=started_start,
                    started_end=started_end)

    def format_experiment(self, args):
        uuid, experiment = args
        custom_format_experiment = self.application.options.format_experiment

        if custom_format_experiment:
            experiment = custom_format_experiment(copy.copy(experiment))
        return uuid, experiment
