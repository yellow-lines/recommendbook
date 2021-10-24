from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
import pandas as pd

server = SSHTunnelForwarder(
        ('178.154.241.46', 22),
        ssh_username="owner",
        ssh_password="здесь ваш закрытый ssh ключ",
        remote_bind_address=('127.0.0.1', 5432)
    )

server.start()
local_port = str(server.local_bind_port)
engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format("postgres", "sleeperonelove", "127.0.0.1", local_port,
                                             "recommender_users"))
connection = engine.connect()

"""
# получение id книг, которые читал user с заданным id
def get_id_exp(id_reader, connection):
    zapros_to_id_exp = 'select * from exp_reader_id where "readerID" = ' + str(int(id_reader))
    exp = pd.read_sql(zapros_to_id_exp, connection)
    exp_one_reader = exp[exp['readerID'] == id_reader].iloc[0, 2:].dropna().astype(int)
    list_exp = list(exp_one_reader.unique())
    return list_exp


# получение из бз датафреймов, где один из элементов - книга с заданным id
def get_bz_exp(id_books, connection):
    zapros_to_id_book1 = 'select * from knowledge_base where "Object_1" = ' + str(id_books)
    zapros_to_id_book2 = 'select * from knowledge_base where "Object_2" = ' + str(id_books)
    book_Ob1 = pd.read_sql(zapros_to_id_book1, connection)
    book_Ob2 = pd.read_sql(zapros_to_id_book2, connection)
    return book_Ob1, book_Ob2


# получение инфы о книге по id
def get_info_book(id_books, connection):
    zapros_to_id_book = 'select * from stockstats_cat where "recId" = ' + str(id_books)
    book_info = pd.read_sql(zapros_to_id_book, connection)
    return book_info


# перевод login в iduser
def get_registr_table_userid(login, connection):
    zapros_to_name = 'select * from registr_table where "login" = ' + "'" + login + "'"
    info_user = pd.read_sql(zapros_to_name, connection)
    userid = info_user.iloc[0]['userid']
    return userid


# получение датафрейма по логину юзера с его книгами и рекомендуемыми ему
def create_got_data(login, connection):
    # получаем "уникальный опыт юзера"
    id_reader = get_registr_table_userid(login, connection)
    list_exp = get_id_exp(id_reader, connection)

    sources = []
    name_sources = []
    targets = []
    name_targets = []
    weights = []

    # бежим по его книгам1
    for i_book in list_exp:

        # получаем автора и название книги1
        df_for_i_book = get_info_book(i_book, connection)
        if df_for_i_book.iloc[0]['aut'] == None:
            title_aut_i_book = df_for_i_book.iloc[0]['title']
        elif df_for_i_book.iloc[0]['title'] == None:
            title_aut_i_book = df_for_i_book.iloc[0]['aut']
        else:
            title_aut_i_book = df_for_i_book.iloc[0]['aut'] + ' ' + df_for_i_book.iloc[0]['title']

            # из бз получаем дф с книгами, которые связаны с  книгой1
        books_for_user1, books_for_user2 = get_bz_exp(i_book, connection)

        # бежим по книгам2 связанными с книгой1
        for i in range(len(books_for_user1)):
            # игнорируем самосвязь
            if books_for_user1.iloc[i][2] != i_book:
                # получаем автора и название книги2
                df_for_bfu = get_info_book(books_for_user1.iloc[i][2], connection)
                if df_for_bfu.iloc[0]['aut'] == None:
                    title_aut_bfu = df_for_bfu.iloc[0]['title']
                elif df_for_bfu.iloc[0]['title'] == None:
                    title_aut_bfu = df_for_bfu.iloc[0]['aut']
                else:
                    title_aut_bfu = df_for_bfu.iloc[0]['aut'] + ' ' + df_for_bfu.iloc[0]['title']

                # title_aut_bfu = df_for_bfu.iloc[0]['aut'] + ' ' + df_for_bfu.iloc[0]['title']
                # записываем айдишники, названия, авторов книг и вес их связи
                sources.append(books_for_user1.iloc[i][1])
                targets.append(i_book)
                name_sources.append(title_aut_bfu)
                name_targets.append(title_aut_i_book)
                weights.append(books_for_user1.iloc[i][3])

            # аналогично по второму датафрейму
        for i in range(len(books_for_user2)):
            if books_for_user2.iloc[i][1] != i_book:

                df_for_bfu = get_info_book(books_for_user2.iloc[i][1], connection)

                if df_for_bfu.iloc[0]['aut'] == None:
                    title_aut_bfu = df_for_bfu.iloc[0]['title']
                elif df_for_bfu.iloc[0]['title'] == None:
                    title_aut_bfu = df_for_bfu.iloc[0]['aut']
                else:
                    title_aut_bfu = df_for_bfu.iloc[0]['aut'] + ' ' + df_for_bfu.iloc[0]['title']

                sources.append(books_for_user2.iloc[i][0])
                targets.append(i_book)
                name_sources.append(title_aut_bfu)
                name_targets.append(title_aut_i_book)
                weights.append(books_for_user2.iloc[i][3])

    df = pd.DataFrame({'Source_id': sources,
                       'Target_id': targets,
                       'Source': name_sources,
                       'Target': name_targets,
                       'Weight': weights})

    # сортируем по убыванию весов
    df.sort_values(by='Weight', inplace=True, ascending=False)
    return df
"""
def get_registr_table_userid(login, connection):
    zapros_to_name = 'select * from registr_table where "login" = ' + "'" + login + "'"
    info_user = pd.read_sql(zapros_to_name, connection)
    userid = info_user.iloc[0]['userid']
    return userid


