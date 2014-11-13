############################################################
#   MONGODB SCRIPT FOR MASTER PASSWORD APPLICATION         #
############################################################
# use 'master' database
use master

# upsert admin with a hashed password, if the record exists then don't do anything
# admin password Sdnob14 (TODO: remove this line)
db.users2.update (
    {_id : 1},
    {
        _id: 1,
        first: 'admin',
        last:  'tmc',
        login: 'admin',
        hash: '$2a$12$NrksQGmyd8o6xipX.kdW1OtxBWzACKtSoAHmlvJVIUBPLbS1CviPm',
        lastModified: new Date(),
        pws: [
            {
                env: 'DEV',
                encpass:[ 'D\x04\xc1<\x8e\xb1\xb8\xc3' ]
            },
            {
                env: 'PROD',
                encpass:[]
            }
        ]
    },
    {  upsert: true  }
);

# add an environment (UAT, STAGE)
db.users2.update(
    {_id: 1 },
    {
     $addToSet: {
                    'pws':{
                           env:'UAT',
                           encpass:[]
                    }
                }
    }
);

# each user will have his/her own set of encrypted password (based on his master password)
# add a password to an environment (PROD, for example)
var encpass_cursor = db.users2.find({_id: 1})
encpass_cursor.forEach(function (col_elem){
    all_pws = col_elem.pws;
    all_pws.forEach(function(pws){
       if (pws.env == 'PROD'){
         pws.encpass.push({username: 'acelrc1', password: 'yeah-newpassword-uat'});
         db.users2.save(col_elem);
         return;
       }
    });
});




