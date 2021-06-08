from ldp import LDP
import parsers

if __name__ == '__main__':
    lst = [
        ("Seattle", "city_directories/seattle.csv", parsers.Seattle_Addr, parsers.Seattle_Name, parsers.Seattle_Filter),
        # ("Chicago", "city_directories/chicago.csv", parsers.Chicago_Addr, parsers.Chicago_Name, parsers.Chicago_Filter),
        # ("Los Angeles", "city_directories/losangeles.csv", parsers.LA_Addr, parsers.LA_Name, parsers.LA_Filter),
        # ("San Francisco", "city_directories/sanfrancisco.csv", parsers.SF_Addr, parsers.SF_Name, parsers.SF_Filter)
    ]

    for city_info in lst:
        try:
            city, input_filename, addr_func, business_name_func, filter_func = city_info
            print("-" * 10, f"Running {city}", "-" * 10)
            l = LDP(input_filename, addr_func, business_name_func, filter_func=filter_func)
            l.process()
        except Exception as e:
            print("!" * 10, "Exception", str(e), "!" * 10)