"""
def get_info_book_dict(id_books, connection, login):
    adf = get_id_exp(get_registr_table_userid(login, connection), connection)
    id_books = tuple(adf)
    zapros_to_id_book = 'select * from stockstats_cat where "recId" in ' + str(id_books)
    book_info = pd.read_sql(zapros_to_id_book, connection)
    return book_info

def recomend(login, connection):
    data = create_got_data(login, connection)

    id_reader = get_registr_table_userid(login, connection)
    list_exp = get_id_exp(id_reader, connection)

    book_rec = []
    for i in range(len(data)):
        if data.iloc[i]['Source_id'] not in list_exp:
            book_rec.append(data.iloc[i]['Source_id'])
        if data.iloc[i]['Target_id'] not in list_exp:
            book_rec.append(data.iloc[i]['Target_id'])

    book_rec = list(pd.Series(book_rec).unique())

    return book_rec"""
login = 'login_313414'
def get_id_exp1(login, connection):
    id_reader = get_registr_table_userid(login, connection)
    zapros_to_id_exp = 'select * from exp_reader_id where "readerID" = ' + str(int(id_reader))
    exp = pd.read_sql(zapros_to_id_exp, connection)
    exp_one_reader = exp.iloc[0, 2:].dropna().astype(int)
    list_exp = list(exp_one_reader.unique())
    exp_reader = tuple(list_exp)
    zapros_to_id_books1 = 'select "Object_1" from knowledge_base where "Object_1" in ' + str(exp_reader) + 'OR "Object_2" in ' + str(exp_reader)
    zapros_to_id_books2 = 'select "Object_2" from knowledge_base where "Object_1" in ' + str(exp_reader) + 'OR "Object_2" in ' + str(exp_reader)
    book_info1 = pd.read_sql(zapros_to_id_books1, connection)
    book_info2 = pd.read_sql(zapros_to_id_books2, connection)
    book_info2.rename(columns={'Object_2': 'Object_1'}, inplace=True)
    book_info = list(pd.concat([book_info1, book_info2], ignore_index=True).Object_1.unique())
    id_books = tuple(list(set(book_info) - set(list_exp)))
    zapros_to_id_book = 'select * from stockstats_cat where "recId" in ' + str(id_books)
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



