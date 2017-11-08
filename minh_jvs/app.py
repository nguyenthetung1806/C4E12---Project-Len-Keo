from flask import Flask, render_template, request, redirect, session
from passlib.hash import sha256_crypt
import mlab
from base64 import b64encode
from bson.objectid import ObjectId
from mongoengine import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "piudfpasudfpa7wr09 21y"

mlab.connect()

class Account(Document):
    username = StringField()
    name = StringField()
    image = StringField()
    password = StringField()
    email = EmailField()
    phone = StringField()
    #friend system
    friendlist = ListField()
    friend_request_sent = ListField()
    friend_accept_pending = ListField()
    #
    #bet system
    pending_bet = ListField()
    active_bet = ListField()
    win_bet = ListField()
    lost_bet = ListField()





@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "GET":
        prompt=0
        return render_template('signup.html',prompt=prompt)
    elif request.method == "POST":
        form = request.form
        username = form['username']
        password = sha256_crypt.encrypt(form['password'])
        name = form['name']
        email = form['email']
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            account = None
        if account is None:
            account = Account(name=name, password=password, username=username, email=email)
            account.save()
            return redirect('/login')
        else:
            prompt=1
            return render_template('signup.html',prompt=prompt)
            # message = "Tên đăng nhập đã tồn tại, vui lòng chọn tên khác"
            # return render_template('message.html', message = message)



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        prompt=0
        return render_template('login.html',prompt=prompt)
    elif request.method == "POST":
        form = request.form
        username = form['username']
        password = form['password']
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            account = None
        if account is None:
            prompt=1
            # message = "Tài khoản không tồn tại"
            return render_template('login.html', prompt = prompt)
        else:
            if sha256_crypt.verify(password, account.password) == True:
                session["username"] = account.username
                url = "/profile/" + account.username
                return redirect(url)
            else:
                # message = "Sai mật khẩu"
                prompt=2
                return render_template('login.html', prompt = prompt)




@app.route('/profile/<username_url>', methods=['GET','POST'])
def profile(username_url):
    username = session['username']
    username_url = username_url
    account = Account.objects.get(username = username)
    account_other = Account.objects.get(username = username_url)
    bets_to_show = []
    for bet in account_other.active_bet:
        bets_to_show.append(Contract_type_1.objects().with_id(bet))

    # dùng để nhét các document player tham gia kèo vào player_to_show []
    player_usernames = []
    for element in bets_to_show:
        for name_user in element.party_left:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        for name_user in element.party_right:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        for name_user in element.party_multiplayers:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
    players_to_show = []
    for username_each in player_usernames:
            players_to_show.append(Account.objects.get(username = username_each))
    # xong

    return render_template('profile.html',  account = account,
                                            account_other = account_other,
                                            username = username,
                                            username_url = username_url,
                                            bets_to_show = bets_to_show,
                                            players_to_show = players_to_show)




@app.route('/edit.profile/<username_url>', methods=['GET','POST'])
def edit_profile(username_url):
    account = Account.objects.get(username = username_url)
    if request.method == "GET":
        return render_template('edit_profile.html', account = account)
    elif request.method == "POST":
        form = request.form
        name = form['name']
        email = form['email']
        phone = form['phone']
        image = request.files['image']
        image = b64encode(image.read()).decode("utf-8")
        account.update(name = name, image = image, email = email, phone = phone)
        url = '/edit.profile/' + username_url
        return redirect(url)




