import base64
import datetime
import json
import os
import random
import signal
import socket
import sqlite3


def get_json(socket:socket):
    """
    get json from client socket
    """
    r = socket.recv(1024)
    s = json.loads(r)
    return s

def register(message:str, socket:socket):
    """
    register
    """
    try:
        conHar.execute("insert into Users(StudentNum, password, email) values(?, ?, ?)", (message['StudentNum'], message['password'], message['email']))
        conHar.commit()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(b'{"respond":"true"}')
    pass

def login(message:str, socket:socket):
    """
    login
    """
    result_factory = conHar.execute("select password from Users where StudentNum = ?", (message['StudentNum'],))
    result_tuple = result_factory.fetchone()
    print(message['password'])
    if (result_tuple == None):
        print('None')
        socket.send(b'{"respond":"false"}')
    elif (result_tuple[0] == message['password']):
        print(result_tuple[0])
        socket.send(b'{"respond":"true"}')
    else:
        print(result_tuple[0])
        socket.send(b'{"respond":"false"}')
    pass

def change_password(message:str, socket:socket):
    """
    change password
    """
    try:
        result_factory = conHar.execute("select password from Users where StudentNum=?", (message['StudentNum'],))
        result_tuple = result_factory.fetchone()
        if (result_tuple[0] == message['oldPassword']):
            conHar.execute("update Users set password=? where StudentNum=?", (message['newPassword'], message['StudentNum']))
            pass
        else:
            raise sqlite3.Error
        conHar.commit()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    except TypeError as Te:
        print(Te)
        socket.send(b'{"respond":"false"}')
    else:
        socket.send(b'{"respond":"true"}')
        pass
    pass

def get_email(message:str, socket:socket):
    """
    get email
    """
    try:
        select_factory = conHar.execute("select email from Users where StudentNum = ?", (message['StudentNum'],))
        select_tuple = select_factory.fetchone()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        send_string = '{"email":"'+str(select_tuple[0])+'"}'
        send_bytes = send_string.encode()
        socket.send(send_bytes)
        pass
    pass

def post_order(message:str, socket:socket):
    """
    post order
    订单号的生成需要在原有订单号的基础上不断累加
    接单者学号置为全零
    取现在时间作为下单时间
    确认码为四位随机字符
    订单状态为"waiting"
    """
    ticket_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
    begin_time = datetime.datetime.now().strftime("%H:%M:%S")
    end_time = (datetime.datetime.now()+datetime.timedelta(minutes=int(message['Time']))).strftime("%H:%M:%S")
    certi_code = base64.b64encode(bytearray(os.urandom(3))).decode()
    try:
        conMem.execute('insert into ticket(TicketNum, Taddress, Gaddress, Item, Time, phoneNum, StudentNum, BroNum, CertiCode, BeginTime, EndTime, Status) values(?,?,?,?,?,?,?,?,?,?,?,?)',
        (ticket_id, message['Taddress'],message['Gaddress'],message['Item'],message['Time'],message['phoneNum'],message['StudentNum'],'0000000000000', certi_code, begin_time, end_time, 'waiting'))
        conMem.commit()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        send_string = '{"TicketNum":"'+str(ticket_id)+'", "CertiCode":"'+ certi_code +'"}'
        send_bytes = send_string.encode()
        socket.send(send_bytes)
        pass
    pass

def get_order(message:str, socket:socket):
    """
    get order
    """
    try:
        result_factory = conMem.execute('select TicketNum, Taddress, Gaddress, Item, EndTime, phoneNum, BeginTime, StudentNum from ticket where Gaddress=? and Status="waiting"', (message['Gaddress'],))
        result_array = result_factory.fetchmany(int(message["Num"]))
        target_array = []
        for result_tuple in result_array:

            target_dict = dict(zip(('TicketNum', 'Taddress', 'Gaddress', 'Item', 'Time', 'phoneNum', 'BeginTime', 'StudentNum'), result_tuple))
            target_array.append(target_dict)
            pass
        target_json = json.dumps(target_array).encode()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(target_json)
        pass
    pass

