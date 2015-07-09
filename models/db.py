import datetime

lang1='du'
lang2='fr'
lang3=None

if(session._language==None):
    session._language=lang1

if(session._language!=lang1 and session._language!=lang2 and session._language!=lang3):
    session._language=lang1

if request.vars._language: session._language=request.vars._language

T.force(session._language)


#db = DAL('sqlite://storage.sqlite')
db =SQLDB('mysql://shw:d6p6f66nd@mysql.server/shw$registratie',fake_migrate_all=True)
##db =SQLDB('mysql://root:@localhost/erd3')
##db = SQLDB('mysql://root:str6nz66@localhost/shwreg',fake_migrate_all=True)
#db = SQLDB('mysql://web2py:w2padmin@localhost:3306/straathoekwerk',fake_migrate_all=True)

response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()


## create all tables needed by auth if not custom tables
auth.settings.table_user_name = 'user'
auth.settings.table_group_name = 'group_role'
auth.settings.table_membership_name = 'group_membership'
auth.settings.table_permission_name = 'permission'
auth.define_tables()


## configure auth policy
auth.settings.actions_disabled.append('register')
auth.settings.login_url = URL('user', args='login')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True



### captcha after failed login attempts
from gluon.tools import Recaptcha
ip = request.env.remote_addr
num_login_attempts = cache.ram(ip, lambda: 0) or 0

if num_login_attempts >= 3:
    #api key is for locahost - if not working, get your own
    auth.settings.login_captcha = Recaptcha(request,\
        '6LedxsASAAAAAAqffUEhN_sJ8GYHexLnF4JE3oWn',\
        '6LedxsASAAAAANjQXMAEinriIZCWuvJk-c3Rq-a2' )

def login_attempt(form):
    cache.ram.increment(ip)

auth.settings.login_onvalidation.append(login_attempt)

def login_success(form):
    cache.ram.clear(ip)

auth.settings.login_onaccept.append(login_success)
### ends captcha

response.title='Jes : Contact - Signal Tool'

def redirect_after_login(form):

    if auth.has_membership(user_id=auth.user.id,role='Straathoekwerkers'):
        redirect(URL(r=request,c='contact',f='mycal'))

    elif auth.has_membership(user_id=auth.user.id,role='Managers'):
        redirect(URL(r=request,c='management',f='user'))

    else:redirect(URL(r=request,c='management',f='value'))

auth.settings.login_onaccept.append(redirect_after_login)




guest_errors=None
guest_errors=[]


condition_guest_errors=None
condition_guest_errors=[]

signal_user_errors=None
signal_user_errors=[]

signal_user_tag_errors=None
signal_user_tag_errors=[]

contact_errors=None
contact_errors=[]

contact_part_errors=None
contact_part_errors=[]

reaction_user_errors=None
reaction_user_errors=[]

contact_part_tag_errors=None
contact_part_tag_errors=[]



db.define_table('country',
    Field('continent',notnull=True,label=T('Continent')),
    Field('country_lang1',label=T('Dutch')),
    Field('country_lang2',label=T('French')),
    Field('country_lang3',label=T('Optional')))

if(session._language==lang1) :
    db.country._format='%(country_lang1)s'
if(session._language==lang2) :
    db.country._format='%(country_lang2)s'
if(session._language==lang3) :
    db.country._format='%(country_lang3)s'

db.define_table('category',
    Field('category',unique=True,notnull=True,label=T('Category')),
    format = '%(category)s ')

db.define_table('value',
    Field('cat',db.category,notnull=True,label=T('Category')),
    Field('val_lang1',label=T('Dutch')),
    Field('val_lang2',label=T('French')),
    Field('val_lang3',label=T('Optional')),
    Field('deleted','boolean',default=False,label=T('Deleted')))

db.value.cat.requires=IS_IN_DB(db,'category.id','%(category)s')



if(lang1!=None):
    db.value.val_lang1.requires = [IS_NOT_EMPTY()]

if(lang2!=None):
    db.value.val_lang2.requires = [IS_NOT_EMPTY()]

if(lang3!=None):
    db.value.val_lang3.requires = [IS_NOT_EMPTY()]


if(session._language==lang1) :
    db.value._format='%(val_lang1)s'

