# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = T('Registratie Straathoekwerk :')
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################


def isVanType(type):            
    rows = db(db.group_membership.group_id==db.group_role.id).select()
    for row in rows:
        if( row.group_membership.user_id==auth.user.id and row.group_role.role==type  ):
            return True
    return False
    


if (auth.user==None):
     response.menu = []

elif (isVanType('Administrators') and isVanType('Straathoekwerkers') and isVanType('Managers') ):

    response.menu = [
    (T('Contact'),False, None, [
        (T('New'),False, URL('contact','new')),
        (T('Overview'),False,URL('contact','mycal'))]),
    (T('Signal'),False, None, [
        (T('New'),False, URL('signal_user','new')),
        (T('Overview'),False,URL('signal_user','overview'))]),    
    (T('Guest'), False, None,[
        (T('New'),False, URL('guest','new')),
        (T('Overview'),False, URL('guest','overview')),
        ]),
    (T('Management'), False, None, [
               (T('User'),False, URL('management','user')),
               (T('Group memberships'),False, URL('management','group_membership')),   
               (T('Values'), False, URL('management','value'))]),        
	(T('Overviews'), False, None, [
			   (T('Guest'),False, URL('manager_overview','overview_guests')),
			   (T('Contacts'),False, URL('manager_overview','overview_contact_parts')),   
			   (T('Conditions'), False, URL('manager_overview','overview_conditions'))])                 
    ]


elif (isVanType('Administrators') and isVanType('Straathoekwerkers')):

    response.menu = [
    (T('Contact'),False, None, [        
        (T('New'),False, URL('contact','new')),
        (T('Overview'),False,URL('contact','mycal'))]),
    (T('Signal'),False, None, [       
        (T('New'),False, URL('signal_user','new')),
        (T('Overview'),False,URL('signal_user','overview'))]),    
    (T('Guest'), False, None,[
        (T('New'),False, URL('guest','new')),
        (T('Overview'),False, URL('guest','overview')),
         ]),
     (T('Management'), False, None, [
           (T('Values'), False, URL('management','value'))])        
               
                    
    ]
    
elif (isVanType('Administrators') and isVanType('Managers')):

    response.menu = [
    (T('Signal'),False, None, [
        (T('Overview'),False, URL('signal_user','overview'))]),
    
    (T('Management'), False, None, [
               (T('User'),False, URL('management','user')),
               (T('Group memberships'),False, URL('management','group_membership')),   
               (T('Values'), False, URL('management','value'))]),
    (T('Overviews'), False, None, [
		       (T('Guest'),False, URL('manager_overview','overview_guests')),
		       (T('Contacts'),False, URL('manager_overview','overview_contact_parts')),   
		       (T('Conditions'), False, URL('manager_overview','overview_conditions'))])
    ]

elif (isVanType('Administrators')):

    response.menu = [
   
     (T('Management'), False, None, [
               (T('Values'),False, URL('management','value'))])]   
    

elif (isVanType('Managers') and isVanType('Straathoekwerkers')):

    response.menu = [
    (T('Contact'),False, None, [        
        (T('New'),False, URL('contact','new')),
        (T('Overview'),False,URL('contact','mycal'))]),
    (T('Signal'),False, None, [        
        (T('New'),False, URL('signal_user','new')),
        (T('Overview'),False, URL('signal_user','overview'))]),    
    (T('Guest'), False, None,[
        (T('New'),False, URL('guest','new')),
        (T('Overview'),False, URL('guest','overview')),
        ]),
    (T('Management'), False, None, [
               (T('User'),False, URL('management','user')),
               (T('Group memberships'),False, URL('management','group_membership'))])  

     
    ]

elif (isVanType('Managers')):

    response.menu = [
    (T('Signal'),False, None, [
        (T('Overview'),False, URL('signal_user','overview'))]),
    (T('Management'), False, None, [
               (T('User'),False, URL('management','user')),
               (T('Group memberships'),False, URL('management','group_membership'))]),
    (T('Overviews'), False, None, [
			   (T('Guest'),False, URL('manager_overview','overview_guests')),
			   (T('Contacts'),False, URL('manager_overview','overview_contact_parts')),   
			   (T('Conditions'), False, URL('manager_overview','overview_conditions'))]) 
# hier de menu's voor de overzichten insteken  
    ]

elif (isVanType('Straathoekwerkers')):

    response.menu = [
    (T('Contact'),False, None, [        
        (T('New'),False, URL('contact','new')),
        (T('Overview'),False,URL('contact','mycal'))]),
    (T('Signal'),False, None, [    
        (T('New'),False, URL('signal_user','new')),
        (T('Overview'),False, URL('signal_user','overview'))]), 
    (T('Guest'), False, None,[
        (T('New'),False, URL('guest','new')),
        (T('Overview'),False, URL('guest','overview')),
       ])            
    ]


else:
    response.menu = []

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################
