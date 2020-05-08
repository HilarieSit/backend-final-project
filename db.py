from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# association tables
clubs_events_assoc = db.Table('clubs_events_assoc', db.Model.metadata,
    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

clubs_admins_assoc = db.Table('clubs_admins_assoc', db.Model.metadata,
    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

clubs_members_assoc = db.Table('clubs_members_assoc', db.Model.metadata,
    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

events_users_assoc = db.Table('events_user_assoc', db.Model.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

tasks_users_assoc = db.Table('tasks_user_assoc', db.Model.metadata,
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin_clubs = db.relationship('Club', secondary=clubs_admins_assoc, back_populates='admins')
    member_clubs = db.relationship('Club', secondary=clubs_members_assoc, back_populates='members')
    events = db.relationship('Event', secondary=events_users_assoc, back_populates='users')
    tasks = db.relationship('Task', back_populates='users')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')

    def serialize(self):
        all_clubs = [a.serialize() for a in self.admin_clubs]
        all_clubs.extend([m.serialize() for m in self.member_clubs])
        serialized_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'clubs': all_clubs,
            'events': [e.serialize() for e in self.events],
            'tasks': [t.serialize() for u in self.tasks],
        }
        for item in removed_item:
            serialized_dict.pop(item)
        return serialized_dict

class Club(db.Model):
    """ many-to-many users
        many-to-many events """
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    events = db.relationship('Event', secondary=clubs_events_assoc, back_populates='clubs')
    admins = db.relationship('User', secondary=clubs_admins_assoc, back_populates='admin_clubs')
    members = db.relationship('User', secondary=clubs_members_assoc, back_populates='member_clubs')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')

    def serialize(self):
        serialized_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.discription,
            'events': [e.serialize_no_course() for e in self.events],
            'admins': [a.serialize_no_course() for a in self.admins],
            'members': [m.serialize_no_course() for m in self.members]
        }
        for item in removed_item:
            serialized_dict.pop(item)
        return serialized_dict

class Events(db.Model):
    """ many-to-many clubs
        many-to-many users
        one-to-many tasks """
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    budget = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, nullable=False)
    tasks = db.relationship('Task', cascade='delete')
    clubs = db.relationship('Club', secondary=clubs_events_assoc, back_populates='events')
    users = db.relationship('User', secondary=events_users_assoc, back_populates='events')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.date = kwargs.get('date', '')
        self.budget = kwargs.get('budget', '')
        self.active = kwargs.get('active', '')

    def serialize(self):
        serialized_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.discription,
            'date': self.date,
            'budget': self.budget,
            'active': self.active,
            'tasks': [t.serialize_no_course() for t in self.tasks],
            'clubs': [c.serialize_no_course() for c in self.clubs],
            'users': [u.serialize_no_course() for u in self.users],
        }
        for item in removed_item:
            serialized_dict.pop(item)
        return serialized_dict

class Task(db.Model):
    """ 1-many with events
        many-many with users """
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    budget = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", back_populates="tasks")
    users = db.relationship('User', secondary=tasks_users_assoc, back_populates='tasks')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.date = kwargs.get('date', '')
        self.budget = kwargs.get('budget', '')
        self.active = kwargs.get('active', '')

    def serialize(self, removed_item):
        serialized_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.discription,
            'date': self.date,
            'budget': self.budget,
            'active': self.active,
            'event': self.event
            'users': [u.serialize() for u in self.users],
        }
        for item in removed_item:
            serialized_dict.pop(item)
        return serialized_dict

class RequestAdd(db.Model):
    __tablename__ = 'requestadd'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    message = db.Column(db.String)
    accepted = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id', '')
        self.club_id = kwargs.get('club_id', '')
        self.event_id = kwargs.get('event_id', '')
        self.task_id = kwargs.get('task_id', '')
        self.message = kwargs.get('message', '')
        self.accepted = kwargs.get('active', '')

    def serialize(self, removed_item):
        serialized_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'club_id': self.club_id,
            'event_id': self.event_id,
            'task_id': self.task_id,
            'message': self.message,
            'active': self.active
        }
        for item in removed_item:
            serialized_dict.pop(item)
        return serialized_dict
