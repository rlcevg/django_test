from contact.models import ActionDBModel, HttpRequestLog
from datetime import datetime
from django.db.models.signals import post_save, post_delete


MODEL_TRACKER_IGNORE = (ActionDBModel, HttpRequestLog)
ACTION_DB_UNIQUE_ID = '{0}_{1}_action_db_unique_id'.format(
    ActionDBModel.__module__,
    ActionDBModel.__name__
)


def model_action_save(sender, **kwargs):
    if not issubclass(sender, MODEL_TRACKER_IGNORE):
        if kwargs['created']:
            act = ActionDBModel.ACTION_CREATE
        else:
            act = ActionDBModel.ACTION_EDIT
        action = ActionDBModel(
            model='{0}.{1}'.format(
                sender.__module__,
                sender.__name__
            ),
            action=act,
            time=datetime.now(),
#            user=
        )
        action.save()


def model_action_delete(sender, **kwargs):
    if not issubclass(sender, MODEL_TRACKER_IGNORE):
        act = ActionDBModel.ACTION_DELETE
        action = ActionDBModel(
            model='{0}.{1}'.format(
                sender.__module__,
                sender.__name__
            ),
            action=act,
            time=datetime.now(),
#            user=
        )
        action.save()


def start_signal_processor():
    post_save.connect(
        model_action_save,
        dispatch_uid=ACTION_DB_UNIQUE_ID
    )
    post_delete.connect(
        model_action_delete,
        dispatch_uid=ACTION_DB_UNIQUE_ID
    )
