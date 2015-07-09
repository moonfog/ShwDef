def read_reaction():
    if len(reaction_user_errors) == 0 :
        if len(request.args) != 0:
            session.contactpartsID = request.args(0)
    contactpartsId = session.contactpartsID

    reactionRows = db(db.reaction_user.contact_part == contactpartsId).select()
    for row in reactionRows :
        typeRow = db(db.value.id == row.type).select().first()
        subjectRow = db(db.value.id == row.subject).select().first()
        if (session._language==lang1):
             row.type = typeRow.val_lang1
             row.subject = subjectRow.val_lang1 
        if (session._language==lang2):
             row.type = typeRow.val_lang2
             row.subject = subjectRow.val_lang2
        if (session._language==lang3):
             row.type = typeRow.val_lang3
             row.subject = subjectRow.val_lang3

    return dict(rows=reactionRows)
