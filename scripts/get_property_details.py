# TODO: at some point min / max (date, bed, bath, price)

import argparse
from datetime import datetime

from tabulate import tabulate

from rtb_scraper.register import register
from rtb_scraper.tribunal import tribunals
from rtb_scraper.determination import determinations

from irish_property_analysis.settings import PPR_LOCATION
from irish_property_analysis.utils import (
    get_all_historical_listings,
    get_shares,
    get_rentals,
    clean_address_for_comparison,
    minimize_str,
    none_to_str,
)
from irish_property_analysis.ppr_sale import Sales
from irish_property_analysis.schools import schools
from irish_property_analysis.bus_stops import bus_stops


def for_print_tabulate(objects, truncate=False):
    if not objects:
        print("Nothing to show...")
        return

    keys = list(objects[0].keys())
    keys_to_remove = []
    for key in keys:
        if all(not obj.get(key) for obj in objects):
            keys_to_remove.append(key)

    # Comes from rtb db
    for obj in objects:
        obj.pop("searchable_address", None)

    if keys_to_remove:
        print(f"Removing keys: {keys_to_remove} as they are all empty")

    filtered_objects = [
        {k: v for k, v in obj.items() if k not in keys_to_remove} for obj in objects
    ]

    # Don't want price in scientific notation so put to str
    for obj in filtered_objects:
        if "price" in obj:
            obj["price"] = f"{obj['price']:,.0f}"

    if truncate:
        for obj in filtered_objects:
            if obj.get("lat"):
                obj["lat"] = round(obj["lat"], 4)
            if obj.get("lng"):
                obj["lng"] = round(obj["lng"], 4)

    if truncate:
        for obj in filtered_objects:
            for k, v in obj.items():
                if isinstance(v, datetime):
                    obj[k] = v.date()
                    continue

                if not isinstance(v, str):
                    continue

                timestamp = None
                for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        timestamp = datetime.strptime(v, fmt)
                        break
                    except ValueError:
                        continue

                if timestamp:
                    obj[k] = timestamp.date()

    return tabulate(
        [
            list(
                [
                    minimize_str(none_to_str(o)) if truncate else none_to_str(o)
                    for o in obj.values()
                ]
            )
            for obj in filtered_objects
        ],
        headers=list(filtered_objects[0].keys()) if filtered_objects else [],
        tablefmt="fancy_grid",
    )


def address_substr_csv(value: str):
    return (
        [clean_address_for_comparison(addr).lower() for addr in value.split(",")]
        if value
        else []
    )


def print_ppr(args):
    ppr_sales = Sales.load(PPR_LOCATION)

    ppr_results = []
    for address_substr in args.address_substr_csv:
        # TODO: add feature to have a list of address substrings
        ppr_results = ppr_sales.filter(
            address=address_substr, county=args.county, partial=True
        )

    final_ppr_results = []
    ppr_results_by_date = {}
    for ppr_item in ppr_results:
        if all(
            [
                i in clean_address_for_comparison(ppr_item.address)
                for i in args.address_substr_csv
            ]
        ):
            if ppr_item.address not in ppr_results_by_date:
                final_ppr_results.append(ppr_item)
                ppr_results_by_date[ppr_item.address] = [ppr_item.date]
            elif (
                ppr_item.address in ppr_results_by_date
                and ppr_item.date not in ppr_results_by_date[ppr_item.address]
            ):
                final_ppr_results.append(ppr_item)
                ppr_results_by_date[ppr_item.address].append(ppr_item.date)

    print("\nPPR:")
    print(
        for_print_tabulate(
            [i.serialise() for i in final_ppr_results], truncate=not args.all
        )
    )


def passes_listing_filter(args, listing):
    if args.county:
        if not listing["county"] == args.county:
            return False

    if args.address_substr_csv:
        if not all(
            [
                i in clean_address_for_comparison(listing["original_address"])
                for i in args.address_substr_csv
            ]
        ):
            return False

    return True


def serialise_listing_for_print(listing: dict) -> dict:
    del listing["_id"]
    del listing["clean_address"]
    listing["lat"] = listing["location"]["coordinates"][1]
    listing["lng"] = listing["location"]["coordinates"][0]
    del listing["location"]
    return listing


def add_school_score(listing_data, radius_km=1):
    if listing_data["lat"] and listing_data["lng"]:
        listing_data["school_score"] = schools.get_score(
            listing_data["lat"], listing_data["lng"], radius_km=radius_km
        )
    else:
        listing_data["school_score"] = 0
    return listing_data


def add_bus_stop_score(listing_data, radius_km=1):
    if listing_data["lat"] and listing_data["lng"]:
        listing_data["bus_stop_score"] = bus_stops.get_score(
            listing_data["lat"], listing_data["lng"], radius_km=radius_km
        )
    else:
        listing_data["bus_stop_score"] = 0
    return listing_data


def print_listing_sales(args):
    objects = []

    print("\nHistorical listing sales:")
    for listing in get_all_historical_listings():
        listing_data = serialise_listing_for_print(listing)
        if listing_data in objects:
            continue
        if passes_listing_filter(args, listing):
            listing_data = add_school_score(
                listing_data, radius_km=args.school_radius_km
            )
            listing_data = add_bus_stop_score(
                listing_data, radius_km=args.bus_stop_radius_km
            )
            objects.append(listing_data)

    print(for_print_tabulate(objects, truncate=not args.all))


