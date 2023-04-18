from App.models import ContactForm
from App.database import db


def create_contact_form(name, phone, email, message):
    contact_form = ContactForm(name=name, phone=phone, email=email, message=message)
    if contact_form:
        db.session.add(contact_form)
        db.session.commit()
        return contact_form
    return None


def get_contact_form_by_id(id):
    contact_form = ContactForm.query.filter_by(id=id).first()
    if contact_form:
        return contact_form
    return None


def get_all_contact_forms():
    contact_forms = ContactForm.query.all()
    if contact_forms:
        return contact_forms
    return None


def get_all_contact_forms_json():
    contact_forms = get_all_contact_forms()
    if contact_forms:
        return [contact_form.to_json() for contact_form in contact_forms]
    return None


def delete_contact_form_by_id(id):
    contact_form = ContactForm.query.filter_by(id=id).first()
    if contact_form:
        db.session.delete(contact_form)
        db.session.commit()
        return True
    return False


def update_contact_form_by_id(id, name=None, phone=None, email=None, message=None):
    contact_form = ContactForm.query.filter_by(id=id).first()
    if contact_form:
        if name:
            contact_form.name = name
        if phone:
            contact_form.phone = phone
        if email:
            contact_form.email = email
        if message:
            contact_form.message = message
        db.session.add(contact_form)
        db.session.commit()
        return contact_form
    return False


def resolve_contact_form_by_id(id):
    contact_form = ContactForm.query.filter_by(id=id).first()
    if contact_form:
        contact_form.resolved = True
        db.session.add(contact_form)
        db.session.commit()
        return contact_form
    return False
