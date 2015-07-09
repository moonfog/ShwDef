#debug doet niks staat nu op check boolean simple_contact
from gluon.debug import dbg


@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def mycal():
    session.coming_from_guest_page=False
    rows=db(db.contact.created_by == auth.user.id).select()
    #dbg.set_trace()
    return dict(rows=rows)

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def new():

    if len(contact_errors)==0:

        if(session.guest_updated==1):
            response.flash = T('Guest updated, Please create a new contact')
            session.guest_updated=0

        coming_from_contact_page()

        guests = db(db.contact.created_by == auth.user.id).select()
        form = SQLFORM(db.contact,_id='form2')

        if form.process().accepted:
            session.guestID=form.vars.guest
            maximum=db.contact.id.max()
            session.contactID=db().select(maximum).first()[maximum]
            session.neighbourhoodID = form.vars.neighbourhood
            session.simplecontact = form.vars.simple_contact
            #hier debugpoint zetten
            #dbg.set_trace()
            session_contact_inserted=1
            #redirect(URL(r=request,c='condition_guest',f='new'))
            #hier aanpassen om boolean te doen kloppen met tinyint van mysql
            if session.simplecontact==True:
              redirect(URL(r=request,f='mycal'))
            else:
			  redirect(URL(r=request,c='condition_guest',f='new'))
            # redirect werkt niet meer ??? gaat altijd door naar conditio

        elif form.errors:
            response.flash = T('form has errors')
        else:
            response.flash = T('Please create a new contact')

        return dict(form=form)

    else:
        session.type_error='contact'
        redirect(URL(r=request,c='error',f='category_value'))

def guest_selector():
    if not request.vars.zoek:
        return ''
    pattern = request.vars.zoek.capitalize() + '%'
    selected = [row.name for row in db((db.guest.name.like(pattern)) & (db.guest.user==auth.user.id )).select()]

    return ''.join([DIV(k,
                _onclick="jQuery('#zoek').val('%s'),jQuery('#gast_naam').val('%s'),jQuery('#gast_geslacht').val('%s'),jQuery('#gast_geboorteDatum').val('%s'),jQuery('#gast_afkomst').val('%s'),\
                jQuery('#gast_nationaliteit').val('%s'),jQuery('#gast_opleidingsNiveau').val('%s'),jQuery('#gast_registration_date').val('%s'),\
                jQuery('#contact_guest').val('%s'),jQuery('#test').val('%s'),\
                jQuery('#suggestions').hide()"
                % (getGuest(k).name,getGuest(k).name,getSex(k),getGuest(k).birth_year,getOrigine(k),getNationality(k),getEducation(k),getGuest(k).registration_date,getGuest(k).id,getGuest(k).name),
                _onmouseover="this.style.backgroundColor='yellow'",
                _onmouseout="this.style.backgroundColor='white'"
                 ).xml() for k in selected])

def getGuest(name):
    row=db((db.guest.name==name) &(db.guest.user==auth.user.id) ).select().first()
    return row


def getOrigine(name):
    guest=getGuest(name)
    origin_id=guest.origin
    origin=''
    if(session._language==lang1):
        origin=db.country[origin_id].country_lang1

    if(session._language==lang2):
        origin=db.country[origin_id].country_lang2

    if(session._language==lang3):
        origin=db.country[origin_id].country_lang3

    return origin

def getNationality(name):
    guest=getGuest(name)
    nationality_id=guest.nationality
    nationality=''
    if(session._language==lang1):
        nationality=db.country[nationality_id].country_lang1

    if(session._language==lang2):
        nationality=db.country[nationality_id].country_lang2

    if(session._language==lang3):
        nationality=db.country[nationality_id].country_lang3

    return nationality

def getEducation(name):

    guest=getGuest(name)
    education_id=guest.education
    educationy=''
    if(session._language==lang1):
        education=db.value[education_id].val_lang1

    if(session._language==lang2):
        education=db.value[education_id].val_lang2

    if(session._language==lang3):
        education=db.value[education_id].val_lang3

    return education

def getSex(name):

    guest=getGuest(name)
    sex_id=guest.sex
    sex=''
    if(session._language==lang1):
        sex=db.value[sex_id].val_lang1

    if(session._language==lang2):
        sex=db.value[sex_id].val_lang2

    if(session._language==lang3):
        sex=db.value[sex_id].val_lang3

    return sex




@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def new_guest_contact():

    form = SQLFORM.factory(db.contact,db.guest,_id='form1',fields=['date','neighbourhood','name','sex','birth_year','origin','nationality','education'],hidden=dict(user=auth.user.id),
    labels={'date':T('Contact date'),'neighbourhood':T('Contact neighbourhood'),'name':T('Guest name'),'sex':T('Guest sex'),'birth_year':T('Guest birth year'),'origin':T('Guest origin'),
    'nationality':T('Guest nationality'),'education':T('Guest education')})
    form.vars.user=auth.user.id

    form[0][-1][1].append(TAG.INPUT(_value='Cancel',_type="button",_onclick="window.location='%s';"%URL(r=request,f='new')))

    if form.process().accepted:

        id = db.guest.insert(**db.guest._filter_fields(form.vars))
        form.vars.guest=id
        id = db.contact.insert(**db.contact._filter_fields(form.vars))
        response.flash = 'new guest inserted'
        laatste_gast=db.guest.id.max()
        session.guestID=db().select(laatste_gast).first()[laatste_gast]
        laatste_contact=db.contact.id.max()
        session.contactID=db().select(laatste_contact).first()[laatste_contact]
        session_contact_inserted=1
        redirect(URL(r=request,c='condition_guest',f='new'))
    elif form.errors:
       response.flash = T('form has errors')
    else:
       response.flash = T('Create new guest and contact')

    return dict(form=form)


