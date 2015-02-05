"""
The rest of flower uses the Celery data model as is. Since we are extending that
with the Experiment type, we put those type definitions here.
"""


def experiment_types():
    return sorted(set('L95', ))
