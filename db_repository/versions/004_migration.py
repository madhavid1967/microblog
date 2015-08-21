from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer__comments = Table('answer__comments', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('answercommenttext', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER, nullable=False),
    Column('post_id', INTEGER, nullable=False),
    Column('answer_id', INTEGER, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer__comments'].columns['post_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer__comments'].columns['post_id'].create()
