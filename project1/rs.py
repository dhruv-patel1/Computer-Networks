import socket
import sys
import threading

def connection(sock, rs_table, ts_host):
    while True:
        clientData = sock.recv(4096).decode('utf-8').strip().lower()
        print("[S]: Search for IP for the host: ", clientData)

        if clientData in rs_table:
                address = rs_table[clientData]
                print("[S]: Hostname address found: {}".format(str(address)))
                sock.send(address.encode('utf-8'))
        elif clientData == 'finished':
                break
        else:
                print("[S]: Server could not find request")
                sock.send(ts_host.encode('utf-8'))

    sock.close()
    return

def server_rs():
    rs_port = int(sys.argv[1])
    rs_table = {}
    ts_msg = ''
    file = open("PROJI-DNSRS.txt", "r")
    line_contents = file.readline()
    while line_contents:
            line_split = line_contents.split()
            host = line_split[0].strip()

            if line_split[2] == 'A':
                rs_table[host.lower()] = line_contents.strip()
            if line_split[2] == 'NS':
                ts_host = line_contents.strip()
            line_contents = file.readline()

    file.close()

    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Root Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    print("[S]: Root server host is: {} and the ip is: {}".format(host, ip))
    rs_binding = ('', rs_port)
    rs.bind(rs_binding)
    rs.listen(1)

    if True:
        sock, addr = rs.accept()
        print("[S]: Connection requested from client: ", addr)
        connection(sock, rs_table, ts_host)
        t1 = threading.Thread(name="server", target=connection, args=(sock, rs_table, ts_host))
        t1.start()

    rs.close()
    return

server_rs()





