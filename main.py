import argparse

from utils.helpers import \
    parse_json_log, \
    get_ip_location, \
    convert_unix_time_to_local_time, \
    save_array_to_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ogExtractor - get information from log")
    parser.add_argument("--input", type=str, help="Input file path.", default="./input/sample.log")
    parser.add_argument("--output", type=str, help="Result in CSV.", default="./output/result.csv")
    args = parser.parse_args()

    logs = parse_json_log(args.input)

    result = []
    city = ''
    isp = ''
    for log in logs:
        req = log.get("req", {})
        headers = req.get("headers", None)

        if not headers:
            continue

        client_ip_address = headers.get("x-real-ip", '')
        user_agent = headers.get("user-agent", '')

        if client_ip_address != '':
            location_data = get_ip_location(client_ip_address)
            city = location_data.get("city", '')
            isp = location_data.get("isp", '')

        if type(log.get("time")) == int:
            local_time = convert_unix_time_to_local_time(log.get("time", None))
        else:
            local_time = log.get("time", '')

        log_info = [local_time, client_ip_address, city, isp, user_agent]
        result.append(log_info)

        print(f' {log["time"]} - {client_ip_address} - {user_agent} - {city} - {isp}')

    save_array_to_csv(result, args.output)