if(session._language==lang2) :
    db.value._format='%(val_lang2)s'

if(session._language==lang3) :
    db.value._format='%(val_lang3)s'


def getCategory(value):
    row = db(db.category.category==value).select().first()
    return row

def valueNotEmpty(value):
    if(getCategory(value)==None):
        return False
    else :
        row = db(db.value.cat == getCategory(value).id).select().first()
        if row!=None:
            return True
        else:
            return False

years=[]

def makeYears():
    i=0
    year=datetime.date.today().year
    while i<100:
        i=i+1
        years.append(year)
        year=year-1


makeYears()


db.define_table('guest',
    Field('name',notnull=True,label=T('Name')),
    Field('sex',db.value,notnull=True,label=T('Sex')),
    Field('birth_year','integer',notnull=True,label=T('Birth year')),
    Field('origin',db.country,notnull=True,label=T('Origin')),
    Field('nationality',db.country,notnull=True,label=T('Nationality')),
    Field('education',db.value,notnull=True,label=T('Education')),
    Field('registration_date','date',notnull=True,default=request.now,label=T('Registered on'),requires=IS_DATE(format=T('%d-%m-%Y'))),
    Field('user',db.user,notnull=True,label=T('Registered by')),
    Field('age',compute=lambda r: (datetime.datetime.now().year) - int(r['birth_year']),label=T('Age')),
    format = '%(name)s')

db.guest.birth_year.requires=IS_IN_SET(years,zero=T('choose one'),
         error_message=T('choose a year from the list !'))


if(auth.user!=None):
    guests_User = db(db.guest.user==auth.user.id)
    db.guest.name.requires=IS_NOT_IN_DB(guests_User, 'guest.name')

