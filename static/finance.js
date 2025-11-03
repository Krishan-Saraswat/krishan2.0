// Daily Expense
function addDailyExpense() {
    let title = document.getElementById("dailyExpenseTitle").value;
    let amount = document.getElementById("dailyExpenseAmount").value;
    if (!title.trim() || !amount) return;
    fetch("/add-daily-expense", { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({title: title, amount: parseFloat(amount)})})
    .then(resp => resp.json()).then(data => {
        if (data.success) {
            document.getElementById("dailyExpenseTitle").value = "";
            document.getElementById("dailyExpenseAmount").value = "";
            loadDailyExpenses();
        }
    });
}

function loadDailyExpenses() {
    fetch("/get-daily-expenses").then(resp => resp.json()).then(data => {
        let html = '';
        data.forEach(exp => {
            html += `<div class="expense-item"><div class="expense-info"><span class="expense-title">${exp.title}</span><span class="expense-date">${exp.date}</span></div><div class="expense-amount">₹${exp.amount.toFixed(2)}</div><button class="delete-btn" onclick="deleteDailyExpense(${exp.id})">×</button></div>`;
        });
        document.getElementById("dailyExpenseList").innerHTML = html || '<p class="no-tasks">No expenses</p>';
    });
}

function deleteDailyExpense(id) {
    fetch(`/delete-daily-expense/${id}`, { method: "POST" }).then(resp => resp.json()).then(data => { if (data.success) loadDailyExpenses(); });
}

// Credit Card
function addCCExpense() {
    let type = document.getElementById("ccExpenseType").value;
    let amount = document.getElementById("ccExpenseAmount").value;
    let card = document.getElementById("ccCardType").value;
    if (!type.trim() || !amount || !card) return;
    fetch("/add-cc-expense", { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({type: type, amount: parseFloat(amount), card: card})})
    .then(resp => resp.json()).then(data => {
        if (data.success) {
            document.getElementById("ccExpenseType").value = "";
            document.getElementById("ccExpenseAmount").value = "";
            document.getElementById("ccCardType").value = "";
            loadCCExpenses();
        }
    });
}

function loadCCExpenses() {
    fetch("/get-cc-expenses").then(resp => resp.json()).then(data => {
        let html = '';
        data.forEach(exp => {
            html += `<div class="expense-item"><div class="expense-info"><span class="expense-title">${exp.type} <span class="card-chip">${exp.card}</span></span><span class="expense-date">${exp.date}</span></div><div class="expense-amount">₹${exp.amount.toFixed(2)}</div><button class="delete-btn" onclick="deleteCCExpense(${exp.id})">×</button></div>`;
        });
        document.getElementById("ccExpenseList").innerHTML = html || '<p class="no-tasks">No expenses</p>';
    });
}

function deleteCCExpense(id) {
    fetch(`/delete-cc-expense/${id}`, { method: "POST" }).then(resp => resp.json()).then(data => { if (data.success) loadCCExpenses(); });
}

// Loans
function addLoan() {
    let name = document.getElementById("loanName").value;
    let remaining = document.getElementById("loanRemaining").value;
    let emi = document.getElementById("loanEMI").value;
    let lastRemaining = document.getElementById("loanLastRemaining").value;
    let lastEMI = document.getElementById("loanLastEMI").value;
    if (!name.trim() || !remaining || !emi || !lastRemaining || !lastEMI) return;
    fetch("/add-loan", { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({name: name, remaining: parseFloat(remaining), emi: parseFloat(emi), last_remaining: parseFloat(lastRemaining), last_emi: parseFloat(lastEMI)})})
    .then(resp => resp.json()).then(data => {
        if (data.success) {
            document.getElementById("loanName").value = "";
            document.getElementById("loanRemaining").value = "";
            document.getElementById("loanEMI").value = "";
            document.getElementById("loanLastRemaining").value = "";
            document.getElementById("loanLastEMI").value = "";
            document.getElementById("loanFormExtra").style.display = "none";
            loadLoans();
        }
    });
}

