#!/usr/bin/env python3
"""
Gramps XML Utilities

Utility functions for parsing and analyzing Gramps XML export files.
"""

import gzip
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
from typing import Optional
import sys

# Gramps XML namespace
NS = {'gramps': 'http://gramps-project.org/xml/1.7.2/'}


def load_gramps_xml(filepath: str) -> ET.Element:
    """
    Load a Gramps XML file (handles both .gramps and uncompressed XML).

    Args:
        filepath: Path to .gramps or .xml file

    Returns:
        Root Element of the XML tree
    """
    path = Path(filepath)

    if path.suffix == '.gramps':
        with gzip.open(path, 'rb') as f:
            tree = ET.parse(f)
    else:
        tree = ET.parse(path)

    return tree.getroot()


def get_statistics(root: ET.Element) -> dict:
    """
    Get counts of all primary objects in the database.

    Args:
        root: Root element of Gramps XML

    Returns:
        Dictionary with object counts
    """
    stats = {}

    sections = [
        ('people', 'person'),
        ('families', 'family'),
        ('events', 'event'),
        ('places', 'placeobj'),
        ('sources', 'source'),
        ('citations', 'citation'),
        ('repositories', 'repository'),
        ('notes', 'note'),
        ('objects', 'object'),
        ('tags', 'tag'),
    ]

    for section_name, element_name in sections:
        section = root.find(f'gramps:{section_name}', NS)
        if section is not None:
            count = len(section.findall(f'gramps:{element_name}', NS))
            stats[section_name] = count
        else:
            stats[section_name] = 0

    return stats


def get_event_types(root: ET.Element) -> Counter:
    """
    Count occurrences of each event type.

    Args:
        root: Root element of Gramps XML

    Returns:
        Counter of event types
    """
    events = root.find('gramps:events', NS)
    if events is None:
        return Counter()

    types = []
    for event in events.findall('gramps:event', NS):
        type_elem = event.find('gramps:type', NS)
        if type_elem is not None and type_elem.text:
            types.append(type_elem.text)

    return Counter(types)


def get_source_types(root: ET.Element) -> Counter:
    """
    Count occurrences of each source type.

    Args:
        root: Root element of Gramps XML

    Returns:
        Counter of source types
    """
    sources = root.find('gramps:sources', NS)
    if sources is None:
        return Counter()

    types = []
    for source in sources.findall('gramps:source', NS):
        for attr in source.findall('gramps:srcattribute', NS):
            if attr.get('type') == 'TYPE':
                types.append(attr.get('value', 'Unknown'))
                break
        else:
            types.append('Unclassified')

    return Counter(types)


def find_persons_by_surname(root: ET.Element, surname: str) -> list:
    """
    Find all persons with a given surname.

    Args:
        root: Root element of Gramps XML
        surname: Surname to search for (case-insensitive)

    Returns:
        List of dicts with handle, id, and full name
    """
    people = root.find('gramps:people', NS)
    if people is None:
        return []

    results = []
    surname_lower = surname.lower()

    for person in people.findall('gramps:person', NS):
        for name in person.findall('gramps:name', NS):
            for sn in name.findall('gramps:surname', NS):
                if sn.text and sn.text.lower() == surname_lower:
                    first = name.find('gramps:first', NS)
                    first_name = first.text if first is not None and first.text else ''
                    surname_text = sn.text

                    results.append({
                        'handle': person.get('handle'),
                        'id': person.get('id'),
                        'name': f"{first_name} {surname_text}".strip()
                    })
                    break

    return results


def find_uncited_events(root: ET.Element) -> list:
    """
    Find events without any citations.

    Args:
        root: Root element of Gramps XML

    Returns:
        List of dicts with event id, type, and description
    """
    events = root.find('gramps:events', NS)
    if events is None:
        return []

    uncited = []

    for event in events.findall('gramps:event', NS):
        citations = event.findall('gramps:citationref', NS)
        if not citations:
            type_elem = event.find('gramps:type', NS)
            desc_elem = event.find('gramps:description', NS)

            uncited.append({
                'id': event.get('id'),
                'type': type_elem.text if type_elem is not None else 'Unknown',
                'description': desc_elem.text if desc_elem is not None else ''
            })

    return uncited