def confirm_order(message:str, socket:socket):
    """
    confirm order
    """
    result_factory = conMem.execute('select Status from ticket where TicketNum=?', (message['TicketNum'],))
    result_array = result_factory.fetchone()
    send_string_true = '{"TicketNum":"'+message['TicketNum']+'", "respond":"true"}'
    send_bytes_true = send_string_true.encode()
    send_string_false = '{"TicketNum":"'+message['TicketNum']+'", "respond":"false"}'
    send_bytes_false = send_string_false.encode()
    try:
        if result_array[0] == 'waiting':
            conMem.execute('update ticket set BroNum=?, Status=? where TicketNum=?', (message['StudentNum'], 'seized', message['TicketNum']))
            print(send_bytes_true)
            socket.send(send_bytes_true)
            pass
        else:
            print(send_bytes_false)
            socket.send(send_bytes_false)
            pass
        conMem.commit()
        pass
    except TypeError as Te2:
        print(Te2)
        socket.send(send_bytes_false)
        pass

def get_order_status(message:str, socket:socket):
    """
    get order status
    """
    try:
        result_factory = conMem.execute('select TicketNum, Status, Certicode from ticket where StudentNum=?', (message['StudentNum'],))
        result_array = result_factory.fetchall()
        target_array = []
        for result_tuple in result_array:
            target_dict = dict(zip(('TicketNum', 'Status', 'CertiCode'), result_tuple))
            target_array.append(target_dict)
            pass
        target_json = json.dumps(target_array).encode()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(target_json)
        pass
    pass

def get_working_status(message:str, socket:socket):
    """
    get working status
    """
    try:
        result_factory = conMem.execute('select TicketNum, Status, Taddress, Gaddress, phoneNum, EndTime from ticket where BroNum=?', (message['StudentNum'],))
        result_array = result_factory.fetchall()
        target_array = []
        for result_tuple in result_array:
            target_dict = dict(zip(('TicketNum', 'Status', 'Taddress', 'Gaddress', 'phoneNum', 'Time'), result_tuple))
            target_array.append(target_dict)
            pass
        target_json = json.dumps(target_array).encode()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(target_json)
        pass
    pass

def get_ticket_status(message:str, socket:socket):
    """
    get ticket status
    """
    try:
        result_factory = conMem.execute('select TicketNum, Status from ticket where TicketNum=?', (message['TicketNum'],))
        result_array = result_factory.fetchone()
        target_dict = dict(zip(('TicketNum', 'Status'), result_array))
        target_json = json.dumps(target_dict).encode()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(target_json)
        pass
    pass

def cancel_ticket(message:str, socket:socket):
    """
    cancel ticket
    """
    try:
        result_factory = conMem.execute('select TicketNum, Item, StudentNum, BroNum, BeginTime, Taddress from ticket where TicketNum=?', (message['TicketNum'],))
        result_tuple = result_factory.fetchone()
        conHar.execute('insert into Record(TicketNum, Item, StudentNum, BroNum, BeginTime, Taddress) values(?,?,?,?,?,?)',result_tuple)
        conMem.execute('delete from ticket where TicketNum=?', (message['TicketNum'],))
        conMem.commit()
        conHar.commit()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(b'{"respond":"true"}')
        pass
    pass

def get_all_info(message:str, socket:socket):
    """
    get all info
    """
    try:
        result_factory = conMem.execute('select TicketNum, Taddress, Gaddress, Item, Status, StudentNum, BroNum, phoneNum, CertiCode ,EndTime from ticket where TicketNum=?', (message['TicketNum'],))
        result_tuple = result_factory.fetchone()
        target_dict = dict(zip(('TicketNum','Taddress', 'Gaddress', 'Item', 'Status', 'StudentNum', 'BroNum', 'phoneNum', 'CertiCode', 'Time'), result_tuple))
        target_json = json.dumps(target_dict).encode()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    except TypeError as te:
        print(te)
        socket.send(b'{"respond":"false"}')
    else:
        socket.send(target_json)
        pass
    pass

def forget_password(message:str, socket:socket):
    """
    forget password
    """
    try:
        result_factory = conHar.execute("select password from Users where StudentNum=?", (message['StudentNum'],))
        result_tuple = result_factory.fetchone()
        if (result_tuple == None):
            socket.send(b'{"respond":"false"}')
        else:
            conHar.execute("update Users set password=? where StudentNum=?", ('123456', message['StudentNum']))
            pass
        conHar.commit()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(b'{"respond":"true"}')
        pass
    pass

def admin_require(message:str, socket:socket):
    """
    admin require
    """
    try:
        result_factory = conMem.execute('select TicketNum, Taddress, Gaddress, Item, StudentNum, BroNum, Status from ticket')
        result_array = result_factory.fetchall()
        target_array =[]
        for result_tuple in result_array:
            target_dict = dict(zip(('TicketNum', 'Taddress', 'Gaddress', 'Item', 'StudentNum', 'BroNum', 'Status'), result_tuple))
            target_array.append(target_dict)
            pass
        target_json = json.dumps(target_array).encode()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(target_json)
        pass
    pass