def createDropDownListsGuests():

    if(getCategory('guest.sex')!=None and valueNotEmpty('guest.sex')):
        query = ((db.value.cat == getCategory("guest.sex").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.guest.sex.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.guest.sex.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.guest.sex.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='guest.sex'
        guest_errors.append(element)

    if(getCategory('guest.education')!=None and valueNotEmpty('guest.education')):
        query = ((db.value.cat == getCategory("guest.education").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.guest.education.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.guest.education.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.guest.education.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='guest.education'
        guest_errors.append(element)

    if(session._language==lang1) :
        db.guest.origin.requires=IS_IN_DB(db,'country.id','%(country_lang1)s')
        db.guest.nationality.requires=IS_IN_DB(db,'country.id','%(country_lang1)s')
    if(session._language==lang2) :
        db.guest.origin.requires=IS_IN_DB(db,'country.id','%(country_lang2)s')
        db.guest.nationality.requires=IS_IN_DB(db,'country.id','%(country_lang2)s')
    if(session._language==lang3) :
        db.guest.origin.requires=IS_IN_DB(db,'country.id','%(country_lang3)s')
        db.guest.nationality.requires=IS_IN_DB(db,'country.id','%(country_lang3)s')


createDropDownListsGuests()






db.define_table('contact',
    Field('guest',db.guest,notnull=True,label=T('Guest')),
    Field('neighbourhood',db.value,notnull=True,label=T('Neighbourhood')),
    Field('date','date',default=request.now,notnull=True,label=T('Date'),requires=IS_DATE(format=T('%d-%m-%Y'))),
    Field('created_by', default=auth.user_id,label=T('Created by'),writable=False,readable=False),
	Field('simple_contact','boolean',default=False,label=T('Simple Contact')),
    format = '%(date)s : %(guest)s')

def createDropDownListContacts():

    if(getCategory('contact.neighbourhood')!=None and valueNotEmpty('contact.neighbourhood')):
            query = ((db.value.cat == getCategory("contact.neighbourhood").id) & (db.value.deleted==False))
            if(session._language==lang1) : db.contact.neighbourhood.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
            if(session._language==lang2) : db.contact.neighbourhood.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
            if(session._language==lang3) : db.contact.neighbourhood.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='contact_neighbourhood'
        contact_errors.append(element)

createDropDownListContacts()

def default_date():
    if(db(db.contact).count()>0):
        contact_row=db(db.contact.id==session.contactID).select().first()
        if(contact_row!=None):
            contact_date=contact_row.date
            return contact_date
        else:
            return request.now
    else:
        return request.now


db.define_table('condition_guest',
    Field('guest',db.guest,notnull=True,label=T('Guest')),
    Field('date','date',notnull=True,default=default_date(),label=T('Date'),requires=IS_DATE(format=T('%d-%m-%Y'))),
    Field('financial',db.value,notnull=True,label=T('Financial situation')),
    Field('family',db.value,notnull=True,label=T('Family situation')),
    Field('gainings',db.value,notnull=True,label=T('Gainings')),
    Field('physical',db.value,notnull=True,label=T('Physical')),
    Field('mental',db.value,notnull=True,label=T('Mental')),
    Field('residence',db.value,notnull=True,label=T('Residence')),
    Field('housing',db.value,notnull=True,label=T('Housing')),
    Field('justice',db.value,notnull=True,label=T('Justice')),
    Field('drug',db.value,notnull=True,label=T('Drugs/Alcohol')),
    Field('current_study',db.value,notnull=True,label=T('Current study')),
    format = '%(date)s ')

class GuestAge():
    def age(self):
        year = datetime.datetime.now().year
        if self.guest.birth_year is not None :
         birthyear = self.guest.birth_year
         age = year - birthyear
        else : age = 0
        return (age)


db.guest.virtualfields.append(GuestAge())


def createDropDownListsCondition():

    if(getCategory('condition_guest.financial')!=None and valueNotEmpty('condition_guest.financial')):
        query = ((db.value.cat == getCategory("condition_guest.financial").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.financial.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.financial.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.financial.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.financial'
        condition_guest_errors.append(element)

    if(getCategory('condition_guest.family')!=None and valueNotEmpty('condition_guest.family')):
        query = ((db.value.cat == getCategory("condition_guest.family").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.family.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.family.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.family.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.family'
        condition_guest_errors.append(element)

    if(getCategory('condition_guest.gainings')!=None and (valueNotEmpty('condition_guest.gainings'))) :
        query = ((db.value.cat == getCategory("condition_guest.gainings").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.gainings.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.gainings.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.gainings.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.gainings'
        condition_guest_errors.append(element)

    if(getCategory('condition_guest.physical')!=None and valueNotEmpty('condition_guest.physical')):
        query = ((db.value.cat == getCategory("condition_guest.physical").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.physical.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.physical.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.physical.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.physical'
        condition_guest_errors.append(element)

    if(getCategory('condition_guest.mental')!=None and valueNotEmpty('condition_guest.mental')):
        query = ((db.value.cat == getCategory("condition_guest.mental").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.mental.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.mental.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.mental.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.mental'
        condition_guest_errors.append(element)

    if(getCategory('condition_guest.residence')!=None and valueNotEmpty('condition_guest.residence')):
        query = ((db.value.cat == getCategory("condition_guest.residence").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.residence.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.residence.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.residence.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.residence'
        condition_guest_errors.append(element)

    if(getCategory('condition_guest.housing')!=None and valueNotEmpty('condition_guest.housing')):
        query = ((db.value.cat == getCategory("condition_guest.housing").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.housing.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.housing.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.housing.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.housing'
        condition_guest_errors.append(element)


    if(getCategory('condition_guest.justice')!=None and valueNotEmpty('condition_guest.justice')):
        query = ((db.value.cat == getCategory("condition_guest.justice").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.justice.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.justice.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.justice.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.justice'
        condition_guest_errors.append(element)


    if(getCategory('condition_guest.drug')!=None and valueNotEmpty('condition_guest.drug')):
        query = ((db.value.cat == getCategory("condition_guest.drug").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.drug.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.drug.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.drug.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.drug'
        condition_guest_errors.append(element)

    if(getCategory('condition_guest.current_study')!=None and valueNotEmpty('condition_guest.current_study')):
        query = ((db.value.cat == getCategory("condition_guest.current_study").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.condition_guest.current_study.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.condition_guest.current_study.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.condition_guest.current_study.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='condition_guest.current_study'
        condition_guest_errors.append(element)



createDropDownListsCondition()

db.define_table('contact_part',
    Field('contact',db.contact,notnull=True,label=T('Contact')),
    Field('subject',db.value,notnull=True,label=T('Contact part subject')),
    Field('story','text',notnull=True,label=T('Contact part Story')),
    Field('indirect','boolean',default=False,label=T('Indirect contact')),
    format = '%(contact)s')

def createDropDownListContact_Parts():

    if(getCategory('subject')!=None and valueNotEmpty('subject')):
        query = ((db.value.cat == getCategory("subject").id) & (db.value.deleted==False))
        if(session._language==lang1) : db.contact_part.subject.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
        if(session._language==lang2) : db.contact_part.subject.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
        if(session._language==lang3) : db.contact_part.subject.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

    else:
        element='contact_part.subject'
        contact_part_errors.append(element)

createDropDownListContact_Parts()


db.define_table('contact_part_tag',
    Field('contact_part',db.contact_part,notnull=True),
    Field('tag',db.value,notnull=True,label=T('Tag')),
    format = '%(tag)s')

def createDropDownListContact_Part_Tags():

        if(getCategory('tag')!=None and valueNotEmpty('tag')):
            query = ((db.value.cat == getCategory("tag").id) & (db.value.deleted==False))
            if(session._language==lang1) : db.contact_part_tag.tag.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
            if(session._language==lang2) : db.contact_part_tag.tag.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
            if(session._language==lang3) : db.contact_part_tag.tag.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

        else:
            element='contact_part_tag.tag'
            contact_part_tag_errors.append(element)

createDropDownListContact_Part_Tags()



db.define_table('reaction_user',
    Field('contact_part',db.contact_part,notnull=True,unique=True),
    Field('type',db.value,notnull=True,label=T('Reaction type')),
    Field('content',db.value,label=T('Value')),
    Field('description','text',label=T('Description reaction (optional)')))


def createDropDownListReactions():

        if(getCategory('reaction_user.type')!=None and valueNotEmpty('reaction_user.type')):
            query = ((db.value.cat == getCategory("reaction_user.type").id) & (db.value.deleted==False))
            if(session._language==lang1) : db.reaction_user.type.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
            if(session._language==lang2) : db.reaction_user.type.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
            if(session._language==lang3) : db.reaction_user.type.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

        else:
            element='reaction_user.type'
            reaction_user_errors.append(element)



createDropDownListReactions()



db.define_table('signal_user',
    Field('user',db.user,notnull=True,label=T('User')),
    Field('title',notnull=True,label=T('Title')),
    Field('subject',db.value,notnull=True,label=T('Subject')),
    Field('description','text',notnull=True,label=T('Description')),
    Field('date','date',default=request.now,notnull=True,label=T('Date'),requires=IS_DATE(format=T('%d-%m-%Y'))),
    format = '%(date)s : %(user)s')

def createDropDownListSignal_Users():

        if(getCategory('subject')!=None and valueNotEmpty('subject')):
            query = ((db.value.cat == getCategory("subject").id) & (db.value.deleted==False))
            if(session._language==lang1) : db.signal_user.subject.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
            if(session._language==lang2) : db.signal_user.subject.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
            if(session._language==lang3) : db.signal_user.subject.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

        else:
            element='signal_user.subject'
            signal_user_errors.append(element)

createDropDownListSignal_Users()


db.define_table('signal_user_tag',
    Field('signal_user',db.signal_user,notnull=True),
    Field('tag',db.value,notnull=True,label=T('Tag')),
    format = '%(tag)s')

def createDropDownListSignal_User_Tags():

        if(getCategory('tag')!=None and valueNotEmpty('tag')):
            query = ((db.value.cat == getCategory("tag").id) & (db.value.deleted==False))
            if(session._language==lang1) : db.signal_user_tag.tag.requires=IS_IN_DB(db(query),'value.id','%(val_lang1)s')
            if(session._language==lang2) : db.signal_user_tag.tag.requires=IS_IN_DB(db(query),'value.id','%(val_lang2)s')
            if(session._language==lang3) : db.signal_user_tag.tag.requires=IS_IN_DB(db(query),'value.id','%(val_lang3)s')

        else:
            element='signal_user_tag.tag'
            signal_user_tag_errors.append(element)

createDropDownListSignal_User_Tags()
