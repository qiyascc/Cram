from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Config import DATABASE_URL, ADMINS, LESSONS, PYSCHOLOGY, USERS, BLACK_LIST, OTHERS
from colorama import Fore

client = MongoClient(DATABASE_URL)
db = client["Cram"]

# Koleksiyon
LessonsDB = db["Lessons"]
AdminsDB = db["Admins"]
PyschologyDB = db["Pyschology"]
UsersDB = db["Users"]
BlackDB = db["BlackList"]
OtherDB = db["Others"]


class userDB:
    def __init__(self):
        pass

    async def userupdate(self):
        await UsersDB.update_one(
            {"_id": "UserList"}, {"$set": {"users": USERS}}, upsert=True
        )

    async def load_users(self):
        data = await UsersDB.find_one({"_id": "UserList"})
        if data:
            for user in data["users"]:
                if user not in USERS:
                    USERS.append(user)
        print(Fore.YELLOW + "[DATA] Kullanıcı verileri yüklendi.\n" + Fore.RESET)


class blackListDB:
    def __init__(self):
        pass

    async def blackupdate(self):
        await BlackDB.update_one(
            {"_id": "BlackList"}, {"$set": {"blacklist": BLACK_LIST}}, upsert=True
        )

    async def load_blacklist(self):
        data = await BlackDB.find_one({"_id": "BlackList"})
        if data:
            for black in data["blacklist"]:
                if black not in BLACK_LIST:
                    BLACK_LIST.append(black)
        print(Fore.YELLOW + "[DATA] Yasaklıların verileri yüklendi.\n" + Fore.RESET)


# Admin Datası
class adminDB:
    def __init__(self):
        pass

    async def adminupdate(self):
        await AdminsDB.update_one(
            {"_id": "AdminList"}, {"$set": {"admins": ADMINS}}, upsert=True
        )

    async def load_admins(self):
        data = await AdminsDB.find_one({"_id": "AdminList"})
        if data:
            for admin in data["admins"]:
                if admin not in ADMINS:
                    ADMINS.append(admin)
        print(Fore.YELLOW + "[DATA] Admin verileri yüklendi.\n" + Fore.RESET)


# Dersler Datası
class lessonsDB:
    def __init__(self):
        pass

    async def lessonsupdate(self):
        await LessonsDB.update_one(
            {"_id": "LessonList"}, {"$set": {"lessons": LESSONS}}, upsert=True
        )

    async def load_lessons(self):
        data = await LessonsDB.find_one({"_id": "LessonList"})
        if data:
            for lesson in data["lessons"]:
                if lesson not in LESSONS:
                    LESSONS.append(lesson)
    print(Fore.YELLOW + "[DATA] Ders verileri yüklendi.\n" + Fore.RESET)

# Psikoloji Datası
class pyschologyDB:
    def __init__(self):
        pass

    async def pyschologyupdate(self):
        await PyschologyDB.update_one(
            {"_id": "PyschologyList"}, {"$set": {"pyschology": PYSCHOLOGY}}, upsert=True
        )

    async def load_pyschology(self):
        data = await PyschologyDB.find_one({"_id": "PyschologyList"})
        if data:
            for pyschology in data["pyschology"]:
                if pyschology not in PYSCHOLOGY:
                    PYSCHOLOGY.append(pyschology)
        print(Fore.YELLOW + "[DATA] Psikoloji verileri yüklendi.\n" + Fore.RESET)


class otherDB:
    def __init__(self):
        pass

    async def otherupdate(self, key, value):
        if key not in OTHERS:
            OTHERS[key] = value
        else:
            OTHERS[key] += value
        await OtherDB.update_one(
            {"_id": "OtherList"}, {"$set": {"others": OTHERS}}, upsert=True
        )

    async def load_others(self):
        data = await OtherDB.find_one({"_id": "OtherList"})
        if data:
            for key, value in data["others"].items():
                if key not in OTHERS:
                    OTHERS[key] = value
                else:
                    OTHERS[key] = value
        print(Fore.YELLOW + "[DATA] Diğer veriler yüklendi.\n" + Fore.RESET)