@app.route('/friend.request/<method>/<username_url>', methods=['GET','POST'])
def friend_request_method(method, username_url):
    username = session['username']
    account = Account.objects.get(username = username)
    account_other = Account.objects.get(username = username_url)
    url = '/profile/' + username_url
    if method == "delete.friend":
        account.update(pull__friendlist = account_other.username)
        account_other.update(pull__friendlist = account.username)
        return redirect(url)
    elif method == "cancel":
        account.update(pull__friend_request_sent = account_other.username)
        account_other.update(pull__friend_accept_pending = account.username)
        return redirect(url)
    elif method == "accept":
        account.update(add_to_set__friendlist = account_other.username)
        account.update(pull__friend_accept_pending = account_other.username)
        account_other.update(add_to_set__friendlist = account.username)
        account_other.update(pull__friend_request_sent = account.username)
        return redirect(url)
    elif method == "send.request":
        account.update(add_to_set__friend_request_sent = account_other.username)
        account_other.update(add_to_set__friend_accept_pending = account.username)
        return redirect(url)
    elif method == "decline":
        account.update(pull__friend_accept_pending = account_other.username)
        account_other.update(pull__friend_request_sent = account.username)
        return redirect(url)



    # friendlist = ListField()
    # friend_request_sent = ListField()
    # friend_accept_pending = ListField()




class Contract_type_1(Document):
    contract_maker = StringField()
    contract_term = StringField()
    #traditional\
    party_left = ListField()
    party_right = ListField()
    #multiparty
    party_multiplayers = ListField()
    number_of_winner = StringField()
    #
    spectator = ListField()
    punishment = StringField()
    #claim victory
    victory_claim = StringField()
    winner = ListField()
    loser  = ListField()


# for contract in Contract_type_1:
#     if contract.victory_claim in party_left:



@app.route('/claim.victory/<username>/<contract_id>', methods=['GET','POST'])
def claim_victory(username,contract_id):
    contract_type_1 = Contract_type_1.objects().with_id(contract_id)
    contract_type_1.update(add_to_set__victory_claim = username)
    url = '/profile/' + username
    return redirect(url)


@app.route('/contract.type.1/<contract_class>', methods=['GET','POST'])
def contract_type_1(contract_class):
    username = session['username']
    account = Account.objects.get(username = username)

    friendlist_information = []
    for friend in account.friendlist:
        friendlist_information.append(Account.objects().get(username = friend))
    if request.method == "GET":
        if contract_class == "traditional":
            return render_template('contract_type_1_traditional.html', account = account, friendlist_information = friendlist_information)
        elif contract_class == "multiparty":
            return render_template('contract_type_1_multiparty.html', account = account, friendlist_information = friendlist_information)
    elif request.method == "POST":
        form = request.form
        if contract_class == "traditional":
            contract_maker = username
            contract_term = form['contract_term']
            party_right = form.getlist('party_right')
            party_left = form.getlist('party_left')
            spectator = form.getlist('spectator')
            punishment = form['punishment']
            contract_type_1 = Contract_type_1(  contract_maker = contract_maker,
                                                contract_term = contract_term,
                                                party_left = party_left,
                                                party_right = party_right,
                                                spectator = spectator,
                                                punishment = punishment)
            contract_type_1.save()
            account.update(add_to_set__active_bet = str(contract_type_1.id))
            url = '/profile/' + username
            return redirect(url)
        elif contract_class == "multiparty":
            contract_maker = username
            contract_term = form['contract_term']
            party_multiplayers = form.getlist('party_multiplayers')
            number_of_winner = form['number_of_winner']
            spectator = form.getlist('spectator')
            punishment = form['punishment']
            contract_type_1 = Contract_type_1(  contract_maker = contract_maker,
                                                contract_term = contract_term,
                                                party_multiplayers = party_multiplayers,
                                                number_of_winner = number_of_winner,
                                                spectator = spectator,
                                                punishment = punishment)
            contract_type_1.save()
            account.update(add_to_set__active_bet = str(contract_type_1.id))
            url = '/profile/' + username
            return redirect(url)
        #
        # for player in party_left and party_right:
        #     player_pending_bet = Account.objects.get(username = player)
        #     player_pending_bet.update(add_to_set__pending_bet = Contract_type_1.id)
        # account.update(add_to_set__friend_request_sent = account_other.username)
        # account_other.update(add_to_set__friend_accept_pending = account.username)


@app.route('/logout', methods = ['GET'])
def logout():
    del session['username']
    return redirect('/login')

if __name__ == '__main__':
  app.run(debug=True)
