from bs4 import BeautifulSoup
from pathlib import Path
root=Path('/mnt/data/v4')

def soup(f): return BeautifulSoup((root/f).read_text(), 'html.parser')
def save(f,s): (root/f).write_text('<!DOCTYPE html>\n'+s.prettify())

def nav_update(s):
    for a in s.select('.sidebar-nav .nav-link'):
        txt=a.select_one('.nav-text')
        if txt and txt.get_text(strip=True)=='Monthly Billing': txt.string='Billing'
        if a.get('href')=='index.html#transactions': a['href']='transactions.html'; a['data-page']='transactions'

# dashboard
s=soup('index.html'); nav_update(s)
# compact income breakdown
p=s.select_one('.income-breakdown-panel')
if p:
    p.select_one('.panel-header p').string='Manager share and TDS are shown separately from owner cashflow.'
    p['class'] += ['income-breakdown-thin']
    for x in p.select('.vc-breakdown-item'):
        x['class'] += ['vc-breakdown-thin-item']
# trend title copy
trend=s.find(id='trend-chart')
if trend:
    trend['class']=['vc-trend-chart']
    parent=trend.find_parent('div',class_='panel')
    if parent:
        desc=parent.select_one('.panel-header p');
        if desc: desc.string='Net owner revenue over the latest six months.'
# owner expenses description
for card in s.select('.metric-card'):
    if card.select_one('#owner-expenses'):
        meta=card.select_one('.metric-meta span');
        if meta: meta.string='One-off expenses + owner-paid bills'
s.save if False else None
save('index.html',s)

# income
s=soup('income.html'); nav_update(s)
main=s.find('main');
# add filter month next to search
panel=main.select_one('.income-register-panel') or main.select_one('.col-xl-7 .panel')
if panel: panel['class']=['panel','income-register-panel']
search=main.find(id='income-search')
if search:
    wrap=search.parent
    filt=s.new_tag('input',id='income-filter-month',type='month',class_='form-control form-control-sm',style='max-width:155px',aria_label='Filter income by month')
    wrap.insert(0,filt)
# compact form column and wording
left=main.select_one('.col-xl-5');
if left: left['class']=['col-12','col-xl-4']
right=main.select_one('.col-xl-7');
if right: right['class']=['col-12','col-xl-8']
# Add a tiny summary strip above records
reg=main.select_one('.income-register-panel')
if reg:
    hdr=reg.select_one('.panel-header')
    if hdr:
        strip=s.new_tag('div',attrs={'class':'vc-register-summary'})
        for ident,label in [('income-owner-total','Owner received'),('income-manager-total','Manager share'),('income-tds-total','TDS')]:
            item=s.new_tag('div',attrs={'class':'vc-register-summary-item'}); span=s.new_tag('span'); span.string=label; strong=s.new_tag('strong',id=ident); strong.string='₹0'; item.extend([span,strong]); strip.append(item)
        reg.insert(1,strip)
save('income.html',s)

# expenses
s=soup('expenses.html'); nav_update(s); main=s.find('main')
# heading action remove monthly billing and add income link
for a in main.select('.heading-actions a'):
    if 'monthly-billing' in (a.get('href') or ''): a.decompose()
# add chart panel before row
row=main.select_one('.row.g-3')
chart_panel=s.new_tag('div',attrs={'class':'panel mb-3'})
chart_panel.append(BeautifulSoup('''<div class="panel-header"><div><h2 class="h5 mb-1 section-title"><i class="bi bi-bar-chart"></i><span>Monthly One-off Expenses</span></h2><p class="text-muted mb-0">Your exceptional owner expenses over the latest six months.</p></div></div><div id="expense-chart" class="vc-expense-chart"></div>''','html.parser'))
if row: row.insert_before(chart_panel)
# filters in register header
reg=main.select_one('.col-xl-8 .panel');
if reg:
    hdr=reg.select_one('.panel-header');
    tools=s.new_tag('div',attrs={'class':'vc-filter-row'})
    for tag,attrs in [('input',{'id':'expense-filter-month','type':'month','class':'form-control form-control-sm'}),('select',{'id':'expense-filter-category','class':'form-select form-select-sm'}) ,('input',{'id':'expense-search','type':'search','class':'form-control form-control-sm','placeholder':'Search...'})]:
        el=s.new_tag(tag,attrs=attrs); tools.append(el)
    sel=tools.select_one('#expense-filter-category'); opt=s.new_tag('option',value=''); opt.string='All categories'; sel.append(opt)
    for c in ["Repairs","Cleaning","Replacement","Plumbing","Electrical","Garden","Pool","Pest Control","Supplies","Transport / Delivery","Appliances","Other"]:
        o=s.new_tag('option',value=c);o.string=c;sel.append(o)
    hdr.append(tools)
# form add notes and more categories
form=main.find(id='expense-form')
if form:
    sel=form.select_one('select[name=category]'); sel.clear()
    for c in ["Repairs","Cleaning","Replacement","Plumbing","Electrical","Garden","Pool","Pest Control","Supplies","Transport / Delivery","Appliances","Other"]:
        o=s.new_tag('option',value=c);o.string=c;sel.append(o)
    desc=form.find(id='expense-description');
    if desc: desc['readonly']=True; desc['class'] += ['bg-light']
    amount=form.find('input',attrs={'name':'amount'}); notes=s.new_tag('div',attrs={'class':'mb-3'}); lab=s.new_tag('label',attrs={'class':'form-label'});lab.string='Notes / Details'; ta=s.new_tag('textarea',attrs={'id':'expense-notes','name':'notes','class':'form-control','rows':'2','placeholder':'What happened? e.g. one glass broke and was replaced.'}); notes.extend([lab,ta]); amount.parent.insert_after(notes)
