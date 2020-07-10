from sanic import Sanic, response
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine("mysql://root:getsurikrish@localhost:surikrish/1999",echo = True)
meta = MetaData()
app = Sanic(__name__)
contacts = Table(
   'Contacts', meta,
   Column('id', Integer, primary_key = True),
   Column('name', String(50)),
   Column('phoneno', String(50)),
Column('email', String(50)),)
meta.create_all(engine)
conn = engine.connect()

LOGIN_FORM = '''
<h2>Contact</h2>
<p>{}</p>
<form action="/check" method="POST" enctype="multipart/form-data">
<label>Select Your Image:</label><br>
<input type="file" name="img" id="img" accept="image/*">
 <p>Enter Name : </p>
  <input class="username" name="username"
    placeholder="username" type="text" value=""><br>
    <p>Enter Phone number : </p>
  <input id="pn" name="pn"
    placeholder="Phone Number" type="text" value=""><br>
    <p>Enter Email : </p>
  <input id="email" name="email"
    placeholder="Email" type="text" value=""><br>
  <input type="submit" value="Sign In"></form>
  <form action="/det" method="POST">
  <input type="submit" value="Delete"></form>
  <form action="/sec" method="POST">
  <input type="submit" value="Search"></form>
  <form action="/edt" method="POST">
  <input type="submit" value="Edit"></form>
  '''
DELETE_FORM='''
<h2>Delete contact</h2>
<p>{}</p>
<form action="/delete" method="POST">
<p>Enter name : </p>
  <input id="name" name="name"
    placeholder="Name" type="text" value=""><br>
    <input type="submit" value="Delete">
    </form>
    <form action="/" >
  <input type="submit" value="Home"></form>
    '''

SEARCH_FORM= '''
<h2>Search contact</h2>
<p>{}</p>
<form action="/search" method="POST">
<p>Enter name : </p>
  <input name="name"
    placeholder="Name" type="text" value=""><br>
    <input type="submit" value="Search">
    </form>
    <form action="/">
  <input type="submit" value="Home"></form>
    '''
SHOW_FORM='''
<h2>Displaying details :</h2>
<p>{}<p>
    <form action="/">
  <input type="submit" value="Home"></form>
'''
@app.route('/')
async def login(request):
    m = 'Enter the contact details'
    return response.html(LOGIN_FORM.format(m))
@app.route('/det',methods=['POST'])
async def det(request):
    m = 'Enter the name to delete'
    return response.html(DELETE_FORM.format(m))
@app.route('/edt',methods=['POST'])
async def edt(request):
    m = 'Enter the name to delete'
    return response.html(EDIT_FORM.format(m))

@app.route('/sec',methods=['POST'])
async def sec(request):
    m = 'Enter the name to Search :'
    return response.html(SEARCH_FORM.format(m))

@app.route('/search',methods=['POST'])
async def search(request):
    if request.method=='POST':
        nam=request.form
        con = contacts.select()
        res = conn.execute(con).fetchall()
        f = 0
        for i in res:
            if nam['name'][0]==i[1]:
                print(i)
                m = 'Name :'+i[1]+'<br>Phone No :'+i[2]+'<br>Email :'+i[3]
                return response.html(SHOW_FORM.format(m))
        else:
            m = 'Name not in contacts :'
            return response.html(SEARCH_FORM.format(m))

@app.route('/delete',methods=['POST'])
async def delete(request):
    if request.method=='POST':
        nam=request.form
        con = contacts.select()
        res = conn.execute(con).fetchall()
        f = 0
        for i in res:
            if nam['name'][0]==i[1]:
                f = 1
                break
        if f:
            stmt = contacts.delete().where(contacts.c.name == nam['name'][0])
            conn.execute(stmt)
            m = nam['name'][0]+' is deleted'
            return response.html(SHOW_FORM.format(m))
        else:
            m = 'Name not in contacts :'
            return response.html(DELETE_FORM.format(m))

@app.route('/check',methods=['POST','GET'])
async def check(request):
    if request.method=='POST':
        res=request.form
        con = contacts.select()
        res = conn.execute(con).fetchall()
        print(res,res)
        f=1
        for i in res:
            if ((res['username'][0] == i[1]) or (res['pn'][0] == i[2]) or (res['email'][0] == i[3])):
                f=0
                m = 'Email or phone number or name is already registerd:'
                break
        if f:
            ins = contacts.insert().values(name = res['username'], phoneno = res['pn'],email=res['email'])
            res = conn.execute(ins)
            con = contacts.select()
            res = conn.execute(con).fetchall()
            m = 'Contact details inserted :'
            for i in res:
                print(i)
        return response.html(LOGIN_FORM.format(m))

if __name__ == '__main__':
    app.run(host='localhost', port=8000,debug='True')
