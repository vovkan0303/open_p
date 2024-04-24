import base64
import datetime
import sqlite3
import time
from base64 import b64encode

from flask import Flask, render_template, redirect, g, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
import random
from data import db_session
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.users import User
import requests
from bs4 import BeautifulSoup


class Currency:
    global currency_e, currency_d, currency_br, currency_aed, currency_bgn, currency_try, currency_jry, currency_azn
    M_E = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B5%D0%B2%D1%80%D0%BE&sca_esv=09379ecd0b6efd91&ei=34wiZtcf0s7A8A-a4KmYDA&udm=&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%2C&gs_lp=Egxnd3Mtd2l6LXNlcnAiEjEwMCDRgNGD0LHQu9C10LkgLCoCCAUyChAAGIAEGEMYigUyCBAAGIAEGLEDMgoQABiABBhDGIoFMgUQABiABDIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBUigJ1DyBFjyBHABeAGQAQCYAVKgAVKqAQExuAEDyAEA-AEBmAICoAJZwgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATKgB7AG&sclient=gws-wiz-serp'
    M_D = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&sca_esv=09379ecd0b6efd91&ei=uIUiZqmMCJa9wPAPj6ytoAs&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9&gs_lp=Egxnd3Mtd2l6LXNlcnAiEDEwMCDRgNGD0LHQu9C10LkqAggEMg8QABiABBhDGIoFGEYYggIyChAAGIAEGEMYigUyChAAGIAEGEMYigUyCBAAGIAEGLEDMgoQABiABBhDGIoFMgoQABiABBhDGIoFMggQABiABBixAzIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIbEAAYgAQYQxiKBRhGGIICGJcFGIwFGN0E2AEBSNRoUABY0ltwAHgBkAEAmAFqoAHyBaoBAzguMrgBAcgBAPgBAZgCCqACnwbCAgUQABiABMICDhAAGIAEGLEDGIMBGIoFwgIREC4YgAQYsQMY0QMYgwEYxwHCAgsQABiABBixAxiDAcICDhAuGIAEGLEDGIMBGIoFmAMAugYGCAEQARgTkgcDOC4yoAeHUg&sclient=gws-wiz-serp'
    M_BR = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B1%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D1%85+%D1%80%D1%83%D0%B1%D0%BB%D1%8F%D1%85&sca_esv=09379ecd0b6efd91&ei=hI0iZp6LPPSbwPAP5J2C-AE&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%2C&gs_lp=Egxnd3Mtd2l6LXNlcnAiFTEwMCDRgNGD0LHQu9C10Lkg0LIgLCoCCAMyChAAGIAEGEMYigUyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARI5idQpxxYpxxwAXgBkAEAmAE9oAE9qgEBMbgBAcgBAPgBAZgCAqACRMICChAAGLADGNYEGEfCAg0QABiABBiwAxhDGIoFmAMAiAYBkAYKkgcBMqAHoAY&sclient=gws-wiz-serp'
    M_AED = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B4%D0%B8%D1%80%D1%85%D0%B0%D0%BC%D0%B0%D1%85&sca_esv=09379ecd0b6efd91&ei=xI8iZrf5MPC-wPAPw7up6AI&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B4&gs_lp=Egxnd3Mtd2l6LXNlcnAiFjEwMCDRgNGD0LHQu9C10Lkg0LIg0LQqAggCMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEiBFVDLBFjLBHABeAGQAQCYATagATaqAQExuAEByAEA-AEBmAICoAI-wgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigWYAwCIBgGQBgqSBwEyoAetBg&sclient=gws-wiz-serp'
    M_BGN = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B1%D0%BE%D0%BB%D0%B3%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D1%85+%D0%BB%D0%B5%D0%B2%D0%B0%D1%85&sca_esv=09379ecd0b6efd91&ei=7I8iZszWL9mmwPAP0Y-1iAs&udm=&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B1%D0%BE&gs_lp=Egxnd3Mtd2l6LXNlcnAiGDEwMCDRgNGD0LHQu9C10Lkg0LIg0LHQvioCCAAyBhAAGBYYHjIIEAAYFhgeGA8yBhAAGBYYHjIGEAAYFhgeMggQABgWGB4YDzIGEAAYFhgeMggQABgWGB4YDzIIEAAYgAQYogQyCBAAGIAEGKIESOgPUKMEWMEJcAF4AZABAJgBSKABiwGqAQEyuAEByAEA-AEBmAIDoAKSAcICChAAGLADGNYEGEfCAgUQABiABJgDAIgGAZAGCJIHATOgB5YP&sclient=gws-wiz-serp'
    M_TRY = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D1%82%D1%83%D1%80%D0%B5%D1%86%D0%BA%D0%B8%D1%85+%D0%BB%D0%B8%D1%80%D0%B0%D1%85&sca_esv=09379ecd0b6efd91&ei=_o8iZtukJIaiwPAPnZeKwAE&udm=&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D1%82&gs_lp=Egxnd3Mtd2l6LXNlcnAiFjEwMCDRgNGD0LHQu9C10Lkg0LIg0YIqAggBMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEifIVCRFliRFnABeACQAQCYAUGgAUGqAQExuAEByAEA-AEBmAICoAJGwgIHEAAYsAMYHsICCRAAGLADGAgYHsICCxAAGLADGAgYHhgPwgILEAAYgAQYsAMYogSYAwCIBgGQBgeSBwEyoAefBw&sclient=gws-wiz-serp'
    M_JRY = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D1%8F%D0%BF%D0%BE%D0%BD%D1%81%D0%BA%D0%B8%D1%85+%D0%B9%D0%B5%D0%BD%D0%B0%D1%85&sca_esv=09379ecd0b6efd91&ei=CpAiZsLQDr61wPAPnY2l4AQ&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D1%8F%D0%BF&gs_lp=Egxnd3Mtd2l6LXNlcnAiGDEwMCDRgNGD0LHQu9C10Lkg0LIg0Y_QvyoCCAAyChAAGIAEGEYYggIyBhAAGBYYHjIIEAAYFhgeGA8yCBAAGBYYHhgPMggQABgWGB4YDzIIEAAYgAQYogQyCBAAGIAEGKIEMhYQABiABBhGGIICGJcFGIwFGN0E2AEBSM4OULEGWO4IcAF4AZABAJgBSKABiAGqAQEyuAEByAEA-AEBmAIDoAKSAcICChAAGLADGNYEGEfCAgUQABiABMICChAAGBYYChgeGA-YAwCIBgGQBgi6BgYIARABGBOSBwEzoAeMEQ&sclient=gws-wiz-serp'
    M_AZN = 'https://www.google.com/search?q=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B0%D0%B7%D0%B5%D1%80%D0%B1%D0%B0%D0%B9%D0%B4%D0%B6%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D1%85+%D0%BC%D0%B0%D0%BD%D0%B0%D1%82%D0%B0%D1%85&sca_esv=09379ecd0b6efd91&ei=FJAiZs3-NtiqwPAP3LCYyA0&oq=100+%D1%80%D1%83%D0%B1%D0%BB%D0%B5%D0%B9+%D0%B2+%D0%B0&gs_lp=Egxnd3Mtd2l6LXNlcnAiFjEwMCDRgNGD0LHQu9C10Lkg0LIg0LAqAggBMgUQABiABDIFEAAYgAQyBRAAGIAEMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB5I_whQNVg1cAF4AZABAJgBQKABQKoBATG4AQHIAQD4AQGYAgKgAkbCAgoQABiwAxjWBBhHmAMAiAYBkAYIkgcBMqAHjAk&sclient=gws-wiz-serp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    current_converted_price = 0

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price_e().replace(",", "."))
        self.current_converted_price = float(self.get_currency_price_d().replace(",", "."))
        self.current_converted_price = float(self.get_currency_price_br().replace(",", "."))
        self.current_converted_price = float(self.get_currency_price_aed().replace(",", "."))
        self.current_converted_price = float(self.get_currency_price_bgn().replace(",", "."))
        self.current_converted_price = float(self.get_currency_price_try().replace(",", "."))
        self.current_converted_price = float(self.get_currency_price_jry().replace(",", "."))
        self.current_converted_price = float(self.get_currency_price_azn().replace(",", "."))

    def get_currency_price_e(self):
        full_page_e = requests.get(self.M_E, headers=self.headers)
        soup_e = BeautifulSoup(full_page_e.content, 'html.parser')
        convert_e = soup_e.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_e[0].text

    def get_currency_price_d(self):
        full_page_d = requests.get(self.M_D, headers=self.headers)
        soup_d = BeautifulSoup(full_page_d.content, 'html.parser')
        convert_d = soup_d.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_d[0].text

    def get_currency_price_br(self):
        full_page_br = requests.get(self.M_BR, headers=self.headers)
        soup_br = BeautifulSoup(full_page_br.content, 'html.parser')
        convert_br = soup_br.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_br[0].text

    def get_currency_price_aed(self):
        full_page_aed = requests.get(self.M_AED, headers=self.headers)
        soup_aed = BeautifulSoup(full_page_aed.content, 'html.parser')
        convert_aed = soup_aed.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_aed[0].text

    def get_currency_price_bgn(self):
        full_page_bgn = requests.get(self.M_BGN, headers=self.headers)
        soup_bgn = BeautifulSoup(full_page_bgn.content, 'html.parser')
        convert_bgn = soup_bgn.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_bgn[0].text

    def get_currency_price_try(self):
        full_page_try = requests.get(self.M_TRY, headers=self.headers)
        soup_try = BeautifulSoup(full_page_try.content, 'html.parser')
        convert_try = soup_try.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_try[0].text

    def get_currency_price_jry(self):
        full_page_jry = requests.get(self.M_JRY, headers=self.headers)
        soup_jry = BeautifulSoup(full_page_jry.content, 'html.parser')
        convert_jry = soup_jry.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_jry[0].text

    def get_currency_price_azn(self):
        full_page_azn = requests.get(self.M_AZN, headers=self.headers)
        soup_azn = BeautifulSoup(full_page_azn.content, 'html.parser')
        convert_azn = soup_azn.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert_azn[0].text

    def check_currency(self):
        currency_e = float(self.get_currency_price_e().replace(",", "."))
        currency_d = float(self.get_currency_price_d().replace(",", "."))
        currency_br = float(self.get_currency_price_br().replace(",", "."))
        currency_aed = float(self.get_currency_price_e().replace(",", "."))
        currency_bgn = float(self.get_currency_price_d().replace(",", "."))
        currency_try = float(self.get_currency_price_br().replace(",", "."))
        currency_jry = float(self.get_currency_price_e().replace(",", "."))
        currency_azn = float(self.get_currency_price_d().replace(",", "."))
        with open('static/text/kurs.txt', 'w+', encoding='utf-8') as f:
            vremya = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write("1 монета = 1 Рубль\n"
                    "100 монет = " + str(currency_e) + ' Евро\n'
                                                       "100 монет = " + str(
                currency_d) + ' Долларов\n'
                              "100 монет = " + str(currency_br) + ' Белорусских рублей\n'
                                                                  "100 монет = " + str(
                currency_aed) + ' Дирхам\n'
                                "100 монет = " + str(currency_bgn) + ' Болгарских львох\n'
                                                                     "100 монет = " + str(
                currency_try) + ' Турецких лир\n'
                                "100 монет = " + str(currency_jry) + ' Японских йен\n'
                                                                     "100 монет = " + str(
                currency_azn) + ' Азербайджанских манатов\n'
                                f'Курс на данное время: {vremya}')
        print('Обновил')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(user_id)).first()
    if user.avatarka_svoya == None:
        ava = None
    else:
        ava = base64.b64encode(user.avatarka_svoya).decode('ascii')
    db_sess.commit()
    tek_user(user_id, ava)
    return db_sess.query(User).get(user_id)


