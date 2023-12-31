import copy
import fastapi
# import database
import pydantic_models
# import config

api = fastapi.FastAPI()

fake_database = {'users': [

    {
        "id": 1,             # тут тип данных - число
        "name": "Anna",      # тут строка
        "nick": "Anny42",    # и тут
        "balance": 15300     # а тут float
    },
    {
        "id": 2,               # у второго пользователя
        "name": "Dima",       # такие же
        "nick": "dimon2319",  # типы
        "balance": 160.23       # данных
    },
    {
        "id": 3,             # у третьего
        "name": "Vladimir",  # юзера
        "nick": "Vova777",   # мы специально сделаем
        "balance": 200.1     # нестандартный тип данных в его балансе
    }
], }


@api.delete('/user/{user_id}')
def delete_user(user_id: int = fastapi.Path()):  # используя fastapi.Path() мы явно указываем, что переменную нужно брать из пути
    for index, u in enumerate(fake_database['users']):  # так как в нашей бд юзеры хранятся в списке, нам нужно найти их индексы внутри этого списка
        if u['id'] == user_id:
            old_db = copy.deepcopy(fake_database)  # делаем полную копию объекта в переменную old_db, чтобы было с чем сравнить
            del fake_database['users'][index]    # удаляем юзера из бд
            return {'old_db': old_db,
                    'new_db': fake_database}
        

@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):  # используя fastapi.Body() мы явно указываем, что отправляем информацию в теле запроса
    for index, u in enumerate(fake_database['users']):  # так как в нашей бд юзеры хранятся в списке, нам нужно найти их индексы внутри этого списка
        if u['id'] == user_id:
            fake_database['users'][index] = user    # обновляем юзера в бд по соответствующему ему индексу из списка users
            return user


@api.post('/user/create')
def index(user: pydantic_models.User):
    fake_database['users'].append(user)
    return {'User Created!': user}


@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id - 1]


@api.get('/get_user_balance_by_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id - 1]['balance']


@api.get('/get_total_balance')
def get_info_about_user():
    total_balance: float = 0.0
    for user in fake_database['users']:
        total_balance += pydantic_models.User(**user).balance
    return total_balance


@api.get("/users/")
def get_users(skip: int = 0, limit: int = 10):
    return fake_database['users'][skip: skip + limit]


@api.get("/user/{user_id}")
def read_user(user_id: str, query: str | None = None):
    if query:
        return {"item_id": user_id, "query": query}
    return {"item_id": user_id}