function loadLoans() {
    fetch("/get-loans").then(resp => resp.json()).then(data => {
        let html = '';
        data.forEach(loan => {
            html += `<div class="loan-item"><div class="loan-header"><strong>${loan.name}</strong><button class="delete-btn" onclick="deleteLoan(${loan.id})">×</button></div><div class="loan-details"><div class="loan-detail-row"><span class="label">Remaining:</span><span class="value">₹${loan.remaining.toFixed(2)}</span></div><div class="loan-detail-row"><span class="label">EMI:</span><span class="value">₹${loan.emi.toFixed(2)}</span></div><div class="loan-detail-row"><span class="label">Last Month Rem:</span><span class="value">₹${loan.last_remaining.toFixed(2)}</span></div><div class="loan-detail-row"><span class="label">Last Month EMI:</span><span class="value">₹${loan.last_emi.toFixed(2)}</span></div></div></div>`;
        });
        document.getElementById("loanList").innerHTML = html || '<p class="no-tasks">No loans</p>';
    });
}

function deleteLoan(id) {
    fetch(`/delete-loan/${id}`, { method: "POST" }).then(resp => resp.json()).then(data => { if (data.success) loadLoans(); });
}

// EMI
function addEMI() {
    let name = document.getElementById("emiName").value;
    let amount = document.getElementById("emiAmount").value;
    let startDate = document.getElementById("emiStartDate").value;
    let endDate = document.getElementById("emiEndDate").value;
    if (!name.trim() || !amount || !startDate) return;
    fetch("/add-emi", { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({name: name, amount: parseFloat(amount), start_date: startDate, end_date: endDate || null})})
    .then(resp => resp.json()).then(data => {
        if (data.success) {
            document.getElementById("emiName").value = "";
            document.getElementById("emiAmount").value = "";
            document.getElementById("emiStartDate").value = "";
            document.getElementById("emiEndDate").value = "";
            loadEMIs();
        }
    });
}

function loadEMIs() {
    fetch("/get-emis").then(resp => resp.json()).then(data => {
        let html = '';
        data.forEach(emi => {
            html += `<div class="expense-item"><div class="expense-info"><span class="expense-title">${emi.name}</span><span class="expense-date">${emi.start_date} → ${emi.end_date || 'Ongoing'}</span></div><div class="expense-amount">₹${emi.amount.toFixed(2)}</div><button class="delete-btn" onclick="deleteEMI(${emi.id})">×</button></div>`;
        });
        document.getElementById("emiList").innerHTML = html || '<p class="no-tasks">No EMIs</p>';
    });
}

function deleteEMI(id) {
    fetch(`/delete-emi/${id}`, { method: "POST" }).then(resp => resp.json()).then(data => { if (data.success) loadEMIs(); });
}

// Mutual Fund
function addMutualFund() {
    let fundName = document.getElementById("fundName").value;
    let amount = document.getElementById("fundAmount").value;
    if (!fundName.trim() || !amount) return;
    fetch("/add-mutual-fund", { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({fund_name: fundName, amount: parseFloat(amount)})})
    .then(resp => resp.json()).then(data => { if (data.success) { document.getElementById("fundName").value = ""; document.getElementById("fundAmount").value = ""; loadMutualFunds(); } });
}

function loadMutualFunds() {
    fetch("/get-mutual-funds").then(resp => resp.json()).then(data => {
        let html = '<div class="investment-item header"><span class="fund-num">Item</span><span class="fund-name">Fund Name</span><span class="fund-amount">Amount</span></div>';
        data.funds.forEach((fund, index) => {
            html += `<div class="investment-item"><span class="fund-num">${index + 1}</span><span class="fund-name">${fund.fund_name}</span><span class="fund-amount">₹${fund.amount.toFixed(2)} <button class="delete-btn" onclick="deleteMutualFund(${fund.id})">×</button></span></div>`;
        });
        document.getElementById("mutualFundList").innerHTML = html;
        document.getElementById("mfTotal").innerText = `₹${data.total.toFixed(2)}`;
        updateTotalCorpus();
    });
}

function deleteMutualFund(id) {
    fetch(`/delete-mutual-fund/${id}`, { method: "POST" }).then(resp => resp.json()).then(data => { if (data.success) loadMutualFunds(); });
}

