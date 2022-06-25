from apifairy import authenticate, body, other_responses, response
from flask import abort

from . import journal_api_blueprint
from project.journal_api.schema import new_entry_schema, entry_schema, entries_schema
from project.models import Entry
from project import db, token_auth


@journal_api_blueprint.route('/', methods=['GET'])
@authenticate(token_auth)
@response(entries_schema)
def journal():
    """Return all journal entries"""
    user = token_auth.current_user()
    return Entry.query.filter_by(user_id=user.id).all()


@journal_api_blueprint.route('/', methods=['POST'])
@authenticate(token_auth)
@body(new_entry_schema)
@response(entry_schema, 201)
def add_journal_entry(kwargs):
    """Add a new journal entry"""
    user = token_auth.current_user()
    new_message = Entry(user_id=user.id, **kwargs)
    db.session.add(new_message)
    db.session.commit()
    return new_message


@journal_api_blueprint.route('/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(entry_schema)
@other_responses({403: 'Forbidden', 404: 'Entry not found'})
def get_journal_entry(id):
    """Return a single journal entry"""
    user = token_auth.current_user()
    entry = Entry.query.filter_by(id=id).first_or_404()

    if entry.user_id != user.id:
        abort(403)
    return entry


@journal_api_blueprint.route('/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@body(entry_schema)
@response(entry_schema)
@other_responses({403: 'Forbidden', 404: 'Entry not found'})
def update_journal_entry(id, data):
    """Update a journal entry"""
    user = token_auth.current_user()
    entry = Entry.query.filter_by(id=id).first_or_404()

    if entry.user_id != user.id:
        abort(403)

    entry.update(data['entry'])
    db.session.add(entry)
    db.session.commit()
    return entry


@journal_api_blueprint.route('/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({403: 'Forbidden', 404: 'Entry not found'})
def delete_journal_entry(id):
    """Delete a journal entry"""
    user = token_auth.current_user()
    entry = Entry.query.filter_by(id=id).first_or_404()

    if entry.user_id != user.id:
        abort(403)

    db.session.delete(entry)
    db.session.commit()
    return '', 204
