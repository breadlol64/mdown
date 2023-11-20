import requests as r

api = "https://api.modrinth.com/v2"
session = r.Session()


def search_projects(query: str) -> list:
    response = session.get(f"{api}/search?query={query}").json()
    hits = response["hits"]
    project_ids = []

    for hit in hits:
        project_ids.append(hit["project_id"])

    return project_ids


def get_project_title_by_id(project_id: str) -> str:
    response = session.get(f"{api}/project/{project_id}").json()
    return response["title"]


def get_project_game_versions_by_id(project_id: str) -> list:
    response = session.get(f"{api}/project/{project_id}").json()
    return response["game_versions"]


def get_project_loaders_by_id(project_id: str) -> list:
    response = session.get(f"{api}/project/{project_id}").json()
    return response["loaders"]


def get_project_versions_by_id(project_id: str, featured: str = "false") -> list:
    response = session.get(f"{api}/project/{project_id}/version?featured={featured}").json()
    versions_id = []
    for version in response:
        versions_id.append(version["id"])

    return versions_id


def get_version_name_by_id(version_id: str) -> str:
    response = session.get(f"{api}/version/{version_id}").json()
    return response["name"]


def get_primary_version_filename_by_id(version_id: str) -> str:
    response = session.get(f"{api}/version/{version_id}").json()
    files = response["files"]
    for file in files:
        if file["primary"]:
            return file["filename"]


def get_primary_version_file_url_by_id(version_id: str) -> str:
    response = session.get(f"{api}/version/{version_id}").json()
    files = response["files"]
    for file in files:
        if file["primary"]:
            return file["url"]