save('expenses.html',s)

# billing
s=soup('monthly-billing.html'); nav_update(s); main=s.find('main')
# title and copy
h=main.find('h1'); h.string='Billing'
# Replace top summary with recurring + summary row
old=main.select_one('.panel.mb-3')
if old:
    old.decompose()
# Build billing overview
row=s.new_tag('div',attrs={'class':'row g-3 mb-3'})
left=s.new_tag('div',attrs={'class':'col-12 col-xl-7'}); p=s.new_tag('div',attrs={'class':'panel h-100'})
p.append(BeautifulSoup('''<div class="panel-header"><div><h2 class="h5 mb-1 section-title"><i class="bi bi-arrow-repeat"></i><span>Recurring Monthly Costs</span></h2><p class="text-muted mb-0">Set the usual monthly amounts once, then apply them to a selected month.</p></div><button type="button" class="btn btn-vc btn-sm" id="save-recurring"><i class="bi bi-check2"></i> Save Defaults</button></div><div class="row g-2" id="recurring-costs"></div><div class="mt-3 d-flex gap-2 align-items-center"><button type="button" class="btn btn-outline-primary btn-sm" id="apply-recurring"><i class="bi bi-calendar-plus"></i> Apply recurring costs</button><span class="small text-muted">Electricity and Water are entered separately because they vary monthly.</span></div>''','html.parser'))
left.append(p)
right=s.new_tag('div',attrs={'class':'col-12 col-xl-5'}); p2=s.new_tag('div',attrs={'class':'panel h-100'})
p2.append(BeautifulSoup('''<div class="panel-header"><div><h2 class="h5 mb-1 section-title"><i class="bi bi-lightning-charge"></i><span>Water & Electricity</span></h2><p class="text-muted mb-0">Monthly record for variable utility costs.</p></div></div><div class="table-responsive"><table class="table align-middle mb-0"><thead><tr><th>Month</th><th class="text-end">Water</th><th class="text-end">Electricity</th></tr></thead><tbody id="water-electricity-table"></tbody></table></div>''','html.parser')); right.append(p2); row.extend([left,right]);
main.insert(1,row)
# add filters to billing register header
reg=main.select_one('.col-xl-8 .panel');
if reg:
    hdr=reg.select_one('.panel-header'); tools=s.new_tag('div',attrs={'class':'vc-filter-row'})
    for tag,attrs in [('input',{'id':'billing-filter-month','type':'month','class':'form-control form-control-sm'}),('select',{'id':'billing-filter-category','class':'form-select form-select-sm'}),('select',{'id':'billing-filter-paid','class':'form-select form-select-sm'})]: tools.append(s.new_tag(tag,attrs=attrs))
    for id_,items,first in [('billing-filter-category',["Electricity","Water","Internet","Gas","Pool","Gardener","Cleaning","Other"],'All bills'),('billing-filter-paid',["Property Manager","Owner"],'Paid by')]:
        sel=tools.select_one('#'+id_); o=s.new_tag('option',value='');o.string=first;sel.append(o)
        for c in items:o=s.new_tag('option',value=c);o.string=c;sel.append(o)
    hdr.append(tools)
# form description readonly auto
bd=main.find(id='billing-description');
if bd: bd['readonly']=True; bd['class'] += ['bg-light']
sel=main.select_one('#billing-form select[name=category]');
if sel:
    sel.clear()
    for c in ["Electricity","Water","Internet","Gas","Pool","Gardener","Cleaning","Other"]:
        o=s.new_tag('option',value=c);o.string=c;sel.append(o)
# change button label
btn=main.select_one('#billing-form button[type=submit]');
if btn: btn.contents[-1].replace_with(' Add Bill')
save('monthly-billing.html',s)

# issues filters
s=soup('issues.html'); nav_update(s); main=s.find('main'); reg=main.select_one('.col-xl-8 .panel');
if reg:
    hdr=reg.select_one('.panel-header'); tools=s.new_tag('div',attrs={'class':'vc-filter-row'})
    for tag,attrs in [('select',{'id':'issue-filter-status','class':'form-select form-select-sm'}),('select',{'id':'issue-filter-priority','class':'form-select form-select-sm'}),('input',{'id':'issue-search','type':'search','class':'form-control form-control-sm','placeholder':'Search...'})]: tools.append(s.new_tag(tag,attrs=attrs))
    for id_,items,first in [('issue-filter-status',["Open","In Progress","Resolved"],'All statuses'),('issue-filter-priority',["High","Medium","Low"],'All priorities')]:
        sel=tools.select_one('#'+id_);o=s.new_tag('option',value='');o.string=first;sel.append(o)
        for c in items:o=s.new_tag('option',value=c);o.string=c;sel.append(o)
    hdr.append(tools)
# add required monetary field / contractor tick
form=main.find(id='issue-form')
if form:
    due=form.find(id='issue-due-date')
    block=s.new_tag('div',attrs={'class':'mb-3'}); block.append(BeautifulSoup('''<div class="form-check"><input class="form-check-input" type="checkbox" id="issue-help-required" name="helpRequired"><label class="form-check-label" for="issue-help-required">Outside help / cost may be required</label></div>''','html.parser'))
    due.parent.insert_after(block)
save('issues.html',s)

# settings nav update only, billing title not needed
s=soup('settings.html'); nav_update(s); save('settings.html',s)
