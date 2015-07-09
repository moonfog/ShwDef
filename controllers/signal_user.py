# coding: utf8
# try something like
def index(): return dict(message="hello from signal.py")

def overview():

    if len(signal_user_errors)==0:

        fields = [db.signal_user.user, db.signal_user.date,db.signal_user.title , db.signal_user.subject]
        form = SQLFORM.grid(db.signal_user,fields = fields, ui = 'jquery-ui',details=False,create=False,editable=False,deletable=False,csv=False,paginate=10,orderby=[~db.signal_user.date],
        links=[lambda row:A(T('Details'),_href=URL("signal_user","details",args=[row.id])),
           lambda row:A(T('Tags'),_href=URL("signal_user_tag","tag",args=[row.id]))])
    
        return dict(form=form)
    
    else:
        session.type_error='signal_user'
        redirect(URL(r=request,c='error',f='category_value'))
    
@auth.requires(auth.has_membership(role='Straathoekwerkers'))    
def new():

    if len(signal_user_errors)==0:
    
        fields = ['title','subject','description']
        form = SQLFORM(db.signal_user,fields=fields,hidden=dict(user=auth.user.id))
        form.vars.user = auth.user.id
        session._signal_user_tag_rows=None
        form[0][-1][1].append(TAG.INPUT(_value=T('Cancel'),_type="button",_onclick="window.location='%s';"%URL(r=request,f='overview'))) 
        if form.accepts(request,session):
            session.signal_userID=form.vars.id
            session.signal_user_tag_rows=db(db.signal_user_tag.signal_user == session.signal_userID).select()
            session.signal_user_inserted=1
            redirect(URL(c='signal_user_tag',f='tag'))
        elif form.errors:
            response.flash = T('form has errors')
        else:
            response.flash = T('Create Signal')
            
        return dict(form=form)
        
    else:
        session.type_error='signal_user'
        redirect(URL(r=request,c='error',f='category_value'))
        
    

    

    
def details():
    
    if len(signal_user_errors)==0:
    
        if len(request.args)!=0:
            session.signal_userID = request.args[0]
        
        signalRow = db(db.signal_user.id == session.signal_userID).select().first()
        userId=signalRow.user
        valueId=signalRow.subject
    
        userRow=db(db.user.id == userId).select().first()
        valueRow=db(db.value.id == valueId).select().first()
    
        form=FORM(TABLE(TBODY(TR(TD(LABEL(T('Title :')),_class="w2p_f1"),TD(INPUT(_name='signal_user_title',_readonly='readonly',_type='text'),_class="w2p_fw")),
                    TR(TD(LABEL(T('Date :')),_class="w2p_f1"),TD(INPUT(_name='signal_user_date',_readonly='readonly'),_class="w2p_fw")),
                    TR(TD(LABEL(T('User :')),_class="w2p_f1"),TD(INPUT(_name='signal_user_user',_readonly='readonly',_type='text'),_class="w2p_fw")),                    
                    TR(TD(LABEL(T('Subject :')),_class="w2p_f1"),TD(INPUT(_name='signal_user_subject',_readonly='readonly',_type='text'),_class="w2p_fw")),
                    TR(TD(LABEL(T('Description :')),_class="w2p_f1"),TD(TEXTAREA(_name='signal_user_description',_readonly='readonly',_type='text'),_class="w2p_fw")))),_id='form1')   
       
        form.vars.signal_user_title=signalRow.title
        form.vars.signal_user_date=(signalRow.date).strftime('%d-%m-%Y')
        form.vars.signal_user_user=userRow.first_name+" "+userRow.last_name
        if(session._language==lang1):form.vars.signal_user_subject=valueRow.val_lang1
        if(session._language==lang2):form.vars.signal_user_subject=valueRow.val_lang2
        if(session._language==lang3):form.vars.signal_user_subject=valueRow.val_lang3
        form.vars.signal_user_description=signalRow.description
    
        signal_record=db(db.signal_user.id==session.signal_userID).select().first()
    
        if(signal_record.user==auth.user.id):    
            my_extra_element1 = TR(TD(_class="w2p_fl"),TD(INPUT(_type="button",_value=T('Edit'),_onclick="window.location='%s';"%URL(r=request,f='edit')),INPUT(_type="button",_value="Tags",_onclick="window.location='%s';"%URL(c='signal_user_tag',f='tag')),INPUT(_type="button",_value="Overview",_onclick="window.location='%s';"%URL(f='overview')),_class="w2p_fw"))
            form[0][0][-1].append(my_extra_element1)  
        form.validate()
        
        if(session.signal_user_updated==1):
            response.flash=T('Signal updated')        

        session.signal_user_updated=0

        return dict(form=form)
    
    else:
        session.type_error='signal_user'
        redirect(URL(r=request,c='error',f='category_value'))
    

    
@auth.requires(auth.has_membership(role='Straathoekwerkers'))
def edit():

    if len(signal_user_errors)==0:
        record = db(db.signal_user.id==session.signal_userID).select().first()
        fields = ['title' , 'subject', 'description','date']
        form = SQLFORM(db.signal_user,record,fields=fields,showid = False,submit_button = 'Update')
        form[0][-1][1].append(TAG.INPUT(_value=T('Cancel'),_type="button",_onclick="window.location='%s';"%URL(r=request,f='details')))
        
        if form.process().accepted: 
            session.signal_user_updated=1
            redirect(URL(r=request,f='details')) 
        elif form.errors:
            response.flash = T('form has errors')
        else:
            response.flash = T('Update Signal')

        return dict(form=form)
   
    else:
        session.type_error='signal_user'
        redirect(URL(r=request,c='error',f='category_value'))
