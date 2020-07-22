import socket
import sys

def client_ts(ts_host, ts_port, line):
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created to contact Top Level Server")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    ts_ip = socket.gethostbyname(ts_host)
    ts_binding = (ts_ip, ts_port)
    ts.connect(ts_binding)

    ts.send(line.encode('utf-8'))
    ts_msg = ts.recv(4096).decode('utf-8')


    ts.close()
    return ts_msg


def client_rs():
    rs_hostname = sys.argv[1]
    rslistenport = int(sys.argv[2])
    tslistenport = int(sys.argv[3])

    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created to contact Root Server")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    rs_ip = socket.gethostbyname(rs_hostname)
    rs_binding = (rs_hostname, rslistenport)
    rs.connect(rs_binding)

    read_file = open("PROJI-HNS.txt", "r")
    write_file = open("RESOLVED.txt", "w")

    host = read_file.readline()
    while host:
        stripped_host = host.strip()
        print("[C]: client is going to query for {}".format(str(stripped_host)))

        rs.send(stripped_host.encode('utf-8'))
        rs_receive = rs.recv(4096).decode('utf-8')
        rsr_split = rs_receive.split()

        if rsr_split[2] == 'A':
            print("[C]: Entry found in Root Server: {}".format(str(rs_receive)))
            write_file.write(rs_receive)
            write_file.write("\n")

        elif rsr_split[2] == 'NS':
            ts_msg = client_ts(rsr_split[0], tslistenport, stripped_host)
            ts_msg_split = ts_msg.split()

            if ts_msg_split[2] == 'A':
                print("[C]: Entry found in Top Level Server: {}". format(str(ts_msg)))
                write_file.write(ts_msg)
                write_file.write("\n")
            elif ts_msg_split[2] == 'Error:HOST':
                print("[C]: Could not find IP for host: {}".format(str(ts_msg)))
                write_file.write(ts_msg)
                write_file.write("\n")

        else:
            raise Error("[C]: Client has the wrong or no flag")

        host = read_file.readline()

    rs.send('finished'.encode('utf-8'))


    read_file.close()
    write_file.close()
    rs.close()
    return

client_rs()