def tek_user(kto_to, ava):
    global chel, svoya
    svoya = ava
    chel = kto_to


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def start():
    return render_template("start.html", title='Начало')


@app.route("/glav")
def glav():
    return render_template("index.html", svoya=svoya, title='Главная')


@app.route('/boxes')
@login_required
def boxes():
    return render_template("boxes.html", svoya=svoya, title='Боксы')


@app.route('/zagruzit_avy')
@login_required
def zagruzit_avy():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    if user.avatarka_svoya == None:
        print('нет своей авы')
    else:
        print('имеется')
    db_sess.commit()
    return render_template("zagruzit_avy.html", svoya=svoya, title='Загрузка своего аватара')


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    global avatarka
    if request.method == 'POST':
        file = request.files['file']
        a = str(file)
        a = a[14:]
        a = a.split()
        a = a[0]
        a = a[1:-1]
        a = a.split('.')
        if file and (str(a[1]) == 'png' or str(a[1]) == 'PNG'):
            img = file.read()
            avatarka = sqlite3.Binary(img)
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == int(chel)).first()
            user.avatarka_svoya = avatarka
            user.avatarka = '-1'
            db_sess.commit()
            print("Аватар обновлен", "success")
            return render_template("ysp2.html", title='Успешно!')
        else:
            return render_template("chtoto.html", title='Что-то пошло не так!')


