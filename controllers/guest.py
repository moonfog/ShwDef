# coding: utf8
# try something like
import datetime


@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def overview():

    if len(guest_errors)==0:
    
        coming_from_guest_page()  
        
        if(session.guest_inserted==1):
            response.flash=T('New guest created !')
            
        session.guest_inserted=0
        
        
        fields=[db.guest.name,db.guest.sex,db.guest.birth_year,db.guest.registration_date,db.guest.origin,db.guest.nationality] 
                
        grid = SQLFORM.grid(db.guest.user==auth.user.id,fields=fields,deletable=False,editable=False,details=False,paginate=10,create=False,csv=False,orderby=[~db.guest.id],
        links = [lambda row:A(T('Details'),_href=URL("guest","details",args=[row.id])),
				 lambda row:A(T('Edit'),_href=URL("guest","edit",args=[row.id])), 
                 lambda row:A(T('Condition'),_href=URL("condition_guest","details",args=[row.id])), 
                 lambda row:A(T('Contacts'),_href=URL("contact","overview",args=[row.id]))])
        
       
        return dict(form=grid)
        
    else:
        session.type_error='guest'
        redirect(URL(r=request,c='error',f='category_value'))
        
        

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def details():

    if len(guest_errors)==0:
    
        coming_from_guest_page()

        if len(request.args)!=0:
            session.guestID = request.args[0]
    
        guestId = session.guestID
        guest_row = db(db.guest.id == guestId).select().first()
        country_row=db(db.country.id==guest_row.nationality).select().first()
        origin_row=db(db.country.id==guest_row.origin).select().first()
        sex_row=db(db.value.id==guest_row.sex).select().first()
        education_row=db(db.value.id==guest_row.education).select().first()
    
    
        country=''
        origin=''
        sex=''
        education=''
    
        if(session._language==lang1):
            country=country_row.country_lang1
            origin=origin_row.country_lang1
            sex=sex_row.val_lang1
            education=education_row.val_lang1
        
        if(session._language==lang2):
            country=country_row.country_lang2
            origin=origin_row.country_lang2
            sex=sex_row.val_lang2
            education=education_row.val_lang2
        
        if(session._language==lang3):
            country=country_row.country_lang3
            origin=origin_row.country_lang3
            sex=sex_row.val_lang3
            education=education_row.val_lang3
        
        form=FORM(TABLE(TBODY(TR(TD(LABEL(T('Name :')),_class="w2p_f1"),TD(INPUT(_name='guest_name',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Sex :')),_class="w2p_f1"),TD(INPUT(_name='guest_sex',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Age :')),_class="w2p_f1"),TD(INPUT(_name='guest_age',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Nationality :')),_class="w2p_f1"),TD(INPUT(_name='guest_country',_readonly='readonly',_type='text'))),                    
                    TR(TD(LABEL(T('Origin :')),_class="w2p_f1"),TD(INPUT(_name='guest_origin',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Education :')),_class="w2p_f1"),TD(INPUT(_name='guest_education',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Registered on :')),_class="w2p_f1"),TD(INPUT(_name='guest_registration_date',_readonly='readonly',_type='text'),_class="w2p_fw")))),_id='form1')   
       
        form.vars.guest_name=guest_row.name
        form.vars.guest_sex=sex
        form.vars.guest_age=guest_row.age
        form.vars.guest_country=country
        form.vars.guest_origin=origin
        form.vars.guest_education=education
        form.vars.guest_registration_date=(guest_row.registration_date).strftime('%d-%m-%Y')
        
        my_extra_element1 = TR(TD(_class="w2p_fl"),TD(INPUT(_type="button",_value=T('Edit'),_onclick="window.location='%s';"%URL(r=request,f='edit')),INPUT(_type="button",_value=T('Condition'),_onclick="window.location='%s';"%URL(r=request,c='condition_guest',f='details')),INPUT(_type="button",_value=T('Overview'),_onclick="window.location='%s';"%URL(r=request,f='overview')),_class="w2p_fw"))
        form[0][0][-1].append(my_extra_element1) 

        form.validate()   
         
        if(session.guest_updated==1):
            response.flash=T('Guest updated')  
            
        session.guest_updated=0

        return dict(form=form)
    
    else:
        session.type_error='guest'
        redirect(URL(r=request,c='error',f='category_value'))
        
        

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def new():
    
    if len(guest_errors)==0:
    
        form = SQLFORM(db.guest,fields=['name','sex','birth_year','origin','nationality','education'],hidden=dict(shw=auth.user.id))
        form.vars.user = auth.user.id
        form[0][-1][1].append(TAG.INPUT(_value=T('Cancel'),_type="button",_onclick="window.location='%s';"%URL(r=request,f='overview')))  
        if form.process().accepted:
            max = db.guest.id.max()
            guestId=db().select(max).first()[max]
            session.guestID=guestId
            session.guest_inserted=1
            redirect(URL(r=request,f='overview'))
        elif form.errors:
           response.flash = T('form has errors')
        
        else:
            response.flash = T('Create new guest')
       
        return dict(form=form)
        
    else:
        session.type_error='guest'
        redirect(URL(r=request,c='error',f='category_value'))
        

        
@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def edit():

    if len(guest_errors)==0:
    
        if len(request.args)!=0:
            session.guestID = request.args[0]

        record = db(db.guest.id==session.guestID).select().first()
        fields = ['name' , 'sex', 'birth_year','nationality','origin','education']
        form = SQLFORM(db.guest,record,fields=fields,showid = False,submit_button = T('Update'))
        
        if form.process().accepted:   
            session.guest_updated=1
            redirect(URL(r=request,f='details')) 
            
        elif form.errors:
            response.flash = T('form has errors')
        else:
            response.flash = T('Update Guest')
   
        return dict(form=form)
    
    else:
        session.type_error='guest'
        redirect(URL(r=request,c='error',f='category_value'))

def coming_from_guest_page():
    session.coming_from_guest_page=True
