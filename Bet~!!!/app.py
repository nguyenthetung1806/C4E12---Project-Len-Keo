from flask import Flask, render_template, request, redirect, session
from passlib.hash import sha256_crypt
import mlab
from base64 import b64encode
from bson.objectid import ObjectId
from mongoengine import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "piudfpasudfpa7wr09a113Q$ả$#2221y"

mlab.connect()

@app.route('/')
def index():
    return render_template('homepage.html')

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
    other_claiming_winner_bets = ListField()
    #friend notify about game
    bet_notification = ListField()

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
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
            message = "Tên đăng nhập đã tồn tại, vui lòng chọn tên khác"
            return render_template('message.html', message = message)



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        form = request.form
        username = form['username']
        password = form['password']
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            account = None
        if account is None:
            message = "Tài khoản không tồn tại"
            return render_template('message.html', message = message)
        else:
            if sha256_crypt.verify(password, account.password) == True:
                session["username"] = account.username
                url = "/profile/" + account.username
                return redirect(url)
            else:
                message = "Sai mật khẩu"
                return render_template('message.html', message = message)




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
        # add tất cả các user account vào 1 list , làm thế này để list ko chứa quá nhiều thông tin thừa
        for name_user in element.party_left:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        for name_user in element.party_left_pending:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        for name_user in element.party_right:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        for name_user in element.party_right_pending:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        for name_user in element.party_multiplayers:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        for name_user in element.party_multiplayers_pending:
            if name_user not in player_usernames:
                player_usernames.append(name_user)
        #end
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
    party_left_pending = ListField()####
    party_right_pending = ListField()####
    #multiparty
    party_multiplayers = ListField()
    party_multiplayers_pending = ListField()####
    number_of_winner = StringField()
    #
    spectator = ListField()
    punishment = StringField()
    #claim victory
    victory_claim = ListField()
    accept_verification_accept = ListField()
    accept_verification_decline = ListField()
    winner = ListField()
    loser  = ListField()


# for contract in Contract_type_1:
#     if contract.victory_claim in party_left:





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
            party_right_pending = form.getlist('party_right')
            party_left_pending = form.getlist('party_left')
            spectator = form.getlist('spectator')
            punishment = form['punishment']
            contract_type_1 = Contract_type_1(  contract_maker = contract_maker,
                                                contract_term = contract_term,
                                                party_left_pending = party_left_pending,
                                                party_right_pending = party_right_pending,
                                                spectator = spectator,
                                                punishment = punishment)
            contract_type_1.save()
            if username in party_left_pending:
                contract_type_1.update(pull__party_left_pending = username)
                contract_type_1.update(add_to_set__party_left = username)
            elif username in party_right_pending:
                contract_type_1.update(pull__party_right_pending = username)
                contract_type_1.update(add_to_set__party_right = username)
            account.update(add_to_set__active_bet = str(contract_type_1.id))
            for account_other in contract_type_1.party_right_pending:
                clone = Account.objects().get(username = account_other)
                clone.update(add_to_set__pending_bet = str(contract_type_1.id))
            for account_other_1 in contract_type_1.party_left_pending:
                clone = Account.objects().get(username = account_other_1)
                clone.update(add_to_set__pending_bet = str(contract_type_1.id))
            for account_other_spec in contract_type_1.spectator:
                clone = Account.objects().get(username = account_other_spec)
                clone.update(add_to_set__bet_notification = str(contract_type_1.id))
            url = '/profile/' + username
            return redirect(url)
        elif contract_class == "multiparty":
            contract_maker = username
            contract_term = form['contract_term']
            party_multiplayers_pending = form.getlist('party_multiplayers')
            number_of_winner = form['number_of_winner']
            spectator = form.getlist('spectator')
            punishment = form['punishment']
            contract_type_1 = Contract_type_1(  contract_maker = contract_maker,
                                                contract_term = contract_term,
                                                party_multiplayers_pending = party_multiplayers_pending,
                                                number_of_winner = number_of_winner,
                                                spectator = spectator,
                                                punishment = punishment)
            contract_type_1.save()
            contract_type_1.update(pull__party_multiplayers_pending = username)
            contract_type_1.update(add_to_set__party_multiplayers = username)
            account.update(add_to_set__active_bet = str(contract_type_1.id))
            for account_other in contract_type_1.party_multiplayers_pending:
                clone = Account.objects().get(username = account_other)
                clone.update(add_to_set__pending_bet = str(contract_type_1.id))
            for account_other_spec in contract_type_1.spectator:
                clone = Account.objects().get(username = account_other_spec)
                clone.update(add_to_set__bet_notification = str(contract_type_1.id))
            url = '/profile/' + username
            return redirect(url)
        #
        # for player in party_left and party_right:
        #     player_pending_bet = Account.objects.get(username = player)
        #     player_pending_bet.update(add_to_set__pending_bet = Contract_type_1.id)
        # account.update(add_to_set__friend_request_sent = account_other.username)
        # account_other.update(add_to_set__friend_accept_pending = account.username)


