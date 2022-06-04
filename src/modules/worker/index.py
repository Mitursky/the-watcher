from modules.db.index import *
import time
import playwright
from modules.pager.index import *
from bot import *

UPDATE_TIMEOUT = 600
# get all users from db and get list of users ho track update time > 10 min
def get_users_to_update():
    users = db.db.find()
    users_to_update = []
    for user in users:
        for track in user["tracking"]:
            if user["tracking"][track]["update"] + UPDATE_TIMEOUT < time.time():
                users_to_update.append(user["_id"])
                break
    return users_to_update

# render all users tracking
def render_users_tracking(tgbot):
    users_to_update = get_users_to_update()
    print(users_to_update)
    for user_id in users_to_update:
        user = db.find(user_id)
        for track in user["tracking"]:
            track = user["tracking"][track]
            # if tracking update time > 10 min, update tracking
            if track["update"] + UPDATE_TIMEOUT < time.time():
                response = {}
                try:
                    response = pager.update(name=track["name"], url=track["url"], id=user["_id"], type="img")
                except playwright._impl._api_types.Error:
                    # send message about error
                    tgbot.send_message(
                        user["_id"],
                        f'❌ Ошибка при попытке проверить изменения на сайте: {track["url"]}. Проверьте правильность введенных данных.',
                    )
                    continue
                # add new tracking in DB
                track["update"] = time.time()
                user["tracking"][track["name"]] = track
                db.save(
                    user["_id"],
                    {"$set": user},
                )
                # if responce is_changed == True, send message about change
                print(response)
                if response["is_change"]:
                    tgbot.send_photo(
                        user["_id"],
                        photo=open(response["path"] + "/difference.png", "rb"),
                        caption=f'📸 Изменения на сайте {track["name"]} ({track["url"]}). Изменившиеся элементы выделены на изображении.'
                    )

# call render_users_tracking every minute
while True:
    print('call the render')
    render_users_tracking(tgbot)
    time.sleep(60)
