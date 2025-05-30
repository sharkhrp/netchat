import subprocess
import select
import sys
import threading
from colorama import Fore, Style, init



#TODO: These are vars
exit_flag = False
yellow_color = f'{Fore.YELLOW}'
def clear_previous_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K") 


# Engine start
server_command = subprocess.Popen("sudo nc -l -p 56", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True)

readable_objects = [server_command.stdout, server_command.stderr]



# To receive messeges and display
def receive():
    while not exit_flag:

        readable, _, _ = select.select(readable_objects, [], [], 0.1)
        for readable_object in readable:

            if readable_object == server_command.stdout:
                line = server_command.stdout.readline().strip()
                if sent_flag == False:
                    print('aaa')
                    clear_previous_line()

                    print(f'{Fore.RESET}[ {Fore.GREEN}{Style.BRIGHT}MESSAGE{Fore.RESET} ] : {yellow_color}{line}{Fore.RESET}')
                    print(f'{Fore.RESET}[ {Fore.MAGENTA}{Style.BRIGHT}SEND{Fore.RESET} ] : {yellow_color}', end='', flush=True)

                else:
                    print(f'\n{Fore.RESET}[ {Fore.GREEN}{Style.BRIGHT}MESSAGE{Fore.RESET} ] : {yellow_color}{line}{Fore.RESET}')
                    print(f'{Fore.RESET}[ {Fore.MAGENTA}{Style.BRIGHT}SEND{Fore.RESET} ] : {yellow_color}', end='', flush=True)

# Start the receive thread
r_t = threading.Thread(target=receive)
r_t.start()

try:
    while not exit_flag:
        
        # To see an msg have successfully sent
        sent_flag = False

        if select.select([],[sys.stdin],[],0.1)[1]:
            d_t_s = input(f'{Fore.RESET}[ {Fore.MAGENTA}{Style.BRIGHT}SEND{Fore.RESET} ] : {yellow_color}')

            if d_t_s.lower() == "$q":
                exit_flag = True

            sent_flag = True

            message_to_send = d_t_s
            server_command.stdin.write(message_to_send + "\n")
            server_command.stdin.flush()

            
                
    # Wait for the receive thread to finish
    r_t.join()

    server_command.stdin.close()

except KeyboardInterrupt as err:
    exit_flag = True
    r_t.join()
    server_command.terminate()

except BrokenPipeError:
    print(f"{Fore.RESET}[ {Fore.LIGHTRED_EX}{Style.BRIGHT}INFO{Fore.RESET} ] : {Fore.LIGHTGREEN_EX}the connection has been stopped, sir{Fore.RESET}")
    exit_flag = True

finally:
    print(f'\n{Fore.RESET}[ {Fore.BLUE}{Style.BRIGHT}CHAT{Fore.RESET} ]-----------------------------------[ {Fore.BLUE}{Style.BRIGHT}END{Fore.RESET} ]')

