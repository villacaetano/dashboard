from bs4 import BeautifulSoup
from pathlib import Path
root=Path('/mnt/data/v4')
s=BeautifulSoup((root/'index.html').read_text(),'html.parser')
s.body['data-page']='transactions'
main=s.find('main')
main.clear()
main.append(BeautifulSoup('''<div class="container-fluid px-3 px-lg-4 py-4">
<div class="page-heading"><div class="page-heading-copy"><span class="page-icon"><i class="bi bi-arrow-left-right"></i></span><div><p class="eyebrow mb-1">Financials</p><h1 class="h3 mb-1">Transactions</h1><p class="text-muted mb-0">A complete view of recorded income, one-off expenses and billing.</p></div></div></div>
<div class="panel"><div class="panel-header"><div><h2 class="h5 mb-1 section-title"><i class="bi bi-filter-circle"></i><span>Transaction Register</span></h2><p class="text-muted mb-0">Filter by type, category and month whenever you need a report.</p></div></div>
<div class="vc-filter-row vc-filter-row-wide"><select id="transaction-filter-type" class="form-select form-select-sm"><option value="">All types</option><option value="Income">Income</option><option value="Expense">Expense</option><option value="Billing">Billing</option></select><select id="transaction-filter-category" class="form-select form-select-sm"><option value="">All categories</option><option value="Property Income">Property Income</option><option value="Repairs">Repairs</option><option value="Cleaning">Cleaning</option><option value="Replacement">Replacement</option><option value="Plumbing">Plumbing</option><option value="Electrical">Electrical</option><option value="Garden">Garden</option><option value="Pool">Pool</option><option value="Pest Control">Pest Control</option><option value="Supplies">Supplies</option><option value="Transport / Delivery">Transport / Delivery</option><option value="Appliances">Appliances</option><option value="Electricity">Electricity</option><option value="Water">Water</option><option value="Internet">Internet</option><option value="Gas">Gas</option><option value="Gardener">Gardener</option><option value="Other">Other</option></select><input id="transaction-filter-month" type="month" class="form-control form-control-sm"><input id="transaction-search" type="search" class="form-control form-control-sm" placeholder="Search transactions..."></div>
<div class="table-responsive"><table class="table align-middle mb-0"><thead><tr><th>Date</th><th>Type</th><th>Category</th><th>Description</th><th>Paid / Received By</th><th class="text-end">Amount</th></tr></thead><tbody id="transactions-table"></tbody></table></div></div>
</div>''','html.parser'))
(root/'transactions.html').write_text('<!DOCTYPE html>\n'+s.prettify())
