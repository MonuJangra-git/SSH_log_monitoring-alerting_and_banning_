import json
class FileHandler:
    def file_writer(self, content):
        with open("threat_ip.log", "a") as file:
            file.write(content + "\n")
    def file_manager(self, stats, recent_logs):
        try:
            with open("threat_ip.log", "w") as file:
                file.write("=" * 75 + "\n")
                file.write("THREAT DETECTION SCORECARD\n")
                file.write("=" * 75 + "\n\n")
                total_attacks = sum(stats.values())
                file.write(f"TOTAL ATTACKS DETECTED: {total_attacks}\n\n")
                for attack_type in stats:   #every attack type stats and recent logs are written to the file for reference
                    file.write(f"[{attack_type.upper()}]\n")
                    file.write(f"Failed Attempts: {stats[attack_type]}\n")
                    file.write("Last 10 Logs:\n") #recent logs means the last 10 logs of that attack type which are stored in the recent_logs dictionary and written to the file for reference and stats means the total count of that attack type which is stored in the stats dictionary and written to the file for reference
                    if recent_logs[attack_type]:
                        for log in recent_logs[attack_type]:
                            file.write(f"  {log}")
                    else:
                        file.write("  No logs recorded yet.\n")
                    file.write("\n" + "-" * 75 + "\n")
        except Exception as e:
            print(f"Error updating scorecard: {e}")
    def file_manager_json(self,stats,recent_logs):
        try:
            data = {
                "total_attacks": sum(stats.values()),
                "attack_details": {}
            }
            for attack_type in stats: # attack_type is the key of the stats dictionary which represents the type of attack and stats[attack_type] is the value of that key which represents the total count of that attack type and recent_logs[attack_type] is the value of that key which represents the last 10 logs of that attack type which are stored in the recent_logs dictionary and written to the json file for reference
                data["attack_details"][attack_type] = {
                    "failed_attempts": stats[attack_type],# every attack type stats and recent logs are written to the json file for reference
                    "recent_logs": recent_logs[attack_type][-10:] # last 10 logs of that attack type are stored in the recent_logs dictionary and written to the json file for reference and stats means the total count of that attack type which is stored in the stats dictionary and written to the json file for reference
                }
            with open("threat_ip.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            print(f"Error updating JSON scorecard: {e}")
    def output_log(self,content):
        with open("output.log","a") as f :
            f.write(content)
