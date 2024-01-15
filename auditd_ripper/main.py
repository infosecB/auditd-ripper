"""Main script"""
import argparse
import binascii
import json
from typing import List


def get_log_file(log_path: str) -> list:
    """Load and return a list of line items from a file containing auditd logs"""
    lines = []
    with open(log_path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    return lines


def parse_logs(logs: List) -> List:
    """Parse auditd logs and return a list of dictionary items the represent the events"""
    all_logs = []
    old_log = {"msg": "none"}
    for l in logs:
        d = {}
        split_line = l.split(" ")
        for i in split_line:
            if "=" in i:
                k = i.split("=")[0]
                v = i.split("=")[1]
                d[k] = v
        if old_log["msg"] == d["msg"]:
            d = {**d, **old_log}
            old_log = d
        else:
            if old_log["msg"] != "none":
                all_logs.append(old_log)
                old_log = d
            else:
                old_log = d
        if logs.index(l) == len(logs) - 1:
            all_logs.append(old_log)

    return all_logs


def export_json(path: str, content: list) -> None:
    """Exports json to specified file"""
    with open(path, mode="w", encoding="utf-8") as out_file:
        out_file.write(json.dumps(content, indent=4))
        out_file.close()


def decrypt_proctitle(logs: List) -> List:
    """Decrypts the proctitle field in each log entry"""
    for l in logs:
        if "proctitle" in l.keys():
            try:
                l["proctitle"] = (
                    binascii.unhexlify(l["proctitle"].rstrip("\n"))
                    .decode("ascii")
                    .replace("\u0000", " ")
                )
            except:  # pylint: disable=bare-except
                pass

    return logs


def parse_arguments():
    """Parse CLI input"""
    parser = argparse.ArgumentParser(
        description="Process an auditd file and output result."
    )
    parser.add_argument(
        "-p", "--path", help="Auditd log file", dest="input", required=True
    )
    parser.add_argument(
        "-o", "--output", help="JSON output file path", dest="output", required=True
    )
    return parser.parse_args()


def main():
    """Main function runs whenever the script is run from a shell"""
    args = parse_arguments()
    raw_logs = get_log_file(args.input)
    logs = parse_logs(logs=raw_logs)
    decoded_logs = decrypt_proctitle(logs=logs)
    export_json(path=args.output, content=decoded_logs)
    print(logs)


if __name__ == "__main__":
    main()
