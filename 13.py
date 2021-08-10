import telebot
import sqlite3
from telebot import types


con=sqlite3.connect('nerochat.db')
curs=con.cursor()
curs.execute("""CREATE TABLE IF NOT EXISTS omma(
id TEXT,
name TEXT,
gen TEXT,
sts TEXT,
par TEXT,
pul TEXT
)""")
con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS akt(
id TEXT,
sgen TEXT,
gen TEXT
)""")

con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS adm(
id TEXT,
key TEXT,
psl TEXT,
sts TEXT
)""")

con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS ban(
id TEXT
)""")

con.commit()

curs.execute("SELECT key FROM adm")
data=curs.fetchone()
if data is None:
    curs.execute("INSERT INTO adm VALUES(?, ?, ?, ?)", ('0', '123456', '0', 'adm'))
    con.commit()

bot_token = '1640553110:AAEW_5GFusYxU1aQPV9ap4yfY2aaIqwgJYo'

bot=telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()

    shaxs_id=message.chat.id
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"SELECT id FROM omma WHERE id={shaxs_id}")
        data=curs.fetchone()
        if data is None:
            curs.execute("INSERT INTO omma VALUES(?, ?, ?, ?, ?, ?)", (shaxs_id, message.from_user.first_name, '0',  'nm', '0', '0'))
            con.commit()
            knob=types.InlineKeyboardMarkup()
            name=types.InlineKeyboardButton(message.from_user.first_name, callback_data='nm')
            knob.add(name)
            try:
                bot.send_message(shaxs_id, 'Добро пожаловать в Нейро чат! Напишите своё имя или нажмите на кнопку:', reply_markup=knob)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                    con.commit()
                except:
                    b=0

        else:
            try:
                bot.send_message(shaxs_id, 'С возвращением!')
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                    con.commit()
                    cls(message)
                except:
                    b=0

@bot.callback_query_handler(func= lambda call: True)
def answ (call):

    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    shaxs_id=call.message.chat.id
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        if call.data == "nm":
            bot.answer_callback_query(call.id)
            curs.execute("""UPDATE omma SET sts=? WHERE id=?""", ('gl', shaxs_id))
            con.commit()
            kb = types.InlineKeyboardMarkup(row_width=2)
            
            kb1=types.InlineKeyboardButton('Мужчина', callback_data='boy')
            kb2=types.InlineKeyboardButton('Женшина', callback_data='girl') 
            kb.add(kb1,kb2)
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text="Отлично, теперь выберите свой пол:", reply_markup=kb)
            
        elif call.data == "adm":

            bot.answer_callback_query(call.id)
            curs.execute("""UPDATE adm SET sts=?""", ('adm',))
            curs.execute("""UPDATE adm SET id=?""", (shaxs_id,))
            con.commit()

            kb1=types.InlineKeyboardButton( text="Участники", callback_data="stat")############
            kb2=types.InlineKeyboardButton( text="Рассылка", callback_data="rass")############
            kb3=types.InlineKeyboardButton( text="Изменить пароль", callback_data="pass")
            kb4=types.InlineKeyboardButton( text="Выход", callback_data="out")
            keyb=[[kb1],[kb2],[kb3],[kb4]]
            kb = types.InlineKeyboardMarkup(keyb)
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text="Главный меню", reply_markup=kb)
            
        elif call.data=='out':
            bot.answer_callback_query(call.id)
            curs.execute("""UPDATE adm SET id=?""", ('0',))
            con.commit()
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text="Вы вышли")
            start(call.message)
            
            
        elif call.data=='stat':
            bot.answer_callback_query(call.id)
            kb = types.InlineKeyboardMarkup(row_width=1)
            kb1=types.InlineKeyboardButton(text="Отправить посылание", callback_data="psl")#########
            kb2=types.InlineKeyboardButton(text="Забанить", callback_data="ban")#########
            kb.add(kb1, kb2)
            curs.execute("SELECT id, name FROM omma")
            re=curs.fetchall()
            mes=1
            for i in re:
                bot.send_message(chat_id=shaxs_id, text="{}. {} с id {}".format(mes, i[1], i[0]), reply_markup=kb)
                mes+=1
            kb = types.InlineKeyboardMarkup()
            kb1=types.InlineKeyboardButton(text="Назад", callback_data="adm")
            kb.add(kb1)
            bot.send_message(chat_id=shaxs_id, text="Это всё!", reply_markup=kb)

        elif call.data=='ban':
            bot.answer_callback_query(call.id)
            curs.execute("INSERT INTO ban VALUES (?)", (call.message.text.split()[4],))
            con.commit()
            kb = types.InlineKeyboardMarkup()
            kb1=types.InlineKeyboardButton(text="Отменить", callback_data="otm")######
            kb.add(kb1)
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='{} заблокировано'.format(call.message.text.split()[4]), reply_markup=kb)
            
        elif call.data=='otm':
            bot.answer_callback_query(call.id)
            kb = types.InlineKeyboardMarkup(row_width=1)
            curs.execute("DELETE FROM ban WHERE id=?", (call.message.text.split()[0],))
            con.commit()
            kb1=types.InlineKeyboardButton(text="Отправить посылание", callback_data="psl")#########
            kb2=types.InlineKeyboardButton(text="Забанить", callback_data="ban")#########
            kb.add(kb1, kb2)
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Разблокировано участник с id {}'.format(call.message.text.split()[0]), reply_markup=kb)
            
        elif call.data=='psl':
            bot.answer_callback_query(call.id)
            curs.execute("""UPDATE adm SET psl=?""", (call.message.text.split()[4],))
            con.commit()
            curs.execute("""UPDATE adm SET sts=?""", ('psl',))
            con.commit()
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Напишите посылание:')
            
        elif call.data=='rass':
            curs.execute("""UPDATE adm SET sts=?""", ('rass',))
            con.commit()
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Отправьте рассылку. Можно отправить Текст, Фото, Видео, Файл или Голосовая сообшеня:')
            
        elif call.data=='pass':
            bot.answer_callback_query(call.id)
            curs.execute("""UPDATE adm SET sts=?""", ('pass',))
            con.commit()
            bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text="Введите новый пароль!")
            
        elif call.data=='boy':
            bot.answer_callback_query(call.id)
            curs.execute("""UPDATE omma SET gen=? WHERE id=?""", ('boy', shaxs_id))
            con.commit()
            kb = types.InlineKeyboardMarkup()
            but=types.ReplyKeyboardMarkup(resize_keyboard=True)
            chatbut=types.KeyboardButton('Новый чат')
            clsbut=types.KeyboardButton('Закрыть чат')
            but.add(chatbut, clsbut)
            try:
                bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Зарегистрировано!', reply_markup=kb)
                bot.send_message(chat_id=shaxs_id, text='Чтобы начать общение, нажмите на кнопку "Новый чат".', reply_markup=but)
            except:
                print('er')
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                    con.commit()
                    cls(call.message)
                except:
                    print('er1')
                    b=0


        elif call.data=='girl':
            bot.answer_callback_query(call.id)

            curs.execute("""UPDATE omma SET gen=? WHERE id=?""", ('girl', shaxs_id))
            con.commit()
            kb = types.InlineKeyboardMarkup()
            but=types.ReplyKeyboardMarkup(resize_keyboard=True)
            chatbut=types.KeyboardButton('Новый чат')
            clsbut=types.KeyboardButton('Закрыть чат')
            but.add(chatbut, clsbut)
            try:
                bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Зарегистрировано!', reply_markup=kb)
                bot.send_message(chat_id=shaxs_id, text='Чтобы начать общение, нажмите на кнопку "Новый чат".', reply_markup=but)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                    con.commit()
                    cls(call.message)
                except:
                    b=0


        elif call.data=='wboy':
            bot.answer_callback_query(call.id)
            cls(call.message)
            try:
                bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Подождите, идёт поиск...')
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                    con.commit()
                    cls(call.message)
                except:
                    b=0

            curs.execute(f"""SELECT gen FROM omma WHERE id={shaxs_id}""")
            isngen=curs.fetchone()
            if isngen is not None:
                isgen=str(isngen)[2:(len(isngen)-4)]
                curs.execute("""SELECT id FROM akt WHERE gen=? and sgen=? and id!=?""",('boy',isgen, shaxs_id))
                dats=curs.fetchone()

                if dats is None:
                    curs.execute("INSERT INTO akt VALUES(?, ?, ?)", (shaxs_id, 'boy', isgen))
                    con.commit()
                    try:
                        bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Ожидание партнёра...')
                    except:
                        try:
                            curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                            con.commit()
                            cls(call.message)
                        except:
                            b=0

                else:
                    dat=str(dats)[2:(len(dats)-4)]
                    curs.execute("""SELECT name FROM omma WHERE id=?""",(shaxs_id,))
                    nms=curs.fetchone()
                    nm=str(nms)[2:(len(nms)-4)]
                    curs.execute("""SELECT name FROM omma WHERE id=?""", (dat,))
                    pnms=curs.fetchone()
                    pnm=str(pnms)[2:(len(pnms)-4)]
                    
                    curs.execute("DELETE FROM akt WHERE id=?", (dat,))
                    con.commit()

                    try:
                        bot.send_message(shaxs_id, '{} в чате'.format(pnm))
                    except:
                        try:
                            curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                            con.commit()
                            cls(call.message)
                        except:
                            b=0

                    try:
                        bot.send_message(dat, '{} в чате'.format(nm))
                    except:
                        try:
                            curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                            con.commit()
                            cls(call.message)
                        except:
                            b=0


                    curs.execute("""UPDATE omma SET par=? WHERE id=?""", (shaxs_id, dat))
                    curs.execute("""UPDATE omma SET par=? WHERE id=?""", (dat, shaxs_id))
                    con.commit()
            else:
                start(call.message)

        elif call.data=='wgirl':
            bot.answer_callback_query(call.id)
            cls(call.message)
            try:
                bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Подождите, идёт поиск...')
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                    con.commit()
                    cls(call.message)
                except:
                    b=0

            curs.execute(f"""SELECT gen FROM omma WHERE id={shaxs_id}""")
            isngen=curs.fetchone()
            if isngen is not None:
                isgen=str(isngen)[2:(len(isngen)-4)]
                curs.execute("""SELECT id FROM akt WHERE gen=? and sgen=? and id!=?""",('girl',isgen, shaxs_id))
                dats=curs.fetchone()

                if dats is None:
                    curs.execute("INSERT INTO akt VALUES(?, ?, ?)", (shaxs_id, 'girl', isgen))
                    con.commit()
                    try:
                        bot.edit_message_text(chat_id=shaxs_id, message_id=call.message.message_id, text='Ожидание партнёра...')
                    except:
                        try:
                            curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                            con.commit()
                            cls(call.message)
                        except:
                            b=0

                else:
                    dat=str(dats)[2:(len(dats)-4)]
                    curs.execute("""SELECT name FROM omma WHERE id=?""",(shaxs_id,))
                    nms=curs.fetchone()
                    nm=str(nms)[2:(len(nms)-4)]
                    curs.execute("""SELECT name FROM omma WHERE id=?""", (dat,))
                    pnms=curs.fetchone()
                    pnm=str(pnms)[2:(len(pnms)-4)]

                    try:
                        bot.send_message(shaxs_id, '{} в чате'.format(pnm))
                    except:
                        try:
                            curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                            con.commit()
                            cls(call.message)
                        except:
                            b=0

                    try:
                        bot.send_message(dat, '{} в чате'.format(nm))
                    except:
                        try:
                            curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                            con.commit()
                            cls(call.message)
                        except:
                            b=0


                    curs.execute("""UPDATE omma SET par=? WHERE id=?""", (shaxs_id, dat))
                    curs.execute("""UPDATE omma SET par=? WHERE id=?""", (dat, shaxs_id))
                    con.commit()
            else:
                start(call.message)
            
@bot.message_handler(content_types=['text'])
def butt(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    shaxs_id=message.chat.id
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT sts FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()
        curs.execute(f"""SELECT sts FROM adm""")
        st=curs.fetchone()
        curs.execute(f"""SELECT id FROM adm""")
        adi=curs.fetchone()
        adid=str(adi)[2:(len(adi)-4)]

        curs.execute(f"""SELECT key FROM adm""")
        keyn=curs.fetchone()
        key=str(keyn)[2:(len(keyn)-4)]
        
        if str(message.text.lower())==key.lower():
            curs.execute("DELETE FROM akt WHERE id=?", (shaxs_id,))
            con.commit()
            curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
            con.commit()
            curs.execute("""UPDATE adm SET id=?""", (shaxs_id,))
            con.commit()
            kb = types.InlineKeyboardMarkup(row_width=1)
            kb1=types.InlineKeyboardButton(text="Go", callback_data="adm")
            kb.add(kb1)
            bot.send_message(shaxs_id, text="Теперь вы админ", reply_markup=kb)
            
        elif adid == str(shaxs_id):
            
            if 'pass' in st:
                curs.execute("""UPDATE adm SET key=?""", ((message.text.lower(),)))
                con.commit()
                curs.execute("""UPDATE adm SET sts=?""", ("adm",))
                con.commit()
                kb = types.InlineKeyboardMarkup(row_width=1)
                kb1=types.InlineKeyboardButton(text="Назад", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Пароль обновлён!", reply_markup=kb)

            elif 'psl' in st:
                curs.execute(f"""SELECT psl FROM adm""")
                pid=curs.fetchone()
                psid=str(pid)[2:(len(pid)-4)]
                bot.send_message(psid, text='От имени админа')
                bot.send_message(psid, text=message.text)
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено! Можете продолжить отправку.", reply_markup=kb)

            elif 'rass' in st:
                curs.execute("SELECT id FROM omma")
                re=curs.fetchall()
                mes=1
                for i in re:
                    bot.send_message(chat_id=i[0], text='От имени админа')
                    bot.send_message(chat_id=i[0], text=message.text)
                    mes+=1
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено {} участникам! Можете продолжить отправку".format(mes), reply_markup=kb)

            else:
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Команда с называнием {} не найдено!".format(message.text), reply_markup=kb)
                
            
        elif dats is None:
            start(message)
        elif 'nm' in dats:
            curs.execute("""UPDATE omma SET name=? WHERE id=?""", (message.text, shaxs_id))
            curs.execute("""UPDATE omma SET sts=? WHERE id=?""", ('gl', shaxs_id))
            con.commit()
            kb = types.InlineKeyboardMarkup(row_width=2)
            kb1=types.InlineKeyboardButton('Мужчина', callback_data='boy')
            kb2=types.InlineKeyboardButton('Женшина', callback_data='girl') 
            kb.add(kb1,kb2)
            bot.send_message(shaxs_id, text="Отлично, теперь выберите свой пол:", reply_markup=kb)
            
        elif message.text=='Новый чат':
            chat(message)
        elif message.text=='Закрыть чат':
            cls(message)
        else:
            echo_message(message)

@bot.message_handler(content_types=['photo'])
def echo_photo(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    shaxs_id=message.chat.id
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    curs.execute(f"""SELECT sts FROM adm""")
    st=curs.fetchone()
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT par FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()
        
            
        if adid == str(shaxs_id):
            if 'psl' in st:
                curs.execute(f"""SELECT psl FROM adm""")
                pid=curs.fetchone()
                psid=str(pid)[2:(len(pid)-4)]
                bot.send_message(psid, text='От имени админа')
                bot.send_photo(psid, message.photo[-1].file_id)
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено! Можете продолжить отправку.", reply_markup=kb)

            elif 'rass' in st:
                curs.execute("SELECT id FROM omma")
                re=curs.fetchall()
                mes=1
                for i in re:
                    bot.send_message(chat_id=i[0], text='От имени админа')
                    bot.send_photo(i[0], message.photo[-1].file_id)
                    mes+=1
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено {} участникам! Можете продолжить отправку".format(mes), reply_markup=kb)
        elif dats is None or str(dats)== "('0',)":
            chat(message)
        else:
            dat=str(dats)[2:(len(dats)-4)]
            try:
                bot.send_photo(dat, message.photo[-1].file_id)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                    con.commit()
                    cls(message)
                except:
                    b=0


@bot.message_handler(content_types=['video'])
def echo_video(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    shaxs_id=message.chat.id
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    curs.execute(f"""SELECT sts FROM adm""")
    st=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT par FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()
        if adid == str(shaxs_id):
            if 'psl' in st:
                curs.execute(f"""SELECT psl FROM adm""")
                pid=curs.fetchone()
                psid=str(pid)[2:(len(pid)-4)]
                bot.send_message(psid, text='От имени админа')
                bot.send_video(psid, message.video.file_id)
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено! Можете продолжить отправку.", reply_markup=kb)

            elif 'rass' in st:
                curs.execute("SELECT id FROM omma")
                re=curs.fetchall()
                mes=1
                for i in re:
                    bot.send_message(chat_id=i[0], text='От имени админа')
                    bot.send_video(i[0], message.video.file_id)
                    mes+=1
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено {} участникам! Можете продолжить отправку".format(mes), reply_markup=kb)
        elif dats is None or str(dats)== "('0',)":
            chat(message)
        else:
            dat=str(dats)[2:(len(dats)-4)]
            try:
                bot.send_video(dat, message.video.file_id)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                    con.commit()
                    cls(message)
                except:
                    b=0


@bot.message_handler(content_types=['audio'])
def echo_audio(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    curs.execute(f"""SELECT sts FROM adm""")
    st=curs.fetchone()
    shaxs_id=message.chat.id
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT par FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()
        if adid == str(shaxs_id):
            if 'psl' in st:
                curs.execute(f"""SELECT psl FROM adm""")
                pid=curs.fetchone()
                psid=str(pid)[2:(len(pid)-4)]
                bot.send_message(psid, text='От имени админа')
                bot.send_audio(psid, message.audio.file_id)
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено! Можете продолжить отправку.", reply_markup=kb)

            elif 'rass' in st:
                curs.execute("SELECT id FROM omma")
                re=curs.fetchall()
                mes=1
                for i in re:
                    bot.send_message(chat_id=i[0], text='От имени админа')
                    bot.send_audio(i[0], message.audio.file_id)
                    mes+=1
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено {} участникам! Можете продолжить отправку".format(mes), reply_markup=kb)
        elif dats is None or str(dats)== "('0',)":
            chat(message)
                
        else:
            dat=str(dats)[2:(len(dats)-4)]
            try:
                bot.send_audio(dat, message.audio.file_id)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                    con.commit()
                    cls(message)             
                except:
                    b=0


@bot.message_handler(content_types=['document'])
def echo_file(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    curs.execute(f"""SELECT sts FROM adm""")
    st=curs.fetchone()
    shaxs_id=message.chat.id
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT par FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()
        if adid == str(shaxs_id):
            if 'psl' in st:
                curs.execute(f"""SELECT psl FROM adm""")
                pid=curs.fetchone()
                psid=str(pid)[2:(len(pid)-4)]
                bot.send_message(psid, text='От имени админа')
                bot.send_document(psid, message.document.file_id)
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено! Можете продолжить отправку.", reply_markup=kb)

            elif 'rass' in st:
                curs.execute("SELECT id FROM omma")
                re=curs.fetchall()
                mes=1
                for i in re:
                    bot.send_message(chat_id=i[0], text='От имени админа')
                    bot.send_document(i[0], message.document.file_id)
                    mes+=1
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_document(shaxs_id, text="Отправлено {} участникам! Можете продолжить отправку".format(mes), reply_markup=kb)
        elif dats is None or str(dats)== "('0',)":
            chat(message)
                
        else:
            dat=str(dats)[2:(len(dats)-4)]
            try:
                bot.send_document(dat, message.document.file_id)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                    con.commit()
                    cls(message)
                except:
                    b=0


@bot.message_handler(content_types=['voice'])
def echo_voice(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    curs.execute(f"""SELECT sts FROM adm""")
    st=curs.fetchone()
    shaxs_id=message.chat.id
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT par FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()
        if adid == str(shaxs_id):
            if 'psl' in st:
                curs.execute(f"""SELECT psl FROM adm""")
                pid=curs.fetchone()
                psid=str(pid)[2:(len(pid)-4)]
                bot.send_message(psid, text='От имени админа')
                bot.send_voice(psid, message.voice.file_id)
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено! Можете продолжить отправку.", reply_markup=kb)

            elif 'rass' in st:
                curs.execute("SELECT id FROM omma")
                re=curs.fetchall()
                mes=1
                for i in re:
                    bot.send_message(chat_id=i[0], text='От имени админа')
                    bot.send_voice(i[0], message.voice.file_id)
                    mes+=1
                kb = types.InlineKeyboardMarkup()
                kb1=types.InlineKeyboardButton(text="Главный меню", callback_data="adm")
                kb.add(kb1)
                bot.send_message(shaxs_id, text="Отправлено {} участникам! Можете продолжить отправку".format(mes), reply_markup=kb)
        elif dats is None or str(dats)== "('0',)":
            chat(message)
                
        else:
            dat=str(dats)[2:(len(dats)-4)]
            try:
                bot.send_voice(dat, message.voice.file_id)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                    con.commit()
                    cls(message)
                except:
                    b=0



@bot.message_handler(commands=['chat'])
def chat(message):
    cls(message)
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()

    shaxs_id=message.chat.id
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT gen FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()

        if dats is None:
            start(message)
        else:

            knob=types.InlineKeyboardMarkup()
            iboy=types.InlineKeyboardButton('Мужчина', callback_data='wboy')
            igirl=types.InlineKeyboardButton('Женшина', callback_data='wgirl')

            knob.add(iboy, igirl)
            try:
                bot.send_message(shaxs_id, 'С кем вы хотите общаться?', reply_markup=knob)
            except:
                try:
                    curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                    con.commit()
                    cls(message)
                except:
                    b=0

@bot.message_handler(commands=['close'])
def cls(message):
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    shaxs_id=message.chat.id
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:

        curs.execute(f"SELECT par FROM omma WHERE id={shaxs_id}")
        pars=curs.fetchone()
        if pars is not None:
            par=str(pars)[2:(len(pars)-4)]
            if par == '0':
                b=0
            else:
                curs.execute("""UPDATE omma SET par=? WHERE id=?""", ('0', shaxs_id))
                curs.execute("""UPDATE omma SET par=? WHERE id=?""", ('0', par))
                con.commit()
                
                bot.send_message(shaxs_id, 'Собеседник вышел из чат.')
                try:
                    bot.send_message(par, 'Собеседник вышел из чат.')
                except:
                    try:
                        curs.execute("DELETE FROM omma WHERE id=?", (par,))
                        con.commit()
                        cls(message)
                    except:
                        b=0
        else:
            start(message)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    
    con=sqlite3.connect('nerochat.db')
    curs=con.cursor()
    shaxs_id=message.chat.id
    curs.execute(f"""SELECT id FROM adm""")
    adi=curs.fetchone()
    adid=str(adi)[2:(len(adi)-4)]
    curs.execute(f"SELECT id FROM ban WHERE id={shaxs_id}")
    ban=curs.fetchone()
    if ban is not None:
        bot.send_message(shaxs_id, 'Ваш аккаунт заблокирован!')
    else:
        curs.execute(f"""SELECT par FROM omma WHERE id={shaxs_id}""")
        dats=curs.fetchone()
        if dats is None:
            start(message)
        else:
            dat=str(dats)[2:(len(dats)-4)]
            if dat !='0':
                try:
                    bot.send_message(dat, message.text)
                except:
                    try:
                        curs.execute("DELETE FROM omma WHERE id=?", (dat,))
                        con.commit()
                        cls(message)
                    except:
                        b=0
            else:
                try:
                    bot.send_message(shaxs_id, 'Нажмите на кнопку "Новый чат".')
                except:
                    try:
                        curs.execute("DELETE FROM omma WHERE id=?", (shaxs_id,))
                        con.commit()
                        cls(message)
                    except:
                        b=0









bot.polling()
