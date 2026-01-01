#!/usr/bin/env python3
"""
Citation Formatter

Helper utilities for formatting genealogical citations following
Evidence Explained conventions.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re


@dataclass
class Citation:
    """Base class for citation data."""
    source_type: str
    title: str
    creator: Optional[str] = None
    publication_place: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[str] = None
    page: Optional[str] = None
    url: Optional[str] = None
    access_date: Optional[str] = None
    repository: Optional[str] = None
    notes: Optional[str] = None


def format_access_date(date: Optional[str] = None) -> str:
    """
    Format access date in Evidence Explained style (day month year).

    Args:
        date: Date string or None for today's date

    Returns:
        Formatted date string
    """
    if date is None:
        d = datetime.now()
    else:
        # Try to parse common date formats
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y']:
            try:
                d = datetime.strptime(date, fmt)
                break
            except ValueError:
                continue
        else:
            return date  # Return as-is if can't parse

    return d.strftime('%d %B %Y').lstrip('0')


def format_url_with_access(url: str, access_date: Optional[str] = None) -> str:
    """
    Format URL with access date in Evidence Explained style.

    Args:
        url: The URL
        access_date: Access date (defaults to today)

    Returns:
        Formatted URL string
    """
    date_str = format_access_date(access_date)
    return f"({url} : accessed {date_str})"


def format_census_citation(
    year: int,
    state: str,
    county: str,
    township: str,
    page: str,
    dwelling: int,
    family: int,
    head_name: str,
    url: Optional[str] = None,
    access_date: Optional[str] = None,
    nara_publication: Optional[str] = None,
    roll: Optional[str] = None
) -> str:
    """
    Format a U.S. Census citation.

    Args:
        year: Census year
        state: State name
        county: County name
        township: Township or city name
        page: Page number (with penned/stamped if applicable)
        dwelling: Dwelling number
        family: Family number
        head_name: Name of household head
        url: Digital image URL
        access_date: Access date
        nara_publication: NARA microfilm publication number
        roll: Microfilm roll number

    Returns:
        Formatted citation string
    """
    citation = f"{year} U.S. census, {state}, {county}, {township}, "
    citation += f"population schedule, p. {page}, dwelling {dwelling}, "
    citation += f"family {family}, {head_name}"

    if url:
        # Determine source platform from URL
        if 'ancestry.com' in url.lower():
            platform = "Ancestry.com"
        elif 'familysearch.org' in url.lower():
            platform = "FamilySearch"
        else:
            platform = "digital image"

        citation += f"; digital image, {platform} "
        citation += format_url_with_access(url, access_date)

    if nara_publication and roll:
        citation += f", citing NARA microfilm {nara_publication}, roll {roll}"

    citation += "."
    return citation


def format_vital_record_citation(
    jurisdiction: str,
    record_type: str,
    name: str,
    event_date: str,
    certificate_no: Optional[str] = None,
    database_name: Optional[str] = None,
    url: Optional[str] = None,
    access_date: Optional[str] = None
) -> str:
    """
    Format a vital record citation.

    Args:
        jurisdiction: Issuing jurisdiction (state/county)
        record_type: Type of record (birth, death, marriage)
        name: Person's name
        event_date: Date of event
        certificate_no: Certificate number if available
        database_name: Online database name
        url: Digital image URL
        access_date: Access date

    Returns:
        Formatted citation string
    """
    citation = f"{jurisdiction}, {record_type}"

    if certificate_no:
        citation += f" no. {certificate_no}"

    citation += f", {name}, {event_date}"

    if database_name and url:
        citation += f'; "{database_name}," digital image'
        if 'familysearch.org' in url.lower():
            citation += ", FamilySearch "
        elif 'ancestry.com' in url.lower():
            citation += ", Ancestry.com "
        else:
            citation += " "
        citation += format_url_with_access(url, access_date)

    citation += "."
    return citation


def format_findagrave_citation(
    memorial_id: int,
    name: str,
    birth_year: Optional[int],
    death_year: Optional[int],
    cemetery: str,
    city: str,
    county: str,
    state: str,
    access_date: Optional[str] = None
) -> str:
    """
    Format a Find A Grave citation.

    Args:
        memorial_id: Find A Grave memorial number
        name: Deceased's name
        birth_year: Birth year
        death_year: Death year
        cemetery: Cemetery name
        city: City
        county: County
        state: State
        access_date: Access date

    Returns:
        Formatted citation string
    """
    dates = ""
    if birth_year and death_year:
        dates = f" ({birth_year}–{death_year})"
    elif birth_year:
        dates = f" (b. {birth_year})"
    elif death_year:
        dates = f" (d. {death_year})"

    citation = "Find A Grave, database and images "
    citation += format_url_with_access("https://www.findagrave.com", access_date)
    citation += f", memorial {memorial_id} for {name}{dates}, "
    citation += f"{cemetery}, {city}, {county}, {state}."

    return citation


def format_newspaper_citation(
    headline: Optional[str],
    newspaper: str,
    city: str,
    state: str,
    date: str,
    page: str,
    column: Optional[str] = None,
    url: Optional[str] = None,
    access_date: Optional[str] = None
) -> str:
    """
    Format a newspaper citation.

    Args:
        headline: Article headline (if any)
        newspaper: Newspaper name
        city: City of publication
        state: State
        date: Publication date
        page: Page number
        column: Column number (optional)
        url: Digital image URL
        access_date: Access date

    Returns:
        Formatted citation string
    """
    citation = ""

    if headline:
        citation += f'"{headline}," '

    citation += f"{newspaper} ({city}, {state}), {date}, p. {page}"

    if column:
        citation += f", col. {column}"

    if url:
        # Determine platform
        if 'newspapers.com' in url.lower():
            platform = "Newspapers.com"
        elif 'genealogybank.com' in url.lower():
            platform = "GenealogyBank"
        else:
            platform = url.split('/')[2] if '/' in url else "online"

        citation += f"; digital image, {platform} "
        citation += format_url_with_access(url, access_date)

    citation += "."
    return citation


def source_list_from_note(note_citation: str) -> str:
    """
    Convert a first reference note to source list format.

    This is a simplified converter that handles common patterns.

    Args:
        note_citation: Citation in first reference note format

    Returns:
        Citation in source list format (best effort)
    """
    # This is a simplified implementation
    # Full conversion requires understanding the source type

    # Remove note number if present
    citation = re.sub(r'^[\d]+\s*', '', note_citation.strip())

    # If starts with author name, try to reverse it
    match = re.match(r'^([A-Z][a-z]+)\s+([A-Z][a-z]+),', citation)
    if match:
        first, last = match.groups()
        citation = f"{last}, {first}," + citation[match.end():]

    # Remove specific page references (simplistic)
    citation = re.sub(r',\s*p\.\s*\d+', '', citation)
    citation = re.sub(r',\s*pp\.\s*\d+[-–]\d+', '', citation)

    return citation


def main():
    """Demonstration of citation formatting."""
    print("Citation Formatter Examples\n")
    print("=" * 60)

    # Census example
    print("\n1. Census Citation:")
    census = format_census_citation(
        year=1850,
        state="Ohio",
        county="Muskingum County",
        township="Zanesville",
        page="123 (penned)",
        dwelling=45,
        family=47,
        head_name="John Smith",
        url="https://www.ancestry.com",
        nara_publication="M432",
        roll="723"
    )
    print(census)

    # Vital record example
    print("\n2. Vital Record Citation:")
    vital = format_vital_record_citation(
        jurisdiction="Ohio Department of Health",
        record_type="certificate of death",
        name="John Smith",
        event_date="15 March 1925",
        certificate_no="12345",
        database_name="Ohio, Deaths, 1908–1953",
        url="https://www.familysearch.org"
    )
    print(vital)

    # Find A Grave example
    print("\n3. Find A Grave Citation:")
    grave = format_findagrave_citation(
        memorial_id=12345678,
        name="John Smith",
        birth_year=1850,
        death_year=1925,
        cemetery="Woodlawn Cemetery",
        city="Zanesville",
        county="Muskingum County",
        state="Ohio"
    )
    print(grave)

    # Newspaper example
    print("\n4. Newspaper Citation:")
    news = format_newspaper_citation(
        headline="John Smith, Pioneer Resident, Dies",
        newspaper="Zanesville Times Recorder",
        city="Zanesville",
        state="Ohio",
        date="15 March 1925",
        page="3",
        column="2",
        url="https://www.newspapers.com/image/12345"
    )
    print(news)

    print("\n" + "=" * 60)
    print("\nAccess date formatting:")
    print(f"  Today: {format_access_date()}")
    print(f"  From ISO: {format_access_date('2024-01-15')}")


if __name__ == '__main__':
    main()
