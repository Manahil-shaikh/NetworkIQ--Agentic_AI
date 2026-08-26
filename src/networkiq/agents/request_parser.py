import re


def parse_request(request: str) -> dict:
    """
    Extract basic network identifiers from a user request.

    Currently supports cell IDs such as:
        ISB_001
        ISB_002
        RWP_003
        LHR_001
    """

    cell_match = re.search(
        r"\b[A-Z]{2,5}_\d{3}\b",
        request.upper(),
    )

    cell_id = (
        cell_match.group(0)
        if cell_match
        else None
    )

    region = None

    region_map = {
        "ISLAMABAD": "Islamabad",
        "RAWALPINDI": "Rawalpindi",
        "LAHORE": "Lahore",
        "KARACHI": "Karachi",
    }

    request_upper = request.upper()

    for key, value in region_map.items():

        if key in request_upper:
            region = value
            break

    return {
        "cell_id": cell_id,
        "region": region,
    }