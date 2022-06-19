from aiogram import Bot, Dispatcher, executor, types
from db.allItems import getAllItems
from db.countItem import getCountItem, getAllItemIdName
from NormForm import StrToNormForm
from DiffStr import similar
from db.addUser import addUser
from config import ENV_BOT_TOKEN

# Объект бота
bot = Bot(token=ENV_BOT_TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)


# Хэндлер на команду /start
@dp.message_handler(commands="start")
async def start(message: types.Message):
    import datetime
    now = datetime.datetime.now()
    addUser(message.from_user.id, message.from_user.full_name, str(now.date()), str(now.time()), "Visiter")
    await bot.send_message(message.from_user.id, "Приветствую!")

# Хэндлер на команду /help
@dp.message_handler(commands="help")
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, "Бот компании М, в котором можно узнать количество товаров на складе. \
    Чтобы узнать количество товаров - напишите название того, что ищете")

# Хэндлер на команду /version
@dp.message_handler(commands="version")
async def version(message: types.Message):
    await bot.send_message(message.from_user.id, "1.0")

# Хэндлер на команду /Доступные наименования товаров
@dp.message_handler(commands="Items")
async def allItems(message: types.Message):
    items = getAllItems()
    listItems = ""
    for i in range(0, len(items)):
        listItems += str(i + 1) + ") " + items[i][0] + "\n"
    await bot.send_message(message.from_user.id, listItems)


@dp.message_handler()
async def echo_message(message: types.Message):
#def echo_message(message: types.Message):
    items = getAllItemIdName()
    normForm_items = []

    for item in items:
        # 0 - id, 1 - name
        normForm_items.append([item[0], StrToNormForm(item[1])])

    normMessage = StrToNormForm(message.text)
    count = -1
    for normItem in normForm_items:
        # 0 - id, 1 - name
        if normMessage == normItem[1]:
            count = getCountItem(normItem[0])
            await bot.send_message(message.from_user.id, "Количество " + message.text + " на складе = " + str(count[0]))

    # Не найдено полного совпадения -> находим три самых близких варианта
    if count == -1:
        # 0 - id, 1 - name, 2 - близость к normMessage
        for normItem in normForm_items:
            normItem.append(similar(normItem[1], normMessage))
        newlist = sorted(normForm_items, key=lambda x: x[2], reverse=True)
        await bot.send_message(message.from_user.id, "Выбранный Вами вариант не найден. Три ближайших варианта: ")
        
        threeNorm = []
        for i in range(0, len(newlist)):
            if i < 3:
                for j in range(0, len(items)):
                    # 0 - id, 1 - name, 2 - близость к normMessage
                    if newlist[i][0] == items[j][0]:
                        threeNorm.append(items[j][1])
        messageStr = ""                
        for item in threeNorm:
            messageStr += item + ", "
        await bot.send_message(message.from_user.id, messageStr[:-2])


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
    #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #buttons = ["k", "Узнать количество"]
    #keyboard.add(*buttons), reply_markup=keyboard