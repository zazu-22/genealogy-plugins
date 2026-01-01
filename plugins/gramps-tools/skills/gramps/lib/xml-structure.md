# Gramps XML Structure

Complete reference for the Gramps XML export format.

## File Format

### Compression
- `.gramps` files are **gzip-compressed** XML
- Decompress with: `gunzip -c file.gramps`
- For git-friendly diffs, export uncompressed XML

### Document Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE database PUBLIC "-//Gramps//DTD Gramps XML 1.7.2//EN"
"http://gramps-project.org/xml/1.7.2/grampsxml.dtd">
<database xmlns="http://gramps-project.org/xml/1.7.2/">
  <header>...</header>
  <events>...</events>
  <people>...</people>
  <families>...</families>
  <citations>...</citations>
  <sources>...</sources>
  <places>...</places>
  <objects>...</objects>
  <repositories>...</repositories>
  <notes>...</notes>
  <tags>...</tags>
  <bookmarks>...</bookmarks>
</database>
```

## Element Reference

### Person
```xml
<person handle="_abc123" change="1766898490" id="I0001">
  <gender>M</gender>
  <name type="Birth Name">
    <first>John</first>
    <surname>Smith</surname>
    <suffix>Jr.</suffix>
  </name>
  <name type="Also Known As">
    <first>Jack</first>
    <surname>Smith</surname>
  </name>
  <eventref hlink="_event_handle" role="Primary"/>
  <attribute type="Occupation" value="Farmer"/>
  <childof hlink="_family_handle"/>
  <parentin hlink="_family_handle"/>
  <citationref hlink="_citation_handle"/>
  <noteref hlink="_note_handle"/>
  <tagref hlink="_tag_handle"/>
</person>
```

**Name Types**: `Birth Name`, `Married Name`, `Also Known As`, `Nickname`
**Event Roles**: `Primary`, `Witness`, `Celebrant`, `Informant`

### Family
```xml
<family handle="_abc123" change="1403481600" id="F0001">
  <rel type="Married"/>
  <father hlink="_person_handle"/>
  <mother hlink="_person_handle"/>
  <eventref hlink="_event_handle" role="Family"/>
  <childref hlink="_person_handle"/>
  <childref hlink="_person_handle" mrel="Birth" frel="Birth"/>
  <attribute type="_UID" value="..."/>
  <citationref hlink="_citation_handle"/>
  <noteref hlink="_note_handle"/>
</family>
```

**Relationship Types**: `Married`, `Unmarried`, `Civil Union`, `Unknown`
**Child Relationship (mrel/frel)**: `Birth`, `Adopted`, `Stepchild`, `Foster`, `Unknown`

### Event
```xml
<event handle="_abc123" change="1766898490" id="E0001">
  <type>Birth</type>
  <dateval val="1850-03-15"/>
  <place hlink="_place_handle"/>
  <description>Optional description</description>
  <attribute type="Cause" value="Natural causes"/>
  <noteref hlink="_note_handle"/>
  <citationref hlink="_citation_handle"/>
</event>
```

**Date Variants**:
```xml
<dateval val="1850-03-15"/>                    <!-- Exact date -->
<dateval val="1850" type="about"/>             <!-- Approximate -->
<dateval val="1850" type="before"/>            <!-- Before date -->
<dateval val="1850" type="after"/>             <!-- After date -->
<daterange start="1850" stop="1860"/>          <!-- Range -->
<datespan start="1850-01" stop="1850-12"/>     <!-- Span -->
<datestr val="Spring 1850"/>                   <!-- Text date -->
```

**Common Event Types**:
- Personal: `Birth`, `Death`, `Burial`, `Baptism`, `Christening`, `Cremation`
- Life: `Occupation`, `Education`, `Religion`, `Residence`, `Immigration`, `Emigration`, `Naturalization`
- Family: `Marriage`, `Divorce`, `Engagement`, `Marriage Banns`

### Place
```xml
<placeobj handle="_abc123" change="1767053739" id="P0001" type="City">
  <ptitle>Zanesville, Muskingum County, Ohio, USA</ptitle>
  <pname value="Zanesville" lang="en"/>
  <pname value="Zanesville" lang="abbr"/>
  <coord long="-82.01320" lat="39.94035"/>
  <placeref hlink="_parent_place_handle"/>
  <url href="https://..." type="Web Home"/>
  <noteref hlink="_note_handle"/>
  <citationref hlink="_citation_handle"/>
