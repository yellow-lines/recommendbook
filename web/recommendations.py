import pandas as pd


def get_registr_table_userid(login_, connection):
    zapros_to_name = 'select * from registr_table where "login" = ' + "'" + login_ + "'"
    info_user = pd.read_sql(zapros_to_name, connection)
    userid = info_user.iloc[0]['userid']
    return userid


def get_id_exp1(login_, connection):
    id_reader = get_registr_table_userid(login_, connection)
    zapros_to_id_exp = 'select * from exp_reader_id where "readerID" = ' + \
        str(int(id_reader))
    exp = pd.read_sql(zapros_to_id_exp, connection)
    exp_one_reader = exp.iloc[0, 2:].dropna().astype(int)
    list_exp = list(exp_one_reader.unique())
    exp_reader = tuple(list_exp)
    zapros_to_id_books1 = 'select "Object_1" from knowledge_base where "Object_1" in ' + \
        str(exp_reader) + 'OR "Object_2" in ' + str(exp_reader)
    zapros_to_id_books2 = 'select "Object_2" from knowledge_base where "Object_1" in ' + \
        str(exp_reader) + 'OR "Object_2" in ' + str(exp_reader)
    book_info1 = pd.read_sql(zapros_to_id_books1, connection)
    book_info2 = pd.read_sql(zapros_to_id_books2, connection)
    book_info2.rename(columns={'Object_2': 'Object_1'}, inplace=True)
    book_info = list(
        pd.concat([book_info1, book_info2], ignore_index=True).Object_1.unique())
    id_books = tuple(list(set(book_info) - set(list_exp)))
    zapros_to_id_book = 'select * from stockstats_cat where "recId" in ' + \
        str(id_books)
    book_info = pd.read_sql(zapros_to_id_book, connection)
    return book_info


def get_id_exp2(lgn, connection):
    id_reader = get_registr_table_userid(lgn, connection)
    zapros_to_id_exp = 'select * from exp_reader_id where "readerID" = ' + \
        str(int(id_reader))
    exp = pd.read_sql(zapros_to_id_exp, connection)
    exp_one_reader = exp.iloc[0, 2:].dropna().astype(int)
    list_exp = list(exp_one_reader.unique())
    exp_reader = tuple(list_exp)
    zapros_to_id_books1 = 'select * from knowledge_base where "Object_1" in ' + \
        str(exp_reader) + 'OR "Object_2" in ' + str(exp_reader)
    book_info1 = pd.read_sql(zapros_to_id_books1, connection).drop_duplicates()
    zapros_to_id_books_obj1 = 'select "aut", "title", "recId" from stockstats_cat where "recId" in ' + \
        str(tuple(book_info1.Object_1)) + 'OR "recId" in ' + \
        str(tuple(book_info1.Object_2))
    book_info_obj1 = pd.read_sql(zapros_to_id_books_obj1, connection)

    book_info_obj1.aut.replace({None: 'Автор неизвестен'}, inplace=True)
    book_info_obj1.title.replace({None: 'Название неизвестно'}, inplace=True)
    book_info_obj1['Source'] = book_info_obj1[book_info_obj1.columns[:2]].apply(
        lambda x: ', '.join(x.astype(str)), axis=1)
    book_info_obj1.drop(columns=['aut', 'title'], inplace=True)
    book_info1.rename(columns={'Object_1': 'recId'}, inplace=True)
    book_info1 = book_info1.merge(book_info_obj1, on=["recId"])

    book_info1.drop(columns=['index', 'recId'], inplace=True)

    book_info_obj1.rename(
        columns={'Source': 'Target', 'recId': 'Object_2'}, inplace=True)
    book_info1 = book_info1.merge(book_info_obj1, on=["Object_2"])
    book_info1.drop(columns=['Object_2'], inplace=True)
    book_info1.rename(columns={'val': 'Weight'}, inplace=True)

    return book_info1


def get_history_data(login_, connection):
    id_reader = get_registr_table_userid(login_, connection)
    zapros_to_id_exp = 'select * from exp_reader_id where "readerID" = ' + \
        str(int(id_reader))
    exp = pd.read_sql(zapros_to_id_exp, connection)
    exp_one_reader = exp.iloc[0, 2:].dropna().astype(int)
    list_exp = list(exp_one_reader.unique())
    id_books = tuple(list_exp)
    zapros_to_id_book = 'select * from stockstats_cat where "recId" in ' + \
        str(id_books)
    book_info = pd.read_sql(zapros_to_id_book, connection)
    return book_info


def get_dep_books(id_this_book, connection):
    zapros_to_id_books1 = 'select "Object_1" from knowledge_base where "Object_2" = ' + \
        str(int(id_this_book))
    books_dep_this1 = pd.read_sql(zapros_to_id_books1, connection)

    zapros_to_id_books2 = 'select "Object_2" from knowledge_base where "Object_1" = ' + \
        str(int(id_this_book))
    books_dep_this2 = pd.read_sql(zapros_to_id_books2, connection)

    books_dep_this2.rename(columns={'Object_2': 'Object_1'}, inplace=True)

    books_deps_info = list(pd.concat(
        [books_dep_this1, books_dep_this2], ignore_index=True).Object_1.unique())
    id_books_deps_this = tuple(
        list(set(books_deps_info) - set([id_this_book])))

    if not id_books_deps_this:
        zapros_to_info_books = 'select * from stockstats_cat where "recId" = ' + \
            str(int(id_this_book))
        serial_this_book = pd.read_sql(
            zapros_to_info_books, connection).iloc[0][9]
        zapros_to_info_books_serial = 'select * from stockstats_cat where "serial" = ' + \
            "'" + serial_this_book + "'"
        dep_books_info = pd.read_sql(zapros_to_info_books_serial, connection)
        return dep_books_info

    zapros_to_info_books = 'select * from stockstats_cat where "recId" in ' + \
        str(id_books_deps_this)
    dep_books_info = pd.read_sql(zapros_to_info_books, connection)
    return dep_books_info
