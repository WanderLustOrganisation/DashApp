import subprocess
import time
import argparse

slaves =  ["10.142.0.6", "10.142.0.3", "10.142.0.2", "10.142.0.5"]

master_ip = "10.142.0.4"

MAX_SLAVES = len(slaves)

def calculate_workload():
    workload = 2
    return min(workload, MAX_SLAVES)

def is_machine_up(ip):
    result = subprocess.run(["ping","-c","1", ip], capture_output=True)
    return result.returncode == 0

def start_slave(slave, args):
    if not is_machine_up(slave):
        print(f"{slave} is down. Skipping....")
        return False
    print(f"Starting slave on {slave}")
    java_command = ["ssh",f"user@{slave}", "java", "-jar", "slave_demo-0.0.1-SNAPSHOT.jar"] + args
    result = subprocess.run(java_command, capture_output=True)
    if result.returncode != 0:
        print(f"Failed to start slave on {slave}: {result.stderr.decode()}")
        return False
    return True

def notify_master(num_slaves,  topic, fecha_inicial, fecha_final):
    print(f"Notifying master about {num_slaves} slaves")
    java_command = ["java", "-jar", "master_demo-0.0.1-SNAPSHOT.jar", topic, fecha_inicial, fecha_final, str(num_slaves)]
    result = subprocess.run(java_command, capture_output=True)
    if result.returncode != 0:
        print(f"Failed to notify master: {result.stderr.decode()}")
        return False
    return True


def main(topic, fecha_inicial, fecha_final):
    num_slaves_needed = calculate_workload()
    slaves_started = 0

    for i in range(num_slaves_needed):
        slave_args = [(str)(i+1), master_ip]
        if start_slave(slaves[i], slave_args):
            slaves_started += 1

    if slaves_started > 0:
        notify_master(slaves_started, topic, fecha_inicial, fecha_final)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start slave processes and notify the master.")
    parser.add_argument("topic", help="The topic for the job")
    parser.add_argument("fecha_inicial", help="The initial date in the format yyyy/MM/dd")
    parser.add_argument("fecha_final", help="The final date in the format yyyy/MM/dd")
    args = parser.parse_args()
    main(args.topic, args.fecha_inicial, args.fecha_final)