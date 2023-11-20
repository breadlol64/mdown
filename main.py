import modrinth_api as modrinth
import requests as r

if __name__ == "__main__":
    query = input("Enter query > ")
    found_projects_id = modrinth.search_projects(query)

    mod_count = 0
    for mod_id in found_projects_id:
        print(f"{mod_count}. {modrinth.get_project_title_by_id(mod_id)}")
        mod_count += 1

    project_id_choose = found_projects_id[int(input("Enter mod number > "))]
    mod_versions_id = modrinth.get_project_versions_by_id(project_id_choose)

    version_count = 0
    for mod_version_id in mod_versions_id:
        print(f"{version_count}. {modrinth.get_version_name_by_id(mod_version_id)}")
        version_count += 1

    version_choose = input("Enter version number. Left blank for latest >")
    if version_choose == '':
        version_id_choose = mod_versions_id[0]
    else:
        version_id_choose = mod_versions_id[int(version_choose)]

    print(f"Downloading {modrinth.get_primary_version_filename_by_id(version_id_choose)}")
    with open(modrinth.get_primary_version_filename_by_id(version_id_choose), 'wb') as modfile:
        file = r.get(modrinth.get_primary_version_file_url_by_id(version_id_choose)).content
        modfile.write(file)