@app.route('/bet.request/<method>/<bet_id>', methods=['GET','POST'])
def bet_request_method(method, bet_id):
    username = session['username']
    account = Account.objects.get(username = username)
    bet = Contract_type_1.objects.with_id(bet_id)
    if method == "decline":
        if len(bet.party_multiplayers) == 0:
            if username in bet.party_right_pending:
                bet.update(pull__party_right_pending = account.username)
            elif username in bet.party_left_pending:
                bet.update(pull__party_left_pending = account.username)
        else:
            bet.update(pull__party_multiplayers_pending = account.username)
        account.update(pull__pending_bet = bet_id)
    elif method == "accept":
        if len(bet.party_multiplayers) == 0:
            if username in bet.party_right_pending:
                bet.update(pull__party_right_pending = account.username)
                bet.update(add_to_set__party_right = account.username)
            elif username in bet.party_left_pending:
                bet.update(pull__party_left_pending = account.username)
                bet.update(add_to_set__party_left = account.username)
        else:
            bet.update(pull__party_multiplayers_pending = account.username)
            bet.update(add_to_set__party_multiplayers = account.username)
        account.update(pull__pending_bet = bet_id)
        account.update(add_to_set__active_bet = bet_id)
    url = '/profile/' + username
    return redirect(url)



@app.route('/claim.victory/<username>/<bet_id>', methods=['GET','POST'])
def claim_victory(username, bet_id):
    username = session['username']
    account = Account.objects.get(username = username)
    bet = Contract_type_1.objects.with_id(bet_id)
    if len(bet.party_multiplayers) == 0:
        bet.update(add_to_set__victory_claim = account.username)
        if username in bet.party_right:
            for name_0 in bet.party_left:
                clone = Account.objects().get(username = name_0)
                clone.update(add_to_set__other_claiming_winner_bets = str(bet_id))
        if username in bet.party_left:
            for name_1 in bet.party_right:
                clone = Account.objects().get(username = name_1)
                clone.update(add_to_set__other_claiming_winner_bets = str(bet_id))
    else:
        bet.update(add_to_set__victory_claim = {'username' : account.username,
                                                'vote_count' : 0})
        for name_2 in bet.party_left:
            clone = Account.objects().get(username = name_2)
            clone.update(add_to_set__other_claiming_winner_bets = str(bet_id))
    url = '/profile/' + username
    return redirect(url)



@app.route('//bet.vote.victory/<method>/<bet_id>', methods=['GET','POST'])
def claim_victory(method, bet_id):
    username = session['username']
    account = Account.objects.get(username = username)
    bet = Contract_type_1.objects.with_id(bet_id)
    if len(bet.party_multiplayers) == 0:
        bet.update(add_to_set__accept_verification = username)
        if bet.victory_claim[0] in party_right:
            ### win condition
            if len(bet.accept_verification_accept) >= 2/3 * len(bet.party_left):
                ### winner actions
                for user_right in bet.party_right:
                    bet.update(add_to_set__winner = user_right)
                    clone = Account.objects().get(username = user_right)
                    account.update(pull__active_bet = bet_id)
                    clone.update(add_to_set__win_bet = bet_id)
                    clone.update(add_to_set__bet_notification = bet_id)
                ### loser actions
                for user_left in bet.party_left:
                    bet.update(add_to_set__loser = user_left)
                    clone = Account.objects().get(username = user_left)
                    account.update(pull__active_bet = bet_id)
                    clone.update(add_to_set__lost_bet = bet_id)
                    clone.update(add_to_set__bet_notification = bet_id)
            ### verification fail
            if len(bet.accept_verification_decline) >= 2/3 * len(bet.party_left):
                for user_right in bet.party_right:
                    clone = Account.objects().get(username = user_right)
                    clone.update(pull__other_claiming_winner_bets = bet_id)
                    bet.victory_claim = []
                    bet.accept_verification_accept = []
                    bet.accept_verification_decline = []
        elif bet.victory_claim[0] in party_left:
            ### win condition
            if len(bet.accept_verification_accept) >= 2/3 * len(bet.party_right):
                ### winner actions
                for user_left in bet.party_left:
                    bet.update(add_to_set__winner = user_left)
                    clone = Account.objects().get(username = user_left)
                    account.update(pull__active_bet = bet_id)
                    clone.update(add_to_set__win_bet = bet_id)
                    clone.update(add_to_set__bet_notification = bet_id)
                ### loser actions
                for user_right in bet.party_right:
                    bet.update(add_to_set__loser = user_right)
                    clone = Account.objects().get(username = user_right)
                    account.update(pull__active_bet = bet_id)
                    clone.update(add_to_set__lost_bet = bet_id)
                    clone.update(add_to_set__bet_notification = bet_id)
            ### verification fail
            if len(bet.accept_verification_decline) >= 2/3 * len(bet.party_right):
                for user_right in bet.party_right:
                    clone = Account.objects().get(username = user_right)
                    clone.update(pull__other_claiming_winner_bets = bet_id)
                    bet.victory_claim = []
                    bet.accept_verification_accept = []
                    bet.accept_verification_decline = []

    url = '/profile/' + username
    return redirect(url)

# class Contract_type_1(Document):
#     contract_maker = StringField()
#     contract_term = StringField()
#     #traditional\
#     party_left = ListField()
#     party_right = ListField()
#     party_left_pending = ListField()####
#     party_right_pending = ListField()####
#     #multiparty
#     party_multiplayers = ListField()
#     party_multiplayers_pending = ListField()####
#     number_of_winner = StringField()
#     #
#     spectator = ListField()
#     punishment = StringField()
#     #claim victory
#     victory_claim = ListField()
#     accept_verification = ListField()
#     winner = ListField()
#     loser  = ListField()


@app.route('/logout', methods = ['GET'])
def logout():
    del session['username']
    return redirect('/login')

if __name__ == '__main__':
  app.run(debug=True)