@app.route('/ysp2')
@login_required
def ysp2():
    return render_template("ysp2.html", title='Успешно2!')


@app.route('/obnovit_kurs')
@login_required
def obnovit_kurs():
    currency = Currency()
    currency.check_currency()
    return render_template("obnovit_kurs.html", title='Ожидайте')


@app.route('/kurs_valut')
@login_required
def kurs_valut():
    with open('static/text/kurs.txt', 'r', encoding='utf-8') as f:
        uwu = []
        for line in f:
            uwu.append(str(line))
    k1 = str(uwu[0])
    k2 = str(uwu[1])
    k3 = str(uwu[2])
    k4 = str(uwu[3])
    k5 = str(uwu[4])
    k6 = str(uwu[5])
    k7 = str(uwu[6])
    k8 = str(uwu[7])
    k9 = str(uwu[8])
    v = str(uwu[9])
    return render_template("kurs_valut.html", k1=k1, k2=k2, k3=k3, k4=k4, k5=k5, k6=k6, k7=k7, k8=k8, k9=k9, vremya=v,
                           title='Курс Валют!')


@app.route('/shop')
@login_required
def shop():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    bal = int(user.balance)
    it = bal
    user.balance = str(it)
    db_sess.commit()
    return render_template("shop.html", svoya=svoya, it=it, title='Магазин')


