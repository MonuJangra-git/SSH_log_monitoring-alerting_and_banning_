from log_analyser import log_monitoring_and_alerting

if __name__ == "__main__":
    file_name = "/var/log/auth.log"
    try:
        monitor = log_monitoring_and_alerting(file_name)
        monitor.analyser()
    except KeyboardInterrupt:
        print("exit successfully ")