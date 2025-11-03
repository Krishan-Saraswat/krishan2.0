from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.Date, default=date.today)
    completed_date = db.Column(db.Date, nullable=True)

class DailyExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.Date, default=date.today)

class CreditCardExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_type = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.Date, default=date.today)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    remaining_amount = db.Column(db.Float, nullable=False)
    emi_amount = db.Column(db.Float, nullable=False)
    last_month_remaining = db.Column(db.Float, nullable=False)
    last_month_emi = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.Date, default=date.today)

class RecurringEMI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    created_date = db.Column(db.Date, default=date.today)

class MutualFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.Date, default=date.today)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.Date, default=date.today)

class StockTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(255), nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    sold_price = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.Date, default=date.today)