@app.route('/boxe1')
@login_required
def boxe1():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    a = str(random.choice([1, 2, 3, 4, 5, 6, 7, 21, 22, 26]))
    p = f'\static\img\{a}.png'
    bd = f'sk_{a}'
    if bd == 'sk_1':
        b = int(user.sk_1)
        b += 1
        user.sk_1 = str(b)
        db_sess.commit()
    elif bd == 'sk_2':
        b = int(user.sk_2)
        b += 1
        user.sk_2 = str(b)
        db_sess.commit()
    elif bd == 'sk_3':
        b = int(user.sk_3)
        b += 1
        user.sk_3 = str(b)
        db_sess.commit()
    elif bd == 'sk_4':
        b = int(user.sk_4)
        b += 1
        user.sk_4 = str(b)
        db_sess.commit()
    elif bd == 'sk_5':
        b = int(user.sk_5)
        b += 1
        user.sk_5 = str(b)
        db_sess.commit()
    elif bd == 'sk_6':
        b = int(user.sk_6)
        b += 1
        user.sk_6 = str(b)
        db_sess.commit()
    elif bd == 'sk_7':
        b = int(user.sk_7)
        b += 1
        user.sk_7 = str(b)
        db_sess.commit()
    elif bd == 'sk_21':
        b = int(user.sk_21)
        b += 1
        user.sk_21 = str(b)
        db_sess.commit()
    elif bd == 'sk_22':
        b = int(user.sk_22)
        b += 1
        user.sk_22 = str(b)
        db_sess.commit()
    elif bd == 'sk_26':
        b = int(user.sk_26)
        b += 1
        user.sk_26 = str(b)
        db_sess.commit()
    else:
        print('Ошибка')
    return render_template("boxe1.html", k=p, title='Бокс1')