def terminate(message:str, socket:socket):
    """
    terminate
    """
    try:
        
        conMem.execute('delete from ticket where TicketNum=?', (message['TicketNum'],))
        conMem.commit()
        pass
    except sqlite3.Error as e:
        print(e)
        
        pass
    else:

        pass
    pass
    pass

def get_history(message:str, socket:socket):
    """
    get history
    """
    try:
        result_factory = conHar.execute('select TicketNum, Item, StudentNum, BroNum, BeginTime, Taddress from Record where StudentNum=?', (message['StudentNum'],))
        result_array = result_factory.fetchall()
        target_array = []
        for result_tuple in result_array:
            target_dict = dict(zip(('TicketNum', 'Item', 'StudentNum', 'BroNum', 'BeginTime', 'Taddress'), result_tuple))
            target_array.append(target_dict)
            pass
        target_json = json.dumps(target_array).encode()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(target_json)
        pass
    pass
    pass

def confirm_done(message:str, socket:socket):
    """
    confirm ticket done
    """
    try:
        result_factory = conMem.execute('select TicketNum, Item, StudentNum, BroNum, BeginTime, Taddress from ticket where TicketNum=?', (message['TicketNum'],))
        result_tuple = result_factory.fetchone()
        conHar.execute('insert into Record(TicketNum, Item, StudentNum, BroNum, BeginTime, Taddress) values(?,?,?,?,?,?)',result_tuple)
        conMem.execute('delete from ticket where TicketNum=?', (message['TicketNum'],))
        conMem.commit()
        conHar.commit()
        pass
    except sqlite3.Error as e:
        print(e)
        socket.send(b'{"respond":"false"}')
        pass
    else:
        socket.send(b'{"respond":"true"}')
        pass
    pass

def quit(signum, frame):
    """
    ctrl-c to exit
    """
    server_listening_socket.close()
    clientsocket.close()
    print('SIGINT or CTRL-C detected.')
    print('Listen Socket Closed')
    conHar.close()
    conMem.close()
    print('Database Closed')
    print('Exiting gracefully')
    exit(0)

conMem = sqlite3.connect(":memory:")
conHar = sqlite3.connect("Users.db")

# Create the table
conMem.execute("""create table ticket(
    TicketNum INTEGER PRIMARY KEY     NOT NULL, 
    Taddress TEXT    NOT NULL, 
    Gaddress TEXT    NOT NULL,
    Item TEXT    NOT NULL,
    Time INT    NOT NULL,
    phoneNum CHAR(4)    NOT NULL,
    StudentNum CHAR(13) NOT NULL, 
    BroNum CHAR(13) NOT NULL, 
    CertiCode CHAR(4) NOT NULL, 
    BeginTime TEXT NOT NULL, 
    EndTime TEXT NOT NULL, 
    Status TEXT NOT NULL
    )""")

# close is not a shortcut method and it's not called automatically,
# so the connection object should be closed manually
conMem.commit()

past_time = '0'

#host = socket.gethostname() #get host name as ip
server_listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #set a listening socket
TCP_port = 9998 #set local port 9998 as TCP listening
server_listening_socket.bind(("", TCP_port))  #bind ip and port
server_listening_socket.listen(5) #start listening top to 5

signal.signal(signal.SIGINT, quit)

while True:
    clientsocket,addr = server_listening_socket.accept() #set TCP connections   
    print("Address: %s" % str(addr)) #Let us know a client have already connected
    received_message = get_json(clientsocket) #receive from client
    print(received_message)
    try:
        result = {
        'register':register,
        'login':login,
        'changePassword':change_password,
        'getEmail':get_email,
        'postOrder':post_order,
        'getOrder':get_order,
        'INeedMoney':confirm_order,
        'getOrderStatus':get_order_status,
        'getWorkingStatus':get_working_status,
        'getTicketStatus':get_ticket_status,
        'cancelTicket':cancel_ticket,
        'getTicketAllInfo':get_all_info,
        'forgetPassword':forget_password,
        'AdminRequire':admin_require,
        'Terminate':terminate,
        'getHistory':get_history,
        'confirmTicketDone':confirm_done
        }[received_message['type']](received_message, clientsocket)
        pass
    except KeyError as KEr:
        print(KEr)
        continue
    clientsocket.close()
    pass