def print_listing_shares(args):
    objects = []

    print("\nHistorical listing shares:")
    for listing in get_shares():
        listing_data = serialise_listing_for_print(listing)
        if listing_data in objects:
            continue
        if passes_listing_filter(args, listing):
            listing_data = add_school_score(
                listing_data, radius_km=args.school_radius_km
            )
            listing_data = add_bus_stop_score(
                listing_data, radius_km=args.bus_stop_radius_km
            )
            objects.append(listing_data)

    print(for_print_tabulate(objects, truncate=not args.all))


def print_listing_rentals(args):
    objects = []

    print("\nHistorical listing rentals:")
    for listing in get_rentals():
        listing_data = serialise_listing_for_print(listing)
        if listing_data in objects:
            continue
        if passes_listing_filter(args, listing):
            listing_data = add_school_score(
                listing_data, radius_km=args.school_radius_km
            )
            listing_data = add_bus_stop_score(
                listing_data, radius_km=args.bus_stop_radius_km
            )
            objects.append(listing_data)

    print(for_print_tabulate(objects, truncate=not args.all))


def print_rtb_registrations(args):
    register_accum = []

    for address_substr in args.address_substr_csv:
        register_results = register.filter(address=address_substr, partial=True)
        register_accum.extend(register_results)

    register_results = []
    for register_item in register_accum:
        if (
            all([i in register_item.address.lower() for i in args.address_substr_csv])
            and (args.county in register_item.address.lower() if args.county else True)
            and register_item not in register_results
        ):
            if register_item.eircode in [
                r.eircode for r in register_results
            ] and register_item.month_seen in [r.month_seen for r in register_results]:
                pass
            else:
                register_results.append(register_item)

    print_data = []
    for item in register_results:
        temp_item = item.__data__
        temp_item.pop("id")
        print_data.append(temp_item)

    print("\nRTB register results:")
    print(for_print_tabulate([d for d in print_data], truncate=not args.all))


def print_rtb_determinations(args):
    determination_accum = []

    for address_substr in args.address_substr_csv:
        # TODO: add feature to have a list of address substrings
        determination_accum.extend(
            determinations.filter(address=address_substr, partial=True)
        )

    determination_results = []
    for determination_item in determination_accum:
        if (
            all(
                [
                    i in determination_item.address.lower()
                    for i in args.address_substr_csv
                ]
            )
            and (
                args.county in determination_item.address.lower()
                if args.county
                else True
            )
            and determination_item not in determination_results
        ):
            dp = determination_item.__data__
            dp.pop("id")
            determination_results.append(dp)

    print("\nRTB determination results:")
    print(for_print_tabulate([d for d in determination_results], truncate=not args.all))


def print_rtb_tribunals(args):
    tribunal_accum = []

    for address_substr in args.address_substr_csv:
        # TODO: add feature to have a list of address substrings
        tribunal_accum.extend(tribunals.filter(address=address_substr, partial=True))

    tribunal_results = []
    for tribunal_item in tribunal_accum:
        if (
            all([i in tribunal_item.address.lower() for i in args.address_substr_csv])
            and (args.county in tribunal_item.address.lower() if args.county else True)
            and tribunal_item not in tribunal_results
        ):
            if tribunal_item.tribunal_ref_no not in [
                d.tribunal_ref_no for d in tribunal_results
            ]:
                tribunal_results.append(tribunal_item)

    print_data = []
    for item in tribunal_results:
        temp_item = item.__data__
        temp_item.pop("id")
        print_data.append(temp_item)

    print("\nRTB tribunal results:")
    print(for_print_tabulate([d for d in print_data], truncate=not args.all))


def main():
    parser = argparse.ArgumentParser(
        description="Get all available details about an address"
    )
    parser.add_argument(
        "--address-substr-csv",
        dest="address_substr_csv",
        type=address_substr_csv,
        help="CSV values of address substrings that must be within the found address (e.g. '13,dublin,grand canal')",
        default=[],
    )
    parser.add_argument("--county", type=str, help="County to search in")
    parser.add_argument(
        "--school-radius-km",
        type=float,
        help="How wide around a property to search for schools",
        default=1,
    )
    parser.add_argument(
        "--bus-stop-radius-km",
        type=float,
        help="How wide around a property to search for bus stops",
        default=1,
    )
    parser.add_argument(
        "--all", action="store_true", help="Don't truncate long strings"
    )

    # TODO
    # parser.add_argument(
    #    "--exclude-address-substr-csv",
    #    dest="exclude_address_substr_csv",
    #    type=address_substr_csv,
    #    help="CSV values of address substrings that must not be within the found address (e.g. '13,dublin,grand canal')",
    #    default=[],
    # )
    # parser.add_argument(
    #    "--eircode", type=str, help="eircode to search for, overides address-substr-csv"
    # )

    args = parser.parse_args()

    print_listing_sales(args)
    print_listing_shares(args)
    print_listing_rentals(args)

    print_rtb_tribunals(args)
    print_rtb_determinations(args)
    print_rtb_registrations(args)

    print_ppr(args)


if __name__ == "__main__":
    main()