@app.route('/boxe2')
@login_required
def boxe2():
    a = str(random.choice([8, 9, 10, 11, 12, 13]))
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    p = f'\static\img\{a}.png'
    bd = f'sk_{a}'
    if bd == 'sk_8':
        b = int(user.sk_8)
        b += 1
        user.sk_8 = str(b)
        db_sess.commit()
    elif bd == 'sk_9':
        b = int(user.sk_9)
        b += 1
        user.sk_9 = str(b)
        db_sess.commit()
    elif bd == 'sk_10':
        b = int(user.sk_10)
        b += 1
        user.sk_10 = str(b)
        db_sess.commit()
    elif bd == 'sk_11':
        b = int(user.sk_11)
        b += 1
        user.sk_11 = str(b)
        db_sess.commit()
    elif bd == 'sk_12':
        b = int(user.sk_12)
        b += 1
        user.sk_12 = str(b)
        db_sess.commit()
    elif bd == 'sk_13':
        b = int(user.sk_13)
        b += 1
        user.sk_13 = str(b)
        db_sess.commit()
    else:
        print('Ошибка')
    return render_template("boxe2.html", k=p, title='Бокс2')


@app.route('/boxe3')
@login_required
def boxe3():
    a = str(random.choice([14, 15, 16, 17, 18, 19, 20]))
    p = f'\static\img\{a}.png'
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    bd = f'sk_{a}'
    if bd == 'sk_14':
        b = int(user.sk_14)
        b += 1
        user.sk_14 = str(b)
        db_sess.commit()
    elif bd == 'sk_15':
        b = int(user.sk_15)
        b += 1
        user.sk_15 = str(b)
        db_sess.commit()
    elif bd == 'sk_16':
        b = int(user.sk_16)
        b += 1
        user.sk_16 = str(b)
        db_sess.commit()
    elif bd == 'sk_17':
        b = int(user.sk_17)
        b += 1
        user.sk_17 = str(b)
        db_sess.commit()
    elif bd == 'sk_18':
        b = int(user.sk_18)
        b += 1
        user.sk_18 = str(b)
        db_sess.commit()
    elif bd == 'sk_19':
        b = int(user.sk_19)
        b += 1
        user.sk_19 = str(b)
        db_sess.commit()
    elif bd == 'sk_20':
        b = int(user.sk_20)
        b += 1
        user.sk_20 = str(b)
        db_sess.commit()
    else:
        print('Ошибка')
    return render_template("boxe3.html", k=p, title='Бокс3')


@app.route('/profil')
@login_required
def profil():
    return render_template("profil.html", svoya=svoya, title='Профиль')


@app.route('/invent')
@login_required
def invent():
    return render_template("invent.html", svoya=svoya, title='Инвентарь')


@app.route('/inc')
@login_required
def inc():
    return render_template("inc.html", svoya=svoya, title='Энциклопедия')


@app.route('/ava', methods=['GET', 'POST'])
@login_required
def ava():
    return render_template("ava.html", title='Аватарки')


@app.route('/sbrosava', methods=['GET', 'POST'])
@login_required
def sbrosava():
    return render_template("sbrosava.html", title='Сброс Аватарки')


@app.route('/podt/<int:avatarka>')
@login_required
def podt(avatarka):
    return render_template("podt.html", avatarka=str(avatarka), title='Подтвержение')


@app.route('/podt_prodat/<int:kogo>')
@login_required
def podt_prodat(kogo):
    return render_template("podt_prodat.html", kogo=str(kogo), title='Продать один')


@app.route('/podt_prodat_vse/<int:kto>')
@login_required
def podt_prodat_vse(kto):
    return render_template("podt_prodat_vse.html", kto=str(kto), title='Продать все')


@app.route('/pokupka/<int:kogo>')
@login_required
def pokupka(kogo):
    return render_template("pokupka.html", kogo=str(kogo), title='Покупка персонажа')


@app.route('/nedost')
@login_required
def nedost():
    return render_template("pokupka.html", title='Недостаточно средств')


