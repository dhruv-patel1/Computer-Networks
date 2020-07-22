import socket
import sys
import threading

lsHost = sys.argv[1]
lsPort = int(sys.argv[2])

def client():
    try:
        ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client LS socket has been created")
    except socket.error as err:
        print("Socket open error: {} \n".format(err))

    ls_binding = (lsHost, lsPort)
    ls.connect(ls_binding)

    write_file = open("RESOLVED.txt", "w")

    with open("PROJ2-HNS.txt", "r") as read_file:
        for host in read_file:
            str_host = host.strip()
            str_host = str_host.lower()

            print("[S]: Query for {}".format(str_host))
            ls.send(str_host.encode('utf-8'))
            rcv = ls.recv(1024).decode('utf-8')
            print("[C]: Forwarding [{}]".format(rcv))

            write_data = rcv.split(" ")
            data_len = len(write_data)
            for x in range(0, data_len):
                write_file.write(write_data[x]+" ")
                if data_len-x == 1:
                    write_file.write("\n")

    read_file.close()

    final = "READFILEEMPTY"
    ls.send(final.encode('utf-8'))
    write_file.close()
    ls.close()
    return


t1 = threading.Thread(name="client", target=client())
t1.start()