# About GRIN

GRIN provides a [CAB directory](https://npgsweb.ars-grin.gov/gringlobal/downloads/default) for download. The directory has 16 files, but only on 5 are considered to create the COLDP checklist archive, detailes are avialable on the folowing table: 

| file name | checklist |
| ------------- | ------------- |
|taxonomy_species.txt |  Yes|
|taxonomy_genus.txt | Yes |
|taxonomy_family.txt | Yes |
|taxonomy_common_name.txt | Yes |
|taxonomy_author.txt | Yes |
|taxonomy_use.txt | No |
|taxonomy_noxious.txt | No|
|taxonomy_alt_family_map.txt |No |
|taxonomy_geography_map.txt |No |
|geography.txt | No |
|geography_region_map.txt | No |
|region.txt | No |
|site.txt | No |
|citation.txt | No |
|cooperator.txt | No |
|literature.txt | No |

Below is the maping of each file to COLDP including the considerations made to use some of the fields during data transformation.

# taxonomy_species file

| selected_fields | work_names | coldp_name | comments |
|---|---|---|---|
| current_taxonomy_species_id | parentID | parentID | The accepted name id, parent ID for Synonyms |
| nomen_number | ID | ID | Nomen number on the url and the one that is showed up on the webpage |
| is_specific_hybrid | is_specific_hybrid |  | for conditional |
| species_name | specificEpithet | specificEpithet |  |
| is_subspecific_hybrid | is_subspecific_hybrid |  | for conditional |
| subspecies_name | infraespecificEpithet | infraespecificEpithet |  |
| is_varietal_hybrid | is_varietal_hybrid |  | for conditional |
| variety_name | infraespecificEpithet | infraespecificEpithet |  |
| taxonomy_genus_id | taxonomy_genus_id |  | To cross data with the taxonomy_genus file |
| synonym_code | status | status | A=Autonym, B= Basionym,  I= Invalid Designation, S= Heterotypic Synonym |
| name_verified_date | scrutinizerDate | scrutinizerDate |  |
| name | scientificName | scientificName |  |
| name_authority | authorship | authorship |  |
| protologue | citation | citation | For reference class, a protologue is a term used in botanical nomenclature to refer to the original description of a plant species when it is first formally named. Remove html markers |
| protologue_virtual_path | publishedInPageLink | publishedInPageLink | A protologue is a term used in botanical nomenclature to refer to the original description of a plant species when it is first formally named. Remove html markers |
| hybrid_parentage | hybrid_parentage | remarks | Build remark as  "Hybrid parentage: ----" HTML tags need to be removes |
| is_web_visible | is_web_visible |  | It is not clear why the name is not visible on the website, nevertheless could be use as a filter |


# taxonomy_genus file

| all_field | selected_fields | work_names | coldp_name | comments |
|---|---|---|---|---|
| taxonomy_genus_id | taxonomy_genus_id | ID | ID |  |
| current_taxonomy_genus_id | current_taxonomy_genus_id | current_taxonomy_genus_id | parentID | Combination of genus, subgenus, series, section etc... |
| taxonomy_family_id | taxonomy_family_id | parentID | parentID | to cross data with Taxonomy_genus file |
| qualifying_code | qualifying_code | status | status | Needs data transformation, parentID, (=~) Ussually considered synonym of, (~) possible synonym, (=) synonym of |
| hybrid_code | hybrid_code | hybrid_code |  | As prefix of name, (+)  for graft chimaera, (x) hybrid |
| genus_name | genus_name | genus_name | genus |  |
| genus_authority | genus_authority | authorship | authorship | Of the lowest string category?  genus, subgenus, series, section |
| subgenus_name | subgenus_name | subgenus_name | subgenus |  |
| section_name | section_name | section_name | section |  |
| subsection_name | subsection_name | subsection_name | scientificName |  |
| series_name | series_name | series_name | scientificName |  |
| subseries_name | subseries_name | subseries_name | scientificName |  |
| note | note | remarks | remarks | Html tags present |
| is_web_visible | is_web_visible | is_web_visible |

