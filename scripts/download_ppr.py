from irish_property_analysis.ppr_sale import Sales
from irish_property_analysis.utils import download_ppr_zip, extract_ppr_zip
from irish_property_analysis.settings import PPR_LOCATION


def main():
    zip_location = PPR_LOCATION + ".dl.zip"

    download_ppr_zip(zip_location)
    extract_ppr_zip(zip_location, PPR_LOCATION)

    sales = Sales.load(PPR_LOCATION)
    sales.save(PPR_LOCATION)


if __name__ == "__main__":
    main()