</placeobj>
```

**Place Types**: `Country`, `State`, `County`, `City`, `Town`, `Parish`, `Building`, `Cemetery`, `Unknown`

**Place Hierarchy**: Use `placeref` to link to parent places (e.g., City → County → State → Country)

### Source
```xml
<source handle="_abc123" change="1403481600" id="S0001">
  <stitle>1900 U.S. Census</stitle>
  <sauthor>U.S. Census Bureau</sauthor>
  <spubinfo>Washington, D.C.</spubinfo>
  <sabbrev>1900 Census</sabbrev>
  <noteref hlink="_note_handle"/>
  <objref hlink="_media_handle"/>
  <srcattribute type="TYPE" value="Census"/>
  <reporef hlink="_repository_handle" callno="T623" medium="Microfilm"/>
</source>
```

### Citation
```xml
<citation handle="_abc123" change="1766898490" id="C0001">
  <dateval val="2024-01-15"/>
  <page>Page 5, Line 23</page>
  <confidence>2</confidence>
  <noteref hlink="_note_handle"/>
  <objref hlink="_media_handle"/>
  <srcattribute type="Date Accessed" value="2024-01-15"/>
  <sourceref hlink="_source_handle"/>
</citation>
```

**Confidence Levels**:
- `0` - Very Low
- `1` - Low
- `2` - Normal (default)
- `3` - High
- `4` - Very High

### Note
```xml
<note handle="_abc123" change="1766898490" id="N0001" type="General">
  <text>Note content with optional styling</text>
  <style name="bold" value="1">
    <range start="0" end="10"/>
  </style>
  <tagref hlink="_tag_handle"/>
</note>
```

**Note Types**: `General`, `Research`, `Transcript`, `Source text`, `Citation`, `Report`, `Html code`

### Media Object
```xml
<object handle="_abc123" change="1766898490" id="O0001">
  <file src="Documents/certificate.jpg" mime="image/jpeg"
        checksum="abc123" description="Birth Certificate"/>
  <attribute type="Date" value="1850-03-15"/>
  <noteref hlink="_note_handle"/>
  <dateval val="1850-03-15"/>
  <citationref hlink="_citation_handle"/>
  <tagref hlink="_tag_handle"/>
</object>
```

### Repository
```xml
<repository handle="_abc123" change="1766898490" id="R0001">
  <rname>National Archives</rname>
  <type>Archive</type>
  <address>
    <street>700 Pennsylvania Avenue NW</street>
    <city>Washington</city>
    <state>DC</state>
    <postal>20408</postal>
    <country>USA</country>
  </address>
  <url href="https://www.archives.gov/" type="Web Home"/>
  <noteref hlink="_note_handle"/>
</repository>
```

**Repository Types**: `Archive`, `Library`, `Church`, `Web site`, `Collection`, `Unknown`

## Cross-References

### Handle Links
All cross-references use the `hlink` attribute pointing to a `handle`:

```xml
<!-- Event references a place -->
<event handle="_event1">
  <place hlink="_place1"/>
</event>

<!-- Citation references a source -->
<citation handle="_citation1">
  <sourceref hlink="_source1"/>
</citation>

<!-- Person references events, families, citations -->
<person handle="_person1">
  <eventref hlink="_event1" role="Primary"/>
  <childof hlink="_family1"/>
  <citationref hlink="_citation1"/>
</person>
```

### Reference Attributes
- `eventref`: Includes `role` attribute
- `childref`: Includes `mrel` (mother relation) and `frel` (father relation)
- `objref`: Can include region coordinates for cropping
- `reporef`: Includes `callno` (call number) and `medium`

## Portable Package (.gpkg)

The `.gpkg` format bundles:
- Gramps XML (uncompressed)
- All referenced media files
- Packaged as tar.gz archive

```bash
# Extract gpkg
tar -xzf family.gpkg

# Contents
family.gramps    # XML file
media/           # Media files directory
```
