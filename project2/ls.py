import threading
import socket
import sys
import time

def lsServer():
    lsPort = int(sys.argv[1])
    ts1_host = sys.argv[2]
    ts1_port = int(sys.argv[3])
    ts2_host = sys.argv[4]
    ts2_port = int(sys.argv[5])

    try:
        ls_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: LS server socket has been created")
    except socket.error as err:
        print("LS Server Socket open error: {}".format(err))

    try:
        ts1_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 server socket has been created")
    except socket.error as err:
        print("TS1 Socket open error: {}".format(err))

    try:
        ts2_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS2 server socket has been created")
    except socket.error as err:
        print("TS2 Socket open error: {}".format(err))

    ts1_binding = (ts1_host, ts1_port)
    ts1_server.connect(ts1_binding)

    ts2_binding = (ts2_host, ts2_port)
    ts2_server.connect(ts2_binding)

    ls_binding = ('', lsPort)
    ls_server.bind(ls_binding)
    ls_server.listen(1)

    ls_sockid, addr = ls_server.accept()
    ts_query = ls_sockid.recv(1024).decode('utf-8')
    print("[S]: Received query request for {}".format(ts_query))
    while True:
        ts1_str = ""
        ts2_str = ""
        client_msg = ""
        try:
            print("[S]: Querying {} in TS1_server".format(ts_query))
            ts1_server.send(ts_query.encode('utf-8'))
            ts1_server.settimeout(5)
            ts1_str += ts1_server.recv(1024).decode('utf-8')
        except socket.timeout as err:
            print("TS1_server timeout error: {} ".format(err))

        try:
            print("[S]: Querying {} in TS2_server".format(ts_query))
            ts2_server.send(ts_query.encode('utf-8'))
            ts2_server.settimeout(5)
            ts2_str += ts2_server.recv(1024).decode('utf-8')
        except socket.timeout as err:
            print("TS2_server timeout error: {} \n".format(err))

        print("[S]: Both TS Servers have been queried")
        if ts1_str:
            print("[S]: Query found in TS1_server")
            client_msg = ts1_str
        elif ts2_str:
            print("[S]: Query found in TS2_server")
            client_msg = ts2_str
        else:
            print("[S] Query was not found")
            client_msg = ts_query + " - Error: HOST NOT FOUND"

        ls_sockid.send(client_msg.encode('utf-8'))

        ts_query = ls_sockid.recv(1024).decode('utf-8')
        print("[S]: Received query request for {}".format(ts_query))

        if ts_query == "READFILEEMPTY":
            ts1_server.send(ts_query.encode('utf-8'))
            ts1_server.close()
            ts2_server.send(ts_query.encode('utf-8'))
            ts2_server.close()
            break

    ls_server.close()
    return


t2 = threading.Thread(name="lsServer", target=lsServer)
t2.start()