@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def overview():

    if len(contact_errors)==0:

        coming_from_contact_page()

        if len(request.args)!= 0:
            session.guestID = request.args[0]

        if(session.contact_deleted==1):
            response.flash = T('Contact deleted  !')
            session.contact_deleted=0
        count = count_simple_contacts()
        #probeer enkel de echte contacten te tonen , niet de simpele
        contacts = ((db.contact.guest == session.guestID) & (db.contact.simple_contact ==False))
        fields = [db.contact.guest,db.contact.date,db.contact.neighbourhood]
        form = SQLFORM.grid(contacts,fields=fields,user_signature=False,deletable=False,editable=False,details=False,paginate=10,create=False,csv=False,orderby=[~db.contact.date],
        links = [lambda row:A('Edit',_href=URL("contact","edit",args=[row.id])),
                 lambda row:A('Delete',_href=URL("contact","delete_contact_and_condition_guest",args=[row.id])),
                 lambda row:A('Contact parts',_href=URL("contact_part","overview",args=[row.id]))])
        return dict(form=form,count_simplecontacts=count)

    else:
        session.type_error='contact'
        redirect(URL(r=request,c='error',f='category_value'))




@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def update():

    record = db(db.contact.id==session.contactID).select().first()
    form = SQLFORM(db.contact,record,_id='form2',showid = False,submit_button = 'Update')
    form.element(_id='contact_guest')['_onfocus']="this.blur()"
    if form.process().accepted:
        redirect(URL(r=request,c='contact_part',f='new'))

    elif form.errors:
        response.flash = T('form has errors')


    return dict(form=form)


@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def edit():

    if len(contact_errors)==0:

        if len(request.args)!= 0:
            session.contactID = request.args[0]

        record = db(db.contact.id==session.contactID).select().first()
        session.old_date=record.date
        fields=['date','neighbourhood']
        form = SQLFORM(db.contact,record,fields=fields,showid = False,submit_button = 'Update')
        guest_record=db(db.guest.id==record.guest).select().first()
        name=guest_record.name


        if form.process().accepted:
            update_condition_guest()
            session.contact_updated=1
            redirect(URL(r=request,c='contact_part',f='overview'))

        elif form.errors:
            response.flash = T('form has errors')

        else:
            response.flash = T('Please update this contact')

        return dict(form=form,name=name)

    else:
        session.type_error='contact'
        redirect(URL(r=request,c='error',f='category_value'))

def update_condition_guest():

    old_date=session.old_date
    contact=db(db.contact.id==session.contactID).select().first()
    guestID=contact.guest
    new_date=contact.date
    session.new_date=new_date
    condition_rows=db((db.condition_guest.guest==guestID) & (db.condition_guest.date==old_date)).select()
    session.condition_rows=condition_rows

    condition_row=None

    if(len(condition_rows)!=0):
        cg_id=0
        for row in condition_rows:
            if(row.id>cg_id):cg_id=row.id

        condition_row=db(db.condition_guest.id==cg_id).select().first()
        condition_row.update_record(date=new_date)

def delete_contact_and_condition_guest():

    if len(request.args)!= 0:
        session.contactID = request.args[0]

    contact=db(db.contact.id==session.contactID).select().first()
    condition_rows=db((db.condition_guest.guest==session.guestID) & (db.condition_guest.date==contact.date)).select()

    if(len(condition_rows)!=0):
        db((db.condition_guest.guest==session.guestID) & (db.condition_guest.date==contact.date)).delete()

    db(db.contact.id==session.contactID).delete()
    session.contact_deleted=1

    redirect(URL(r=request,f='overview'))

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def update_guest():
    if (request.vars.naam):
        session.guest_update=request.vars.naam

    record = db(db.guest.name==session.guest_update).select().first()
    form = SQLFORM(db.guest,record,fields=['name','sex','birth_year','origin','nationality','education'],hidden=dict(shw=auth.user.id),showid = False,submit_button = 'Update')

    form[0][-1][1].append(TAG.INPUT(_value=T('Cancel'),_type="button",_onclick="window.location='%s';"%URL(r=request,f='new')))

    if form.process().accepted:
        session.guest_updated=1
        redirect(URL(r=request,f='new'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('Please update your guest')

    return dict(form=form)

def coming_from_contact_page():
    session.coming_from_guest_page=False

def count_simple_contacts():
	count_simplecontacts = db((db.contact.simple_contact=='T') & (db.contact.guest==session.guestID)).count()
	return count_simplecontacts