// Stocks
function addStock() {
    let stockName = document.getElementById("stockName").value;
    let quantity = document.getElementById("stockQuantity").value;
    let price = document.getElementById("stockPrice").value;
    if (!stockName.trim() || !quantity || !price) return;
    fetch("/add-stock", { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({stock_name: stockName, quantity: parseFloat(quantity), current_price: parseFloat(price)})})
    .then(resp => resp.json()).then(data => { if (data.success) { document.getElementById("stockName").value = ""; document.getElementById("stockQuantity").value = ""; document.getElementById("stockPrice").value = ""; loadStocks(); } });
}

function loadStocks() {
    fetch("/get-stocks").then(resp => resp.json()).then(data => {
        let html = '<div class="investment-item header"><span class="stock-num">Item</span><span class="stock-name">Stock Name</span><span class="stock-value">Value</span></div>';
        data.stocks.forEach((stock, index) => {
            html += `<div class="investment-item"><span class="stock-num">${index + 1}</span><span class="stock-name">${stock.stock_name}</span><span class="stock-value">₹${stock.value.toFixed(2)} <button class="delete-btn" onclick="deleteStock(${stock.id})">×</button></span></div>`;
        });
        document.getElementById("stocksList").innerHTML = html;
        document.getElementById("stockTotal").innerText = `₹${data.total_value.toFixed(2)}`;
        updateTotalCorpus();
    });
}

function deleteStock(id) {
    fetch(`/delete-stock/${id}`, { method: "POST" }).then(resp => resp.json()).then(data => { if (data.success) loadStocks(); });
}

// Stock Transaction
function addStockTransaction() {
    let stockName = document.getElementById("txnStockName").value;
    let purchasePrice = document.getElementById("txnPurchasePrice").value;
    let soldPrice = document.getElementById("txnSoldPrice").value;
    if (!stockName.trim() || !purchasePrice || !soldPrice) return;
    fetch("/add-stock-transaction", { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({stock_name: stockName, purchase_price: parseFloat(purchasePrice), sold_price: parseFloat(soldPrice)})})
    .then(resp => resp.json()).then(data => { if (data.success) { document.getElementById("txnStockName").value = ""; document.getElementById("txnPurchasePrice").value = ""; document.getElementById("txnSoldPrice").value = ""; loadStockTransactions(); } });
}

function loadStockTransactions() {
    fetch("/get-stock-transactions").then(resp => resp.json()).then(data => {
        let html = '<div class="investment-item header"><span class="txn-name">Stock Name</span><span class="txn-purchase">Purchase</span><span class="txn-sold">Sold</span><span class="txn-gain">Gain/Loss</span></div>';
        data.forEach(txn => {
            let gainLossClass = txn.gain_loss >= 0 ? 'positive' : 'negative';
            html += `<div class="investment-item"><span class="txn-name">${txn.stock_name}</span><span class="txn-purchase">₹${txn.purchase_price.toFixed(2)}</span><span class="txn-sold">₹${txn.sold_price.toFixed(2)}</span><span class="txn-gain ${gainLossClass}">₹${txn.gain_loss.toFixed(2)} <button class="delete-btn" onclick="deleteStockTransaction(${txn.id})">×</button></span></div>`;
        });
        document.getElementById("stockTransactionList").innerHTML = html || '<p class="no-tasks">No transactions</p>';
    });
}

function deleteStockTransaction(id) {
    fetch(`/delete-stock-transaction/${id}`, { method: "POST" }).then(resp => resp.json()).then(data => { if (data.success) loadStockTransactions(); });
}

// Update Total Corpus
function updateTotalCorpus() {
    let mfTotal = parseFloat(document.getElementById("mfTotal").innerText.replace('₹', '')) || 0;
    let stockTotal = parseFloat(document.getElementById("stockTotal").innerText.replace('₹', '')) || 0;
    let totalCorpus = mfTotal + stockTotal;
    document.getElementById("totalMutualFunds").innerText = `₹${mfTotal.toFixed(2)}`;
    document.getElementById("totalStocks").innerText = `₹${stockTotal.toFixed(2)}`;
    document.getElementById("totalCorpusValue").innerText = `₹${totalCorpus.toFixed(2)}`;
}