@app.route('/ysp_pokupka/<int:ch>')
@login_required
def ysp_pokupka(ch):
    kto = ch
    bd = f'sk_{ch}'
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    if bd == 'sk_1':
        b = int(user.sk_1)
        b += 1
        user.sk_1 = str(b)
        bal = int(user.balance)
        it = bal - 100
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_2':
        b = int(user.sk_2)
        b += 1
        user.sk_2 = str(b)
        bal = int(user.balance)
        it = bal - 150
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_3':
        b = int(user.sk_3)
        b += 1
        user.sk_3 = str(b)
        bal = int(user.balance)
        it = bal - 100000
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_4':
        b = int(user.sk_4)
        b += 1
        user.sk_4 = str(b)
        bal = int(user.balance)
        it = bal - 200
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_5':
        b = int(user.sk_5)
        b += 1
        user.sk_5 = str(b)
        bal = int(user.balance)
        it = bal - 300
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_6':
        b = int(user.sk_6)
        b += 1
        user.sk_6 = str(b)
        bal = int(user.balance)
        it = bal - 500
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_7':
        b = int(user.sk_7)
        b += 1
        user.sk_7 = str(b)
        bal = int(user.balance)
        it = bal - 400
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_8':
        b = int(user.sk_8)
        b += 1
        user.sk_8 = str(b)
        bal = int(user.balance)
        it = bal - 450
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_9':
        b = int(user.sk_9)
        b += 1
        user.sk_9 = str(b)
        bal = int(user.balance)
        it = bal - 550
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_10':
        b = int(user.sk_10)
        b += 1
        user.sk_10 = str(b)
        bal = int(user.balance)
        it = bal - 600
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_11':
        b = int(user.sk_11)
        b += 1
        user.sk_11 = str(b)
        bal = int(user.balance)
        it = bal - 700
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_12':
        b = int(user.sk_12)
        b += 1
        user.sk_12 = str(b)
        bal = int(user.balance)
        it = bal - 800
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_13':
        b = int(user.sk_13)
        b += 1
        user.sk_13 = str(b)
        bal = int(user.balance)
        it = bal - 900
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_14':
        b = int(user.sk_14)
        b += 1
        user.sk_14 = str(b)
        bal = int(user.balance)
        it = bal - 1000
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_15':
        b = int(user.sk_15)
        b += 1
        user.sk_15 = str(b)
        bal = int(user.balance)
        it = bal - 1100
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_16':
        b = int(user.sk_16)
        b += 1
        user.sk_16 = str(b)
        bal = int(user.balance)
        it = bal - 1200
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_17':
        b = int(user.sk_17)
        b += 1
        user.sk_17 = str(b)
        bal = int(user.balance)
        it = bal - 1300
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_18':
        b = int(user.sk_18)
        b += 1
        user.sk_18 = str(b)
        bal = int(user.balance)
        it = bal - 1300
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_19':
        b = int(user.sk_19)
        b += 1
        user.sk_19 = str(b)
        bal = int(user.balance)
        it = bal - 2000
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_20':
        b = int(user.sk_20)
        b += 1
        user.sk_20 = str(b)
        bal = int(user.balance)
        it = bal - 1900
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_21':
        b = int(user.sk_21)
        b += 1
        user.sk_21 = str(b)
        bal = int(user.balance)
        it = bal - 3000
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_22':
        b = int(user.sk_22)
        b += 1
        user.sk_22 = str(b)
        bal = int(user.balance)
        it = bal - 5000
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    elif bd == 'sk_26':
        b = int(user.sk_26)
        b += 1
        user.sk_26 = str(b)
        bal = int(user.balance)
        it = bal - 10000
        if it < 0:
            db_sess.commit()
            return render_template("nedost.html", title='Недостаточно средств')
        else:
            user.balance = str(it)
            db_sess.commit()
    else:
        print('Ошибка')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    bal = int(user.balance)
    it = bal
    user.balance = str(it)
    db_sess.commit()
    return render_template("ysp_pokupka.html", itog=it, title='Успешно!')


@app.route('/ysp/<ch>')
@login_required
def ysp(ch):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    user.avatarka = str(ch)
    user.avatarka_svoya = None
    print(user.avatarka_svoya)
    db_sess.commit()
    return render_template("ysp.html", title='Успешно!')


