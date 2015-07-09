@auth.requires(auth.has_membership(role='Straathoekwerkers'))    
def tag():
    
    if len(signal_user_tag_errors)==0:
 			
        if len(request.args)!=0:
            session.signal_userID = request.args[0]       
       
        signal_record=db(db.signal_user.id==session.signal_userID).select().first()
        user_record=db(db.user.id==signal_record.user).select().first()
        
        form1=FORM(TABLE(TR(TD(LABEL(T('Signal :')),_class="w2p_f1"),TD(INPUT(_name='title',_readonly='readonly'))),
                    TR(TD(LABEL(T('Created by :')),_class="w2p_f1"),TD(INPUT(_name='user',_readonly='readonly',_type='text'))),
                    TR(TD(LABEL(T('Date :')),_class="w2p_f1"),TD(INPUT(_name='date',_readonly='readonly')))),_id='form1') 
                    
        form1.vars.title=signal_record.title
        form1.vars.user=user_record.first_name
        form1.vars.date=(signal_record.date).strftime('%d-%m-%Y')
        
        form1.validate()
        
        fields = ['tag']
        form2 = SQLFORM(db.signal_user_tag,fields=fields,hidden=dict(signal_user=session.signal_userID),labels={'tag':''},submit_button = 'Add Tag')
        form2.vars.signal_user = session.signal_userID
        if form2.accepts(request,session):
            response.flash = ''
        elif form2.errors:
            response.flash = T('form has errors')
        
        delete_same_tag()
        
        fields = [db.signal_user_tag.tag]
        form3 = SQLFORM.grid(db.signal_user_tag.signal_user==session.signal_userID,fields = fields, ui = 'jquery-ui',deletable=False,details=False,create=False,editable=False,csv=False,searchable=False,paginate=10,
        links=[lambda row:A(T('Delete'),_href=URL("delete_tag",args=[row.id]))])
        
        if(signal_record.user!=auth.user.id):
            response.flash=''
            fields = [db.signal_user_tag.tag]
            form2=''
            form3 = SQLFORM.grid(db.signal_user_tag.signal_user==session.signal_userID,fields = fields, ui = 'jquery-ui',deletable=False,details=False,create=False,editable=False,csv=False,searchable=False,paginate=10)
        
        if(tags_already_added()):
            button=TAG.INPUT(_value=T('Next'),_type="button",_onclick="window.location='%s';"%URL(r=request,c='signal_user',f='details')) 
        else:
            button=None

            
        if(session.signal_user_inserted==1):
            response.flash=T('Signal inserted, please add some tags !')
            session.signal_user_inserted=0
        if(session.no_tags_added==1):
            response.flash=T('Please add at least 1 Tag !!!')
            session.no_tags_added=0            
        else:
            response.flash=T('Manage your signal tags') 
           
        return dict(form1=form1,form2=form2,form3=form3,button=button)
    
    else:
        session.type_error='signal_user_tag'
        redirect(URL(r=request,c='error',f='category_value'))

def delete_same_tag():
    signal_userID=session.signal_userID   
    signal_user_tag_rows=db(db.signal_user_tag.signal_user==signal_userID).select()      
    
    for row1 in signal_user_tag_rows:     
        teller=0
        for row2 in signal_user_tag_rows:          
            if row1.tag==row2.tag:
                teller=teller+1
                if teller>1:
                    db(db.signal_user_tag.id == row2.id).delete()
                    break


def delete_tag():
    if len(request.args)!=0:
        signal_user_tagID = request.args[0]
    db(db.signal_user_tag.id == signal_user_tagID).delete()
    redirect(URL(r=request,c='signal_user_tag',f='tag'))

def tags_already_added():
    signal_user_tag_records=db(db.signal_user_tag.signal_user==session.signal_userID).select()
    if(len(signal_user_tag_records)==0):
        session.no_tags_added=1
        return False
    else:
        return True
