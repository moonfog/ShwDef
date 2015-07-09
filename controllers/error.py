def category_value():   
 
    errors=[]
    
    if(session.type_error=='guest'):errors=guest_errors
    if(session.type_error=='condition_guest'):errors=condition_guest_errors
    if(session.type_error=='contact'):errors=contact_errors
    if(session.type_error=='contact_part'):errors=contact_part_errors
    if(session.type_error=='contact_part_tag'):errors=contact_part_tag_errors
    if(session.type_error=='reaction_user'):errors=reaction_user_errors
    if(session.type_error=='signal_user'):errors=signal_user_errors
    if(session.type_error=='signal_user_tag'):errors=signal_user_tag_errors 
    
    messages=[]
    
    for category in errors:
        line="Category "+category+" does not exist or does not have values !"
        messages.append(line)
        
    
    endLine="Please contact your administrator !"
    
    messages.append(endLine)
      
    return dict(messages=messages)
