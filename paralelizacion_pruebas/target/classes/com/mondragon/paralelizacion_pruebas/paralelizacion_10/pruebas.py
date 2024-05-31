import subprocess
import datetime

def notify_master(num_slaves, topic, fecha_inicial, fecha_final):
    print(f"Notifying master about {num_slaves} slaves")
    java_command = ["java", "-jar", "master_demo-0.0.1-SNAPSHOT.jar", topic, fecha_inicial, fecha_final, str(num_slaves)]
    
    while True:
        result = subprocess.run(java_command, capture_output=True)

        stdout_output = result.stdout.decode()
        stderr_output = result.stderr.decode() 
        print(stdout_output)
        print(stderr_output)
        
        if stderr_output == "":
            return True
        else:
            # Check if the error is a connection error
            if "SQLNonTransientConnectionException" in stderr_output and "Read timed out" in stderr_output:
                print("Detected connection error, retrying...")


def main():
    fecha_inicial = "1994-01-01"
    fecha_intermedia = datetime.datetime.strptime("1995-01-01", "%Y-%m-%d")
    fecha_limite = datetime.datetime.strptime("2024-01-01", "%Y-%m-%d")

    for i in range(0, 5):
        fecha_intermedia = datetime.datetime.strptime("1995-01-01", "%Y-%m-%d")
        while fecha_intermedia < fecha_limite:
            fecha_intermedia_str = fecha_intermedia.strftime("%Y-%m-%d")
            notify_master(i, "ejemplo", fecha_inicial, fecha_intermedia_str)
            fecha_intermedia = fecha_intermedia.replace(year=fecha_intermedia.year + 1)

if __name__ == "__main__":
    main()