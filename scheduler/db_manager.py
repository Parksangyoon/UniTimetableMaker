def get_from_db(db_model, company_id):
    result_from_db = []

    for data in db_model.objects.filter(company_id=company_id):
        result_from_db.append(data.get_model())

    return result_from_db


def set_db_data(db_model, data):
    for insert in data:
        db_model.set_model(db_model, insert)


def update_db_from(db_model, company_id, data_list):

    for data in data_list:
        db_model.update_model(data, company_id)
