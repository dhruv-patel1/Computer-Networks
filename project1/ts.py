import socket
import sys
import threading

def connection(sock, ts_table):
    while True:
        clientData = sock.recv(4096).decode('utf-8')
        clientData = clientData.strip().lower()
        print("[S]: Search for IP for the host: ", clientData)

        if clientData in ts_table:
            address = ts_table[clientData]
            print("[S]: Hostname address found: ", address)
            sock.send(address.encode('utf-8'))
        else:
            res = clientData + " - Error:HOST NOT FOUND"
            print("[S]: Server could not find request")
            sock.send(res.encode('utf-8'))

        sock.close()
        return


def server_ts():
    ts_port = int(sys.argv[1])
    ts_table = {}

    with open("PROJI-DNSTS.txt", "r") as file:
        for line in file:
            line_split = line.split()
            host = line_split[0].strip()
            ip = line_split[1]

            if line_split[2] == 'A':
                ts_table[host.lower()] = line.strip()
    file.close()

    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("[S]: Root server host is: {} and the ip is: {}".format(hostname, ip))
    ts_binding = ('', ts_port)
    ts.bind(ts_binding)
    ts.listen(1)

    while True:
        sock, addr = ts.accept()
        print("[S]: Connection requested from client: ", addr)

        t2 = threading.Thread(name='server', target=connection, args=(sock, ts_table))
        t2.start()

    ts.close()


server_ts()
