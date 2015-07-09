# coding: utf8
# try something like
import datetime

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def new():

    if len(condition_guest_errors)==0: 
    
        if(session.contact_inserted==1):
            response.flash=T('Contact created')
            session.contact_inserted=0
        
            
        condition_row=get_latest_condition_from_guest()
        date=None
        
        if(condition_row!=None):
        
            contact_row=db(db.contact.id==session.contactID).select().first()
            date=contact_row.date
            guest_row=db.guest[session.guestID]
                        
            form1=FORM(TABLE(TBODY(
                    TR(TD(LABEL(T('Guest :')),_class="w2p_f1"),TD(INPUT(_name='guest',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Condition date :')),_class="w2p_f1"),TD(INPUT(_name='date',_readonly='readonly',_type='text')))))) 
                    
            form1.vars.guest=guest_row.name
            form1.vars.date=date.strftime('%d-%m-%Y')
            form1.validate()  
            
            fields=['financial','family','gainings','physical','mental','residence','housing','justice','drug','current_study']
            form2 = SQLFORM(db.condition_guest,fields=fields,hidden=dict(guest = session.guestID,date=date))
            form2.vars.guest = session.guestID
            form2.vars.date = date
            form2.vars.financial = condition_row.financial
            form2.vars.family = condition_row.family
            form2.vars.gainings = condition_row.gainings
            form2.vars.physical = condition_row.physical
            form2.vars.mental = condition_row.mental
            form2.vars.drug = condition_row.drug
            form2.vars.residence = condition_row.residence
            form2.vars.housing = condition_row.housing
            form2.vars.drug = condition_row.drug
            form2.vars.justice = condition_row.justice
            form2.vars.current_study = condition_row.current_study               

            form2[0][-1][1].append(TAG.INPUT(_value=T('Cancel'),_type="button",_onclick="window.location='%s';"%URL(r=request,c='contact_part',f='new')))

            if form2.process().accepted:
                session.condition_inserted=1
                redirect(URL(r=request,c='contact_part',f='new'))
            elif form2.errors:
                response.flash = T('form has errors')
            else:
                response.flash = T('Create new condition guest')

            return dict(form1=form1,form2=form2)

        else:redirect(URL(r=request,c='condition_guest',f='first'))
        
    else:
        session.type_error='condition_guest'
        redirect(URL(r=request,c='error',f='category_value'))


@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def first():

    if len(condition_guest_errors)==0:
    
        contact_row=db(db.contact.id==session.contactID).select().first()
        date=contact_row.date
        
        guest_row=db.guest[session.guestID]
                        
        form1=FORM(TABLE(TBODY(
                    TR(TD(LABEL('Guest :'),_class="w2p_f1"),TD(INPUT(_name='guest',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL('Condition date :'),_class="w2p_f1"),TD(INPUT(_name='date',_readonly='readonly',_type='text')))))) 
                    
        form1.vars.guest=guest_row.name
        form1.vars.date=(date).strftime('%d-%m-%Y') 
        form1.validate()  
        
        fields=['financial','family','gainings','physical','mental','residence','housing','justice','drug','current_study']
        form2 = SQLFORM(db.condition_guest,fields=fields,hidden=dict(guest = session.guestID,date=date))
        form2.vars.guest = session.guestID
        
        guest_row = db(db.guest.id == session.guestID).select().first()
        guest_name=guest_row.name
        
        if form2.process().accepted:
            session.condition_inserted=1
            redirect(URL(r=request,c='contact_part',f='new'))
        elif form2.errors:
            response.flash = T('form has errors')
        else:
            response.flash = T('Create new condition guest')

        return dict(form1=form1,form2=form2)
    
    else:
        session.type_error='condition_guest'
        redirect(URL(r=request,c='error',f='category_value'))

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def overview():

    if len(condition_guest_errors)==0:

        if len(request.args)!=0:
            session.guestID = request.args[0]
            
        guest_row=db(db.guest.id==session.guestID).select().first()
        name=guest_row.name
        
        fields=[db.condition_guest.date,db.condition_guest.financial,db.condition_guest.family,db.condition_guest.gainings,db.condition_guest.physical,db.condition_guest.mental,db.condition_guest.residence,db.condition_guest.housing,db.condition_guest.justice,db.condition_guest.drug,db.condition_guest.current_study]
        
        headers={'condition_guest.family':'family','condition_guest.financial':'financial'}
        
        form = SQLFORM.grid(query_all(),searchable=False,deletable=False,editable=False,sortable=True,orderby=[~db.condition_guest.date,~db.condition_guest.id],
                details=False,csv=False,create=False,fields=fields,headers=headers)
        
       
        return dict(form=form,name=name)
    
    else:
        session.type_error='condition_guest'
        redirect(URL(r=request,c='error',f='category_value'))
    
@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def details():

    if len(condition_guest_errors)==0:
    
        if(session.condition_guest_updated==1):
            response.flash = T('Condition guest updated !')
            session.condition_guest_updated=0
    
        if len(request.args)!=0:
            session.guestID = request.args[0]
            condition_row=get_latest_condition_from_guest()
            
            
        else:
            if(session.coming_from_guest_page):
                    condition_row=get_latest_condition_from_guest()
            else:
                condition_row=get_condition_from_contact()
            
            
        date=None
        
        guest_row=db(db.guest.id==session.guestID).select().first()
        
        
        if(condition_row!=None):
        
            date=(condition_row.date).strftime('%d-%m-%Y')
            financial_row=db(db.value.id==condition_row.financial).select().first()
            family_row=db(db.value.id==condition_row.family).select().first()
            gainings_row=db(db.value.id==condition_row.gainings).select().first()
            physical_row=db(db.value.id==condition_row.physical).select().first()
            mental_row=db(db.value.id==condition_row.mental).select().first()
            residence_row=db(db.value.id==condition_row.residence).select().first()
            housing_row=db(db.value.id==condition_row.housing).select().first()
            drugs_row=db(db.value.id==condition_row.drug).select().first()
            justice_row=db(db.value.id==condition_row.justice).select().first()
            current_study_row=db(db.value.id==condition_row.current_study).select().first()
        
            financial=''
            family=''
            gainings=''
            physical=''
            mental=''
            residence=''
            housing=''
            drugs=''
            justice=''
            current_study=''
    
    
            if(session._language==lang1):
                financial=financial_row.val_lang1
                family=family_row.val_lang1
                gainings=gainings_row.val_lang1
                physical=physical_row.val_lang1
                mental=mental_row.val_lang1
                residence=residence_row.val_lang1
                housing=housing_row.val_lang1
                drugs=drugs_row.val_lang1
                justice=justice_row.val_lang1
                current_study=current_study_row.val_lang1
            
            if(session._language==lang2):
                financial=financial_row.val_lang2
                family=family_row.val_lang2
                gainings=gainings_row.val_lang2
                physical=physical_row.val_lang2
                mental=mental_row.val_lang2
                residence=residence_row.val_lang2
                housing=housing_row.val_lang2
                drugs=drugs_row.val_lang2
                justice=justice_row.val_lang2
                current_study=current_study_row.val_lang2
            
            if(session._language==lang3):
                financial=financial_row.val_lang3
                family=family_row.val_lang3
                gainings=gainings_row.val_lang3
                physical=physical_row.val_lang3
                mental=mental_row.val_lang3
                residence=residence_row.val_lang3
                housing=housing_row.val_lang3
                drugs=drugs_row.val_lang3
                justice=justice_row.val_lang3
                current_study=current_study_row.val_lang3
                
            form1=FORM(TABLE(TBODY(
                    TR(TD(LABEL(T('Guest :')),_class="w2p_f1"),TD(INPUT(_name='guest',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Condition date :')),_class="w2p_f1"),TD(INPUT(_name='date',_readonly='readonly',_type='text'))))))   
            form1.vars.guest=guest_row.name
            form1.vars.date=date
            form1.validate()                  
   
            
            form2=FORM(TABLE(TBODY(
                    TR(TD(LABEL(T('Financial :')),_class="w2p_f1"),TD(INPUT(_name='condition_financial',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Family :')),_class="w2p_f1"),TD(INPUT(_name='condition_family',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Gainings :')),_class="w2p_f1"),TD(INPUT(_name='condition_gainings',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Physical :')),_class="w2p_f1"),TD(INPUT(_name='condition_physical',_readonly='readonly',_type='text'))),                    
                    TR(TD(LABEL(T('Mental :')),_class="w2p_f1"),TD(INPUT(_name='condition_mental',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Residence :')),_class="w2p_f1"),TD(INPUT(_name='condition_residence',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Housing :')),_class="w2p_f1"),TD(INPUT(_name='condition_housing',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Justice :')),_class="w2p_f1"),TD(INPUT(_name='condition_justice',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Drugs :')),_class="w2p_f1"),TD(INPUT(_name='condition_drugs',_readonly='readonly',_type='text'))),                    
                    TR(TD(LABEL(T('Current study :')),_class="w2p_f1"),TD(INPUT(_name='condition_current_study',_readonly='readonly',_type='text'),_class="w2p_fw")))),_id='form1')   
        
            
            form2.vars.condition_financial=financial
            form2.vars.condition_family=family
            form2.vars.condition_gainings=gainings
            form2.vars.condition_physical=physical
            form2.vars.condition_mental=mental
            form2.vars.condition_residence=residence
            form2.vars.condition_housing=housing
            form2.vars.condition_justice=justice
            form2.vars.condition_drugs=drugs
            form2.vars.condition_current_study=current_study
            
            if (session.coming_from_guest_page):
                 my_extra_element1 = TR(TD(_class="w2p_fl"),TD(INPUT(_type="button",_value=T('History'),_onclick="window.location='%s';"%URL(r=request,f='overview')),
                 INPUT(_type="button",_value=T('Guest'),_onclick="window.location='%s';"%URL(r=request,c='guest',f='details')),_class="w2p_fw"))
            else:
                my_extra_element1 = TR(TD(_class="w2p_fl"),TD(INPUT(_type="button",_value=T('Edit'),_onclick="window.location='%s';"%URL(r=request,f='edit')),INPUT(_type="button",_value="History",_onclick="window.location='%s';"%URL(r=request,f='overview')),
                INPUT(_type="button",_value=T('Guest'),_onclick="window.location='%s';"%URL(r=request,c='guest',f='details')),_class="w2p_fw"))
            
            form2[0][0][-1].append(my_extra_element1)
            
            form2.validate()        
           
            return dict(form1=form1,form2=form2)
    
        else:       
        
            redirect(URL(r=request,f='no_condition'))
        
    else:
        session.type_error='condition_guest'
        redirect(URL(r=request,c='error',f='category_value'))

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def edit():

    if len(condition_guest_errors)==0:
    
        if len(request.args)!=0:
            session.guestID = request.args[0]        
             
        condition_row=get_condition_from_contact()
        guest_row=db(db.guest.id==session.guestID).select().first()
    
        
        if(condition_row!=None):
        
            date=condition_row.date
            form1=FORM(TABLE(TBODY(
                    TR(TD(LABEL(T('Guest :')),_class="w2p_f1"),TD(INPUT(_name='guest',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Condition date :')),_class="w2p_f1"),TD(INPUT(_name='date',_readonly='readonly',_type='text'))))))   
            form1.vars.guest=guest_row.name
            form1.vars.date=date.strftime('%d-%m-%Y')
            form1.validate()  
        
            
            fields=['financial','family','gainings','physical','mental','residence','housing','justice','drug','current_study']
            form2 = SQLFORM(db.condition_guest,condition_row,fields=fields,showid = False,submit_button = 'Update',hidden=dict(guest = session.guestID,date=date))
            session.edit_condition_date=date
            form2.vars.guest = session.guestID
                        
            guest_row = db(db.guest.id == session.guestID).select().first()
            
            guest_name=(guest_row.name)
            
            
            if form2.process().accepted:   
                session.condition_guest_updated=1
                redirect(URL(r=request,f='details')) 
                
            elif form2.errors:
                response.flash = T('form has errors')
            else:
                response.flash = T('Please, update condition guest')
   
            return dict(form1=form1,form2=form2)
    
    else:
        session.type_error='condition_guest'
        redirect(URL(r=request,c='error',f='category_value'))

##Geef de meest recente conditie van een aantal condities !!!      
def get_latest(condition_rows):

    condition_row=None
    
    if(len(condition_rows)!=0): 
        cg_date=datetime.date(2010,11,11)
        cg_id=0
        for row in condition_rows:
            if(row.date>=cg_date):
                cg_id=row.id
                cg_date=row.date
                
        condition_row=db(db.condition_guest.id==cg_id).select().first()
    
    return condition_row

##Komende van overzicht guests of bij aanmaak nieuw contact >> is de meest recente conditie van de guest  !!!!
def get_latest_condition_from_guest():
        condition_rows=db(db.condition_guest.guest==session.guestID).select()        
        return get_latest(condition_rows)
        
##komende van contact_parts overzicht >> is de laatste conditie van de guest op de datum van het contact !!!    
def get_condition_from_contact():
        contact=db(db.contact.id==session.contactID).select().first()
        guestID=contact.guest
        date=contact.date
        condition_rows=db((db.condition_guest.guest==guestID) & (db.condition_guest.date==date)).select()        
        return get_latest(condition_rows)

    
def no_condition():
    message=None
    return dict(message=message)

def get_all():
    condition_rows = db(query_all()).select()
    return condition_rows
    
def query_all():
    query = db.condition_guest.guest==session.guestID
    return query
