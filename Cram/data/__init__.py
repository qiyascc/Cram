from .database import (
    adminDB,
    lessonsDB,
    pyschologyDB,
    userDB,
    blackListDB,
    otherDB,
)

AdminDB = adminDB()
LessonsDB = lessonsDB()
PyschologyDB = pyschologyDB()
Otherdb = otherDB()
UserDB = userDB()
BlackDB = blackListDB()

async def dataload():
    await AdminDB.load_admins()
    await LessonsDB.load_lessons()
    await PyschologyDB.load_pyschology()
    await UserDB.load_users()
    await BlackDB.load_blacklist()
    await Otherdb.load_others()
