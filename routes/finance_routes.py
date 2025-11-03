from flask import jsonify, request
from datetime import date, datetime, timedelta
from models.db_models import db, DailyExpense, CreditCardExpense, Loan, RecurringEMI, MutualFund, Stock, StockTransaction

def register_finance_routes(app):

    def get_date_range(start_date_str=None, end_date_str=None):
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = date.today()

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = end_date - timedelta(days=30)

        return start_date, end_date

    @app.route('/add-daily-expense', methods=['POST'])
    def add_daily_expense():
        data = request.json
        expense_date = data.get('date', date.today().isoformat())
        new_expense = DailyExpense(
            title=data['title'], 
            amount=data['amount'],
            created_date=datetime.strptime(expense_date, '%Y-%m-%d').date()
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({'success': True, 'id': new_expense.id})

    @app.route('/get-daily-expenses', methods=['GET'])
    def get_daily_expenses():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        start, end = get_date_range(start_date, end_date)

        expenses = DailyExpense.query.filter(
            DailyExpense.created_date >= start,
            DailyExpense.created_date <= end
        ).order_by(DailyExpense.created_date.desc()).all()

        return jsonify([{'id': e.id, 'title': e.title, 'amount': e.amount, 'date': str(e.created_date)} for e in expenses])

    @app.route('/delete-daily-expense/<int:expense_id>', methods=['POST'])
    def delete_daily_expense(expense_id):
        expense = DailyExpense.query.get(expense_id)
        if expense:
            db.session.delete(expense)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False})

    @app.route('/add-cc-expense', methods=['POST'])
    def add_cc_expense():
        data = request.json
        new_expense = CreditCardExpense(expense_type=data['type'], amount=data['amount'], card_type=data['card'])
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({'success': True, 'id': new_expense.id})

    @app.route('/get-cc-expenses', methods=['GET'])
    def get_cc_expenses():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        start, end = get_date_range(start_date, end_date)
        expenses = CreditCardExpense.query.filter(CreditCardExpense.created_date >= start, CreditCardExpense.created_date <= end).all()
        return jsonify([{'id': e.id, 'type': e.expense_type, 'amount': e.amount, 'card': e.card_type, 'date': str(e.created_date)} for e in expenses])

    @app.route('/delete-cc-expense/<int:expense_id>', methods=['POST'])
    def delete_cc_expense(expense_id):
        expense = CreditCardExpense.query.get(expense_id)
        if expense:
            db.session.delete(expense)
            db.session.commit()
        return jsonify({'success': True})

    @app.route('/add-loan', methods=['POST'])
    def add_loan():
        data = request.json
        new_loan = Loan(name=data['name'], remaining_amount=data['remaining'], emi_amount=data['emi'], last_month_remaining=data['last_remaining'], last_month_emi=data['last_emi'])
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({'success': True, 'id': new_loan.id})

    @app.route('/get-loans', methods=['GET'])
    def get_loans():
        loans = Loan.query.all()
        return jsonify([{'id': l.id, 'name': l.name, 'remaining': l.remaining_amount, 'emi': l.emi_amount, 'last_remaining': l.last_month_remaining, 'last_emi': l.last_month_emi} for l in loans])

    @app.route('/delete-loan/<int:loan_id>', methods=['POST'])
    def delete_loan(loan_id):
        loan = Loan.query.get(loan_id)
        if loan:
            db.session.delete(loan)
            db.session.commit()
        return jsonify({'success': True})

    @app.route('/add-emi', methods=['POST'])
    def add_emi():
        data = request.json
        new_emi = RecurringEMI(name=data['name'], amount=data['amount'], start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(), end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None)
        db.session.add(new_emi)
        db.session.commit()
        return jsonify({'success': True, 'id': new_emi.id})

    @app.route('/get-emis', methods=['GET'])
    def get_emis():
        emis = RecurringEMI.query.all()
        return jsonify([{'id': e.id, 'name': e.name, 'amount': e.amount, 'start_date': str(e.start_date), 'end_date': str(e.end_date) if e.end_date else None} for e in emis])

    @app.route('/delete-emi/<int:emi_id>', methods=['POST'])
    def delete_emi(emi_id):
        emi = RecurringEMI.query.get(emi_id)
        if emi:
            db.session.delete(emi)
            db.session.commit()
        return jsonify({'success': True})

    @app.route('/add-mutual-fund', methods=['POST'])
    def add_mutual_fund():
        data = request.json
        new_fund = MutualFund(fund_name=data['fund_name'], amount=data['amount'])
        db.session.add(new_fund)
        db.session.commit()
        return jsonify({'success': True, 'id': new_fund.id})

    @app.route('/get-mutual-funds', methods=['GET'])
    def get_mutual_funds():
        funds = MutualFund.query.all()
        total = sum(f.amount for f in funds)
        return jsonify({'funds': [{'id': f.id, 'fund_name': f.fund_name, 'amount': f.amount} for f in funds], 'total': total})

    @app.route('/delete-mutual-fund/<int:fund_id>', methods=['POST'])
    def delete_mutual_fund(fund_id):
        fund = MutualFund.query.get(fund_id)
        if fund:
            db.session.delete(fund)
            db.session.commit()
        return jsonify({'success': True})

    @app.route('/add-stock', methods=['POST'])
    def add_stock():
        data = request.json
        new_stock = Stock(stock_name=data['stock_name'], quantity=data['quantity'], current_price=data['current_price'])
        db.session.add(new_stock)
        db.session.commit()
        return jsonify({'success': True, 'id': new_stock.id})

    @app.route('/get-stocks', methods=['GET'])
    def get_stocks():
        stocks = Stock.query.all()
        total_value = sum(s.quantity * s.current_price for s in stocks)
        return jsonify({'stocks': [{'id': s.id, 'stock_name': s.stock_name, 'quantity': s.quantity, 'current_price': s.current_price, 'value': s.quantity * s.current_price} for s in stocks], 'total_value': total_value})

    @app.route('/delete-stock/<int:stock_id>', methods=['POST'])
    def delete_stock(stock_id):
        stock = Stock.query.get(stock_id)
        if stock:
            db.session.delete(stock)
            db.session.commit()
        return jsonify({'success': True})

    @app.route('/add-stock-transaction', methods=['POST'])
    def add_stock_transaction():
        data = request.json
        new_txn = StockTransaction(stock_name=data['stock_name'], purchase_price=data['purchase_price'], sold_price=data['sold_price'])
        db.session.add(new_txn)
        db.session.commit()
        return jsonify({'success': True, 'id': new_txn.id})

    @app.route('/get-stock-transactions', methods=['GET'])
    def get_stock_transactions():
        transactions = StockTransaction.query.all()
        return jsonify([{'id': t.id, 'stock_name': t.stock_name, 'purchase_price': t.purchase_price, 'sold_price': t.sold_price, 'gain_loss': t.sold_price - t.purchase_price} for t in transactions])

    @app.route('/delete-stock-transaction/<int:txn_id>', methods=['POST'])
    def delete_stock_transaction(txn_id):
        txn = StockTransaction.query.get(txn_id)
        if txn:
            db.session.delete(txn)
            db.session.commit()
        return jsonify({'success': True})
