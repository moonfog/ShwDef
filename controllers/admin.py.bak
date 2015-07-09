# coding: utf8
# try something like
def index(): return dict(message="hello from admin.py")

def new_category():

    form = SQLFORM(db.category)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_category(): 

    form = SQLFORM.grid(db.category)
    return dict(form=form)
    
def new_value():

    form = SQLFORM(db.value)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)


    
def overview_value(): 

    form = SQLFORM.grid(db.value)
    return dict(form=form)
    
def new_guest():

    form = SQLFORM(db.guest)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

def overview_guest(): 

    form = SQLFORM.smartgrid(db.guest)
    return dict(form=form)
    
def new_condition():

    form = SQLFORM(db.condition)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

def overview_condition(): 

    form = SQLFORM.smartgrid(db.condition_guest)
    return dict(form=form)
    
    
def new_contact():

    form = SQLFORM(db.contact)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_contact(): 

    form = SQLFORM.smartgrid(db.contact)
    return dict(form=form)
    
def new_contact_part():

    form = SQLFORM(db.contact_part)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_contact_part(): 

    form = SQLFORM.smartgrid(db.contact_part)
    return dict(form=form)
    
    
def new_reaction_user():

    form = SQLFORM(db.reaction_user)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_reaction_user(): 

    form = SQLFORM.smartgrid(db.reaction_user)
    return dict(form=form)
    

def new_contact_part_tag():

    form = SQLFORM(db.contact_part_tag)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_contact_part_tag(): 

    form = SQLFORM.smartgrid(db.contact_part_tag)
    return dict(form=form)  
    
    
def new_signal_user():

    form = SQLFORM(db.signal_user)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_signal_user(): 

    form = SQLFORM.smartgrid(db.signal_user)
    return dict(form=form)
    
def new_signal_user_tag():

    form = SQLFORM(db.signal_user_tag)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_signal_user_tag(): 

    form = SQLFORM.smartgrid(db.signal_user_tag)
    return dict(form=form)
    
    
def new_country():

    form = SQLFORM(db.country)
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)
    
def overview_country(): 

    form = SQLFORM.grid(db.country)
    return dict(form=form)
    
    
def search_signal(): 

    return dict(form=crud.create(db.signal_user))
    
def search():
    form,results = dynamic_search(db.signal_user)
    return dict(form=form,results=results)