@app.route('/ysp_p_odn/<ch>')
@login_required
def ysp_p_odn(ch):
    global b2
    bd = f'sk_{ch}'
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    kon = True
    if bd == 'sk_1':
        b2 = int(user.sk_1)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_1 = str(b2)
        db_sess.commit()
    elif bd == 'sk_2':
        b2 = int(user.sk_2)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_2 = str(b2)
        db_sess.commit()
    elif bd == 'sk_3':
        b2 = int(user.sk_3)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_3 = str(b2)
        db_sess.commit()
    elif bd == 'sk_4':
        b2 = int(user.sk_4)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_4 = str(b2)
        db_sess.commit()
    elif bd == 'sk_5':
        b2 = int(user.sk_5)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_5 = str(b2)
        db_sess.commit()
    elif bd == 'sk_6':
        b2 = int(user.sk_6)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_6 = str(b2)
        db_sess.commit()
    elif bd == 'sk_7':
        b2 = int(user.sk_7)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_7 = str(b2)
        db_sess.commit()
    elif bd == 'sk_8':
        b2 = int(user.sk_8)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_8 = str(b2)
        db_sess.commit()
    elif bd == 'sk_9':
        b2 = int(user.sk_9)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_9 = str(b2)
        db_sess.commit()
    elif bd == 'sk_10':
        b2 = int(user.sk_10)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_10 = str(b2)
        db_sess.commit()
    elif bd == 'sk_11':
        b2 = int(user.sk_11)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_11 = str(b2)
        db_sess.commit()
    elif bd == 'sk_12':
        b2 = int(user.sk_12)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_12 = str(b2)
        db_sess.commit()
    elif bd == 'sk_13':
        b2 = int(user.sk_13)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_13 = str(b2)
        db_sess.commit()
    elif bd == 'sk_14':
        b2 = int(user.sk_14)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_14 = str(b2)
        db_sess.commit()
    elif bd == 'sk_15':
        b2 = int(user.sk_15)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_15 = str(b2)
        db_sess.commit()
    elif bd == 'sk_16':
        b2 = int(user.sk_16)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_16 = str(b2)
        db_sess.commit()
    elif bd == 'sk_17':
        b2 = int(user.sk_17)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_17 = str(b2)
        db_sess.commit()
    elif bd == 'sk_18':
        b2 = int(user.sk_18)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_18 = str(b2)
        db_sess.commit()
    elif bd == 'sk_19':
        b2 = int(user.sk_19)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_19 = str(b2)
        db_sess.commit()
    elif bd == 'sk_20':
        b2 = int(user.sk_20)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_20 = str(b2)
        db_sess.commit()
    elif bd == 'sk_21':
        b2 = int(user.sk_21)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_21 = str(b2)
        db_sess.commit()
    elif bd == 'sk_22':
        b2 = int(user.sk_22)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_22 = str(b2)
        db_sess.commit()
    elif bd == 'sk_26':
        b2 = int(user.sk_26)
        b2 -= 1
        if b2 < 0:
            b2 = 0
            kon = False
        user.sk_26 = str(b2)
        db_sess.commit()
    if kon == True:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == int(chel)).first()
        if ch == '3' or ch == 3:
            balp = 10000
        else:
            balp = int(ch) * 25
        bal = int(user.balance)
        it = balp + bal
        user.balance = str(it)
        db_sess.commit()
    else:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == int(chel)).first()
        bal = int(user.balance)
        it = bal
        user.balance = str(it)
        db_sess.commit()
    return render_template("ysp_p_odn.html", itog=it, ch=str(ch), title='Успешно продан один!')


