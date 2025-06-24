#####################################################################################
# Requirement
# ----------------------------------------------------------------------------------#
# pip install PyGithub
#
# Create a new token with this link :
# https://github.com/settings/tokens
# classic token

from github import Github, GithubException

# ----------- Configuring the connexion to GitHub -----------#
# Replace by your personal token
GITHUB_TOKEN = "your_personal_token"

# Connection to GitHub
g = Github(GITHUB_TOKEN)

# ----------- Verifying the token -----------#
EXPECTED_USERNAME = "your_username_here"  # Your Github's username

try:
    user = g.get_user()
    if user.login.lower() != EXPECTED_USERNAME.lower():
        raise ValueError(
            f"Token valide mais associé à un autre utilisateur : {user.login}"
        )
    print(f"Token valide pour l'utilisateur : {user.login}")
except GithubException as e:
    print(f"Erreur d'authentification : {e.data.get('message', 'Inconnue')}")
    exit(1)

# ----------- Listing all of the deposits available -----------#
repos = g.get_user().get_repos()
print("\n--- Dépôts accessibles ---")
for repo in repos:
    print(f"{repo.id} - {repo.name} ({repo.full_name})")

# ----------- Inspect the content of a deposit -----------#
# Replace by the name of the content which you have the access
repo_full_name = "XXXX"

try:
    repo = g.get_repo(repo_full_name)
    branch = repo.default_branch
except GithubException as e:
    print(f"Erreur : dépôt introuvable ({repo_full_name}) : {e}")
    exit(1)


# ----------- Fonction of inspection of the content -----------#
def inspect_path(repo, type: str, ref: str, path: str = ""):
    try:
        if type == "file":
            file_content = repo.get_contents(path, ref)
            print(f"\n📄 Fichier : {file_content.path}")
            print(f"- Taille : {file_content.size} octets")
            print("- Encodage : base64")
            print(f"- Type MIME : {file_content.type}")
        elif type == "dir":
            contents = repo.get_contents(path, ref)
            print(f"\n📁 Contenu de {path or '/'} :")
            for content in contents:
                print(f"- {content.type} : {content.name} ({content.path})")
        else:
            raise ValueError("Type doit être 'file' ou 'dir'")
    except GithubException as e:
        print(f"Erreur d'accès à {path} : {e.data.get('message', 'Inconnue')}")


# ----------- Exploration simulation -----------#
inspect_path(repo, "dir", branch, "")

inspect_path(repo, "file", branch, "README.md")

# Dossier spécifique
inspect_path(repo, "dir", branch, "Data")

# Fichier dans un sous-dossier
inspect_path(repo, "file", branch, "Data/Example.zip")

# Dossier dans un sous-dossier
inspect_path(repo, "dir", branch, "docs/assets")