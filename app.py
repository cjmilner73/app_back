import json
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello():
    return {"hello": "world"}

if __name__ == '__main__':
    app.run(debug=True)

#from sqlalchemy import update
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app_user:oracle@localhost/tracker'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'hi'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class HoldingModel(db.Model):
    __tablename__ = 'holding'

    name = db.Column(db.String(), primary_key=True)
    id = db.Column(db.String())
    amount = db.Column(db.Integer)
    last_price = db.Column(db.DECIMAL(asdecimal=False))
    day_change = db.Column(db.DECIMAL(asdecimal=False))

    def __init__(self, id, name, amount, last_price, day_change):
        self.id = id
        self.name = name
        self.amount = amount
        self.last_price = last_price
        self.day_change = day_change

    def __repr__(self):
        return f"<Holding {self.name}>"

class TransHistModel(db.Model):
    __tablename__ = 'transhist'

    name = db.Column(db.String(), primary_key=True)
    amount = db.Column(db.Integer)
    buy_price = db.Column(db.DECIMAL(asdecimal=False))
    date = db.Column(db.Date)

    def __init__(self, name, amount, buy_price, date):
        self.name = name
        self.amount = amount
        self.buy_price = buy_price
        self.date = date

    def __repr__(self):
        return f"<TransHist {self.name}>"

class TotalHistModel(db.Model):
    __tablename__ = 'totalhist'

    time_stamp = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    def __init__(self, time_stamp, amount):
        self.time_stamp = time_stamp
        self.amount = amount

    def __repr__(self):
        return f"<TotalHist {self.name}>"

@app.route('/holdings', methods=['POST', 'GET'])
def handle_holdings():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            print(type(data))
            new_holding = HoldingModel(name=data['name'], id=data['id'], amount=data['amount'], last_price=data['last_price'], day_change=['day_change'])
            db.session.add(new_holding)
            db.session.commit()
            return {"message": f"holding {new_holding.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        holdings = HoldingModel.query.all()
        print('Forming results...')
        results = [
            {
                "name": holding.name,
                "id": holding.id,
		"amount": holding.amount,
		"last_price": holding.last_price,
		"day_change": holding.day_change
            } for holding in holdings]

        return {"holdings": results}

@app.route('/prices/<holding_name>', methods=['PUT'])
def handle_prices(holding_name):
    print('Handling a PUT' + holding_name)
    holding = HoldingModel.query.get_or_404(holding_name)
    if request.method == 'PUT':
        data = json.loads(request.get_json())
        print(data['name'])
        print('Printing last_price: ')
        print(data['last_price'])
        # holding.name = data['name']
        holding.id = data['id']
        holding.amount = data['amount']
        holding.last_price = data['last_price']
        holding.day_change = data['day_change']
        db.session.add(holding)
        db.session.commit()
        return {"message": f"holding {holding.name} successfully updated"}

@app.route('/totalhist', methods=['POST', 'GET'])
def handle_totalhist():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            print(type(data))
            new_totalhist = TotalHistModel(time_stamp=data['time_stamp'], amount=data['amount'])
            db.session.add(new_totalhist)
            db.session.commit()
            return {"message": f"holding {new_totalhist.time_stamp} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        totalhists = TotalHistModel.query.all()
        results = [
            {
                "time_stamp": totalhist.time_stamp,
		"amount": totalhist.amount,
            } for totalhist in totalhists]

        return {"totalhists": results}
