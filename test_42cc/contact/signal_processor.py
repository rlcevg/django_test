from contact.models import ActionDBModel
from datetime import datetime


ACTION_DB_UNIQUE_ID = '{0}_{1}_action_db_unique_id'.format(
    ActionDBModel.__module__, ActionDBModel.__name__
)


def model_action_save(sender, **kwargs):
    if not isinstance(sender, ActionDBModel):
        if kwargs['created']:
            act = 'create'
        else:
            act = 'edit'
        action = ActionDBModel(
            model='{0}.{1}'.format(
                sender.__module__,
                sender.__name__
            )
            action=act,
            time=datetime.now(),
#            user=
        )
        action.save()


def model_action_delete(sender, **kwargs):
    if not isinstance(sender, ActionDBModel):
        act = 'del'
        action = ActionDBModel(
            model='{0}.{1}'.format(
                sender.__module__,
                sender.__name__
            )
            action=act,
            time=datetime.now(),
#            user=
        )
        action.save()
