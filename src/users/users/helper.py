from users.records.record import Record


def to_class(class_obj, query):
    return class_obj(**query) if query else None


def save_to_db(data):
    return Record.save(data)


def update_db(field_id_to_find, field_id_value, data):
    Record.Update.update(field_id_to_find, field_id_value, data)
