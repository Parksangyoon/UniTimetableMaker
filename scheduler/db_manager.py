def get_from_db(db_model):

    result_from_db = []

    for data in db_model.objects.all():
        result_from_db.append(data.get_model())

    return result_from_db


def set_db_data(db_model, data):
    row_num = 0
    for insert in data:
        db_model.set_model(db_model, insert)
        row_num += 1
