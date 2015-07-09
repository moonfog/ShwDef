@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def new():

    if len(contact_part_errors)==0:

        if(session.condition_inserted==1):
            response.flash=T('Condition guest created, please add your contact parts !')
            session.condition_inserted=0
            
        else:
            response.flash=''

 
        form1=FORM(TABLE(TR(TD(LABEL(T('Date :')),_class="w2p_f1"),TD(INPUT(_name='contact_date',_readonly='readonly'))),
                    TR(TD(LABEL(T('Guest :')),_class="w2p_f1"),TD(INPUT(_name='guest_name',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Neighbourhood :')),_class="w2p_f1"),TD(INPUT(_name='contact_neighbourhood',_readonly='readonly')))),_id='form1')                      
   
       
        form1.vars.contact_date=(db.contact[session.contactID].date).strftime('%d-%m-%Y')
        form1.vars.guest_name=db.guest[session.guestID].name
        valueID=db.contact[session.contactID].neighbourhood
   
        if (session._language == lang1) :    
            form1.vars.contact_neighbourhood=db.value[valueID].val_lang1
        if (session._language == lang2) :
            form1.vars.contact_neighbourhood=db.value[valueID].val_lang2
        if (session._language == lang3) :
            form1.vars.contact_neighbourhood=db.value[valueID].val_lang3
    
        form1.validate()    

        query = (db.contact_part.contact==session.contactID) 
        fields = [db.contact_part.subject]
        form3 = SQLFORM.grid(query,fields = fields, ui = 'jquery-ui',user_signature=False,deletable=False,details=False,create=False,editable=False,csv=False,searchable=False,paginate=10)

  
        form2 = SQLFORM.factory(db.contact_part,db.reaction_user,_id='form2',submit_button='Insert',fields=['subject','story','indirect','type','content','description'],hidden=dict(contact=session.contactID,contactpart=session.contactpartID))
        form2.vars.contact=request.vars.contact
        form2.vars.contact_part=request.vars.contactpart

        form2[0][-1][1].append(TAG.INPUT(_value=T('Cancel'),_type="button",_onclick="window.location='%s';"%URL(r=request,f='overview')))   

        insert(form2)   

        return dict(form1=form1,form2=form2,grid=form3)
    
    else:
        session.type_error='contact_part'
        redirect(URL(r=request,c='error',f='category_value'))

    
   
@auth.requires(auth.has_membership(role='Straathoekwerkers'))    
def insert(form):

    if len(contact_part_errors)==0:
                    
        if form.process().accepted:
            id = db.contact_part.insert(**db.contact_part._filter_fields(form.vars))
            session.contactpartID = id
            form.vars.contact_part=id
            id = db.reaction_user.insert(**db.reaction_user._filter_fields(form.vars))
            form.vars.reaction_user=id
            session.contact_part_inserted=1
            redirect(URL(r=request,c='contact_part_tag',f='tag')) 
            
        elif form.errors:
           response.flash = T('form has errors')         

    else:
        session.type_error='contact_part'
        redirect(URL(r=request,c='error',f='category_value'))
    
    
    
@auth.requires(auth.has_membership(role='Straathoekwerkers')) 
def overview():

    if len(contact_part_errors)==0:
        
        ##Edit van condition guest is allowed !!!
        coming_from_contact_page()
    
        if len(request.args)!= 0:
            session.contactID = request.args[0]
            
        contact_row=db(db.contact.id==session.contactID).select().first()
        guest_row=db.guest[contact_row.guest]    
        session.guestID=guest_row.id
        nh_row=db(db.value.id==contact_row.neighbourhood).select().first()
        

        
        form1=FORM(TABLE(TR(TD(LABEL(T('Date :')),_class="w2p_f1"),TD(INPUT(_name='contact_date',_readonly='readonly'))),
                    TR(TD(LABEL(T('Guest :')),_class="w2p_f1"),TD(INPUT(_name='guest_name',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Neighbourhood :')),_class="w2p_f1"),TD(INPUT(_name='contact_neighbourhood',_readonly='readonly')))),_id='form1')                      
   
       
        form1.vars.contact_date=(contact_row.date).strftime('%d-%m-%Y')
        form1.vars.guest_name=guest_row.name
        valueID=db.contact[session.contactID].neighbourhood
   
        if (session._language == lang1) :    
            form1.vars.contact_neighbourhood=db.value[valueID].val_lang1
        if (session._language == lang2) :
            form1.vars.contact_neighbourhood=db.value[valueID].val_lang2
        if (session._language == lang3) :
            form1.vars.contact_neighbourhood=db.value[valueID].val_lang3
    
        form1.validate()
        
        button_contact=TAG.INPUT(_value=T('Edit'),_type="button",_onclick="window.location='%s';"%URL(r=request,c='contact',f='edit'))
        button_contact_part=TAG.INPUT(_value=T('Add'),_type="button",_onclick="window.location='%s';"%URL(r=request,f='new'))
        button_condition_guest=TAG.INPUT(_value=T('Details'),_type="button",_onclick="window.location='%s';"%URL(r=request,c='condition_guest',f='details'))
         
        fields = [db.contact_part.subject]
        form2 = SQLFORM.grid(db.contact_part.contact==session.contactID,fields = fields, ui = 'jquery-ui',user_signature=False,deletable=False,details=False,create=False,editable=False,csv=False,searchable=False,paginate=10,
        links=[lambda row:A(T('Details'),_href=URL("details",args=[row.id])),
               lambda row:A(T('Edit'),_href=URL("edit",args=[row.id])),
               lambda row:A(T('Delete'),_href=URL("delete",args=[row.id])),
               lambda row:A(T('Tags'),_href=URL("contact_part_tag","tag",args=[row.id]))])
               
        if(session.contact_part_inserted==1):
            response.flash=T('Contact part inserted')
            
        if(session.contact_part_deleted==1):
            response.flash=T('Contact part deleted')
            
        if(session.contact_updated==1):
            response.flash=T('Contact updated')
            
        session.contact_part_inserted=0
        session.contact_part_deleted=0
        session.contact_updated=0
        
        session.new_condition_after_new_contact=1
        
        return dict(form1=form1,form2=form2,button_contact=button_contact,button_contact_part=button_contact_part,button_condition_guest=button_condition_guest)
            
    else:
        session.type_error='contact_part'
        redirect(URL(r=request,c='error',f='category_value'))
       
def condition_exists():
    contact=db(db.contact.id==session.contactID).select().first()
    guest=contact.guest
    date=contact.date
    condition=db(db.condition_guest.date==date & db.condition_guest.guest==guest).select().first()
    if(condition!=None):
        return True
    else:
        return False
       

@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def delete():
        
    if len(request.args)!= 0:
        session.contactpartID = request.args[0]

    db(db.contact_part.id==session.contactpartID).delete()    
    session.contact_part_deleted=1    
    redirect(URL(r=request,f='overview'))
    
    
            
@auth.requires(auth.has_membership(role='Straathoekwerkers')) 
def update():
    query = (db.contact_part.contact==session.contactID)
    record = db(db.contact_part.contact==session.contactID).select().first()
    return record
    
    

@auth.requires(auth.has_membership(role='Straathoekwerkers'))     
def details():

    if len(contact_part_errors)==0:
    
        if len(request.args)!= 0:
            session.contactpartID = request.args[0]
            
        contact_row=db.contact[session.contactID]     
        guest_row=db.guest[contact_row.guest]
        contact_part_row=db.contact_part[session.contactpartID]
        reaction_user_row = db(db.reaction_user.contact_part==session.contactpartID).select().first()
    
        session.reaction_userID=reaction_user_row.id
    
        contact_partID = session.contactpartID
        contact_part_row = db(db.contact_part.id == contact_partID).select().first()
        reaction_user_row = db(db.reaction_user.contact_part==session.contactpartID).select().first()
        subject_row=db(db.value.id==contact_part_row.subject).select().first()
        reaction_type_row=db(db.value.id==reaction_user_row.type).select().first()
        reaction_content_row=db(db.value.id==reaction_user_row.content).select().first()

    
        valueID=db.contact[session.contactID].neighbourhood
    
        guest=''
        contact_date=''
        subject=''
        story=''
        indirect=''
        reaction_type=''
        reaction_content=''
        reaction_description=''
        neighbourhood=''
    
        guest=guest_row.name
        contact_date=(contact_row.date).strftime('%d-%m-%Y')
        story=contact_part_row.story
        indirect=contact_part_row.indirect
        reaction_description=reaction_user_row.description
        
        if(session._language==lang1):
            subject=subject_row.val_lang1        
            reaction_type=reaction_type_row.val_lang1
            reaction_content=reaction_content_row.val_lang1
            neighbourhood=db.value[valueID].val_lang1
        
        if(session._language==lang2):
            subject=subject_row.val_lang2        
            reaction_type=reaction_type_row.val_lang2
            reaction_content=reaction_content_row.val_lang2
            neighbourhood=db.value[valueID].val_lang2
        
        if(session._language==lang3):
            subject=subject_row.val_lang3        
            reaction_type=reaction_type_row.val_lang3
            reaction_content=reaction_content_row.val_lang3
            neighbourhood=db.value[valueID].val_lang3
        
        form=FORM(TABLE(TBODY(TR(TD(LABEL(T('Contact part subject :')),_class="w2p_f1"),TD(INPUT(_name='contact_part_subject',_readonly='readonly',_type='text'))),
            TR(TD(LABEL(T('Contact part story :')),_class="w2p_f1"),TD(TEXTAREA(_name='contact_part_story',_readonly='readonly',_type='text'))),
            TR(TD(LABEL(T('Indirect contact ?')),_class="w2p_f1"),TD(INPUT(_name='contact_part_indirect',_readonly='readonly',_type='checkbox'))),
            TR(TD(LABEL(T('Reaction type :')),_class="w2p_f1"),TD(INPUT(_name='reaction_user_type',_readonly='readonly',_type='text'))),                    
            TR(TD(LABEL(T('Value :')),_class="w2p_f1"),TD(INPUT(_name='reaction_user_content',_readonly='readonly',_type='text'))),
            TR(TD(LABEL(T('Reaction description (optional) :')),_class="w2p_f1"),TD(TEXTAREA(_name='reaction_user_description',_readonly='readonly',_type='text'),_class="w2p_fw")))),_id='form1')   
       
        form.vars.contact_part_subject=subject
        form.vars.contact_part_story=story
        form.vars.contact_part_indirect=indirect
        form.vars.reaction_user_type=reaction_type
        form.vars.reaction_user_content=reaction_content
        form.vars.reaction_user_description=reaction_description
        
        my_extra_element1 = TR(TD(_class="w2p_fl"),TD(INPUT(_type="button",_value=T('Edit'),_onclick="window.location='%s';"%URL(r=request,f='edit'))))
        form[0][0][-1].append(my_extra_element1)  

        form.validate()   
    
    
        return dict(form=form,guest=guest,contact_date=contact_date,neighbourhood=neighbourhood)
    
    else:
        session.type_error='contact_part'
        redirect(URL(r=request,c='error',f='category_value'))
    

@auth.requires(auth.has_membership(role='Straathoekwerkers')) 
def edit():

    if len(contact_part_errors)==0:
    
        if len(request.args)!= 0:
            session.contactpartID = request.args[0]
    
        contactpartID=session.contactpartID
        reaction_userID=session.reaction_userID     
        contactID=session.contactID
    
        contact_part_row = db(db.contact_part.id==session.contactpartID).select().first()
        reaction_user_row = db(db.reaction_user.contact_part==session.contactpartID).select().first()
        contact_row=db(db.contact.id==contactID).select().first()
        guest_row=db.guest[contact_row.guest]
        
        valueID=db.contact[session.contactID].neighbourhood
        neighbourhood=''
        
        if (session._language == lang1) :    
            neighbourhood=db.value[valueID].val_lang1
        if (session._language == lang2) :
            neighbourhood=db.value[valueID].val_lang2
        if (session._language == lang3) :
            neighbourhood=db.value[valueID].val_lang3
        
        guest=guest_row.name
        contact_date=contact_row.date
        
       
        fields_cp=['subject','story','indirect']
        form_cp = SQLFORM(db.contact_part,record=contact_part_row,fields=fields_cp,showid = False,submit_button = 'Update',hidden=dict(contact=contactID))
        form_cp.vars.contact=contactID
        
        form_cp[0][-1][1].append(TAG.INPUT(_value=T('Overview'),_type="button",_onclick="window.location='%s';"%URL(r=request,c='contact_part',f='overview')))
        
        fields_ru=['type','content','description']
        form_ru=SQLFORM(db.reaction_user,record=reaction_user_row,fields=fields_ru,showid = False,submit_button = 'Update',hidden=dict(contact_part=contactpartID))
        form_ru.vars.contact_part=contactpartID        
        
        form_ru[0][-1][1].append(TAG.INPUT(_value='Overview',_type="button",_onclick="window.location='%s';"%URL(r=request,c='contact_part',f='overview')))
        
        if form_cp.process().accepted:
            response.flash = T('Contact part updated') 

        elif form_cp.errors:
            response.flash = T('Form contact part has errors')
            
        else:
            response.flash = T('Update contact part and/or reaction')
            
        if form_ru.process().accepted:
            response.flash = T('Reaction user updated')

        elif form_ru.errors:
            response.flash = T('Form reaction user has errors')
                

            

        return dict(form_cp=form_cp,form_ru=form_ru,guest=guest,contact_date=contact_date,neighbourhood=neighbourhood)
   
    else:
        session.type_error='signal_user'
        redirect(URL(r=request,c='error',f='category_value'))

def coming_from_contact_page():
    session.coming_from_guest_page=False
    
def listenings():
    cat=db(db.category.category=='reaction_user.value_listening').select().first()
    listenings=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(listenings)
    

def interest_representations():
    cat=db(db.category.category=='reaction_user.value_interest_representation').select().first()
    interest_representations=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(interest_representations)
    
def mediations():
    cat=db(db.category.category=='reaction_user.value_mediation').select().first()
    mediations=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(mediations)
    

def crise_interventions():
    cat=db(db.category.category=='reaction_user.value_crise_intervention').select().first()
    crise_interventions=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(crise_interventions)
    
def informings():
    cat=db(db.category.category=='reaction_user.value_informing').select().first()
    informings=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(informings)
    

def distributing_materials():
    cat=db(db.category.category=='reaction_user.value_distributing_material').select().first()
    distributing_materials=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(distributing_materials)
    
def tasks():
    cat=db(db.category.category=='reaction_user.value_task').select().first()
    tasks=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(tasks)
    
def locations():
    cat=db(db.category.category=='reaction_user.value_location').select().first()
    locations=db(db.value.cat==cat.id).select().as_list()
    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(locations)
    
def language():
    if(session._language==lang1):
        lang='lang1'
    elif(session._language==lang2):
        lang='lang2'
    else:
        lang='lang3'

    import gluon.contrib.simplejson
    return gluon.contrib.simplejson.dumps(lang)