def find_orphan_citations(root: ET.Element) -> list:
    """
    Find citations that reference non-existent sources.

    Args:
        root: Root element of Gramps XML

    Returns:
        List of orphan citation IDs
    """
    # Get all source handles
    sources = root.find('gramps:sources', NS)
    source_handles = set()
    if sources is not None:
        for source in sources.findall('gramps:source', NS):
            source_handles.add(source.get('handle'))

    # Check citation references
    citations = root.find('gramps:citations', NS)
    if citations is None:
        return []

    orphans = []
    for citation in citations.findall('gramps:citation', NS):
        sourceref = citation.find('gramps:sourceref', NS)
        if sourceref is not None:
            ref_handle = sourceref.get('hlink')
            if ref_handle not in source_handles:
                orphans.append(citation.get('id'))

    return orphans


def validate_xml(root: ET.Element) -> dict:
    """
    Run basic validation checks on the Gramps XML.

    Args:
        root: Root element of Gramps XML

    Returns:
        Dictionary with validation results
    """
    results = {
        'valid': True,
        'warnings': [],
        'errors': []
    }

    # Check for uncited events
    uncited = find_uncited_events(root)
    if uncited:
        results['warnings'].append(f"{len(uncited)} events without citations")

    # Check for orphan citations
    orphans = find_orphan_citations(root)
    if orphans:
        results['errors'].append(f"{len(orphans)} citations reference missing sources")
        results['valid'] = False

    # Check for persons without events
    people = root.find('gramps:people', NS)
    if people is not None:
        no_events = 0
        for person in people.findall('gramps:person', NS):
            eventrefs = person.findall('gramps:eventref', NS)
            if not eventrefs:
                no_events += 1
        if no_events:
            results['warnings'].append(f"{no_events} persons without any events")

    return results


def main():
    """Command-line interface for Gramps XML utilities."""
    if len(sys.argv) < 2:
        print("Usage: xml-utils.py <command> <gramps-file> [args...]")
        print("\nCommands:")
        print("  stats <file>              - Show database statistics")
        print("  events <file>             - Count event types")
        print("  sources <file>            - Count source types")
        print("  search <file> <surname>   - Find persons by surname")
        print("  uncited <file>            - Find events without citations")
        print("  validate <file>           - Run validation checks")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'stats' and len(sys.argv) >= 3:
        root = load_gramps_xml(sys.argv[2])
        stats = get_statistics(root)
        print("Database Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    elif command == 'events' and len(sys.argv) >= 3:
        root = load_gramps_xml(sys.argv[2])
        types = get_event_types(root)
        print("Event Types:")
        for event_type, count in types.most_common():
            print(f"  {event_type}: {count}")

    elif command == 'sources' and len(sys.argv) >= 3:
        root = load_gramps_xml(sys.argv[2])
        types = get_source_types(root)
        print("Source Types:")
        for source_type, count in types.most_common():
            print(f"  {source_type}: {count}")

    elif command == 'search' and len(sys.argv) >= 4:
        root = load_gramps_xml(sys.argv[2])
        surname = sys.argv[3]
        results = find_persons_by_surname(root, surname)
        print(f"Persons with surname '{surname}':")
        for person in results:
            print(f"  {person['id']}: {person['name']}")

    elif command == 'uncited' and len(sys.argv) >= 3:
        root = load_gramps_xml(sys.argv[2])
        uncited = find_uncited_events(root)
        print(f"Events without citations ({len(uncited)}):")
        for event in uncited[:20]:  # Limit output
            print(f"  {event['id']}: {event['type']} - {event['description']}")
        if len(uncited) > 20:
            print(f"  ... and {len(uncited) - 20} more")

    elif command == 'validate' and len(sys.argv) >= 3:
        root = load_gramps_xml(sys.argv[2])
        results = validate_xml(root)
        print("Validation Results:")
        print(f"  Valid: {results['valid']}")
        if results['warnings']:
            print("  Warnings:")
            for warning in results['warnings']:
                print(f"    - {warning}")
        if results['errors']:
            print("  Errors:")
            for error in results['errors']:
                print(f"    - {error}")

    else:
        print(f"Unknown command or missing arguments: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