@app.route('/ysp_p_vse/<ch>')
@login_required
def ysp_p_vse(ch):
    global b3, sk_b
    bd = f'sk_{ch}'
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    if bd == 'sk_1':
        b3 = int(user.sk_1)
        sk_b = int(b3)
        b3 = 0
        user.sk_1 = str(b3)
        db_sess.commit()
    elif bd == 'sk_2':
        b3 = int(user.sk_2)
        sk_b = int(b3)
        b3 = 0
        user.sk_2 = str(b3)
        db_sess.commit()
    elif bd == 'sk_3':
        b3 = int(user.sk_3)
        sk_b = int(b3)
        b3 = 0
        user.sk_3 = str(b3)
        db_sess.commit()
    elif bd == 'sk_4':
        b3 = int(user.sk_4)
        sk_b = int(b3)
        b3 = 0
        user.sk_4 = str(b3)
        db_sess.commit()
    elif bd == 'sk_5':
        b3 = int(user.sk_5)
        sk_b = int(b3)
        b3 = 0
        user.sk_5 = str(b3)
        db_sess.commit()
    elif bd == 'sk_6':
        b3 = int(user.sk_6)
        sk_b = int(b3)
        b3 = 0
        user.sk_6 = str(b3)
        db_sess.commit()
    elif bd == 'sk_7':
        b3 = int(user.sk_7)
        sk_b = int(b3)
        b3 = 0
        user.sk_7 = str(b3)
        db_sess.commit()
    elif bd == 'sk_8':
        b3 = int(user.sk_8)
        sk_b = int(b3)
        b3 = 0
        user.sk_8 = str(b3)
        db_sess.commit()
    elif bd == 'sk_9':
        b3 = int(user.sk_9)
        sk_b = int(b3)
        b3 = 0
        user.sk_9 = str(b3)
        db_sess.commit()
    elif bd == 'sk_10':
        b3 = int(user.sk_10)
        sk_b = int(b3)
        b3 = 0
        user.sk_10 = str(b3)
        db_sess.commit()
    elif bd == 'sk_11':
        b3 = int(user.sk_11)
        sk_b = int(b3)
        b3 = 0
        user.sk_11 = str(b3)
        db_sess.commit()
    elif bd == 'sk_12':
        b3 = int(user.sk_12)
        sk_b = int(b3)
        b3 = 0
        user.sk_12 = str(b3)
        db_sess.commit()
    elif bd == 'sk_13':
        b3 = int(user.sk_13)
        sk_b = int(b3)
        b3 = 0
        user.sk_13 = str(b3)
        db_sess.commit()
    elif bd == 'sk_14':
        b3 = int(user.sk_14)
        sk_b = int(b3)
        b3 = 0
        user.sk_14 = str(b3)
        db_sess.commit()
    elif bd == 'sk_15':
        b3 = int(user.sk_15)
        sk_b = int(b3)
        b3 = 0
        user.sk_15 = str(b3)
        db_sess.commit()
    elif bd == 'sk_16':
        b3 = int(user.sk_16)
        sk_b = int(b3)
        b3 = 0
        user.sk_16 = str(b3)
        db_sess.commit()
    elif bd == 'sk_17':
        b3 = int(user.sk_17)
        sk_b = int(b3)
        b3 = 0
        user.sk_17 = str(b3)
        db_sess.commit()
    elif bd == 'sk_18':
        b3 = int(user.sk_18)
        sk_b = int(b3)
        b3 = 0
        user.sk_18 = str(b3)
        db_sess.commit()
    elif bd == 'sk_19':
        b3 = int(user.sk_19)
        sk_b = int(b3)
        b3 = 0
        user.sk_19 = str(b3)
        db_sess.commit()
    elif bd == 'sk_20':
        b3 = int(user.sk_20)
        sk_b = int(b3)
        b3 = 0
        user.sk_20 = str(b3)
        db_sess.commit()
    elif bd == 'sk_21':
        b3 = int(user.sk_21)
        sk_b = int(b3)
        b3 = 0
        user.sk_21 = str(b3)
        db_sess.commit()
    elif bd == 'sk_22':
        b3 = int(user.sk_22)
        sk_b = int(b3)
        b3 = 0
        user.sk_22 = str(b3)
        db_sess.commit()
    elif bd == 'sk_26':
        b3 = int(user.sk_26)
        sk_b = int(b3)
        b3 = 0
        user.sk_26 = str(b3)
        db_sess.commit()

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(chel)).first()
    if ch == '3' or ch == 3:
        balp = 10000 * sk_b
    else:
        balp = int(ch) * 25 * sk_b
    bal = int(user.balance)
    it = balp + bal
    user.balance = str(it)
    db_sess.commit()
    return render_template("ysp_p_vse.html", itog=it, ch=str(ch), title='Успешно проданы все!')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            email=form.email.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/polzovateli.sqlite")
    app.run(app.run(port=8080, host='127.0.0.1'))


if __name__ == '__main__':
    main()
