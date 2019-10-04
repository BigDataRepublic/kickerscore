from github import Github
from jinja2 import Template
import subprocess


def get_latest_git_hash():
    g = Github()
    repo = g.get_repo("BigDataRepublic/kickerscore")
    branch = repo.get_branch("master")
    commit = branch.commit

    return commit.sha


def render_deployment_yml(git_hash):
    with open('deployment.yml') as f:
        t = Template(f.read())

    rendered_template = t.render(git_hash=git_hash)

    with open('rendered_deployment.yml', 'w') as f:
        f.write(rendered_template)


def apply_deployment():
    subprocess.run(["kubectl", "apply", "-f", "rendered_deployment.yml"])


if __name__ == "__main__":
    git_hash = get_latest_git_hash()
    render_deployment_yml(git_hash)
    apply_deployment()
