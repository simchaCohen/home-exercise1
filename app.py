import random, string
from flask import Flask , render_template, request ,session
from flask_session import Session

#start the application
app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_letters) for _ in range(30))
Session(app)
app.config['SESSION_TYPE'] = 'redis'
app.config.from_object(__name__)
sess = Session()
#data sorted for testing
data1={"applicationId": "123",
       "sessionId": "345",
       "messageId": "678",
       "participants": ["simcha" , "hilel" , "rachel"],
       "content": "hello to particpant 123"  }
data2={"applicationId": "123",
       "sessionId": "223",
       "messageId": "223",
       "participants": ["nomi" , "avi" , "yaakov"],
       "content": "hello to particpant 223"  }
allData=[data1,data2]
#stored the data in session
sess.allData = allData

#home page
@app.route('/')
def Index():
   return render_template('index.html')

#get the messages adjusted with the parameter
class Get():
   
    @app.route('/GetMessage', methods=['GET', 'POST'])
    def GetMessage():
       id=None
       messageList=[]
       messages=None
       allData=sess.allData
       #check if the iputs are filled
       if request.method == 'POST' and 'id' in request.form and 'parameter' in request.form:
          id=request.form['id']
          param=request.form['parameter']
          #search in the message the appropriate messages
          for data in allData:
              if id==data[param]:
                 messageList.append(data)
        
       return render_template('GetMessage.html',id=str(id),messages=messageList)
      
  

#add new messages adjusted with the parameter
class Post():
   @app.route('/AddMessage', methods=['GET', 'POST'])
   def AddMessage():
     #check if the iputs are filled
      if request.method == 'POST' and 'applicationId' in request.form:
          applicationId=request.form['applicationId']
          if 'sessionId' in request.form :
             sessionId=request.form['sessionId']
             if'messageId' in request.form:
                 messageId=request.form['messageId']
                 if 'participants' in request.form and 'content' in request.form:
                     participants=request.form['participants']
                     content=request.form['content']
                     allData=sess.allData
                     #add the new message
                     allData.append({"applicationId":applicationId,"sessionId":sessionId,"messageId":messageId,"participants":participants,"content":content})
                     sess.allData=allData
                     flag=1
      return render_template('AddMessage.html')
   
#delete the messages adjusted with the parameter   
class Delete():
    @app.route('/DeleteMessage', methods=['GET', 'POST'])
    def DeleteMessage():
       id=None
       allData=sess.allData
       #check if the iputs are filled
       if request.method == 'POST' and 'id' in request.form and 'parameter' in request.form:
          id=request.form['id']
          param=request.form['parameter']
          #search in the message the appropriate messages
          for data in allData:
              if id==data[param]:
                 allData.remove(data)
       sess.allData=allData
       return render_template('DeleteMessage.html')
          
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
