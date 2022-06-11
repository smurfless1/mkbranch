import json

from pathlib import Path
from invoke import task

@task
def prepublish(c):
    """Publish a prerelease"""
    token = get_field(c, "Github", "api token for goreleaser").strip()
    c.run(f'GITHUB_TOKEN="{token}" goreleaser release --snapshot --rm-dist')


@task
def publish(c):
    """Publish the latest tag"""
    c.run(f"git push --follow-tags")
    token = get_field(c, "Github", "api token for goreleaser").strip()
    c.run(f'GITHUB_TOKEN="{token}" goreleaser release --rm-dist')
    # part 2: npm - update version, get OTP to clipboard, publish
    c.run('op item get "NPM registry" --otp | pbcopy')
    c.run('npm publish')  # user has to paste for now


@task
def build_only_local_platform(c):
    c.run("goreleaser build --single-target --rm-dist")


@task
def update_pj(c, version):
    with Path("package.json").open("r", encoding='utf-8') as pjhandle:
        loaded = json.load(pjhandle)
        loaded['version'] = version
    with Path("package.json").open("w", encoding='utf-8') as pjhandle:
        pjhandle.write(json.dumps(loaded, indent=4))
    c.run(f"git add package.json ; git commit -m 'Update npm version to v{version}'")


@task
def tag(c, version):
    """State a release version"""
    update_pj(c, version)
    c.run(f"git tag -a v{version} -m 'Version v{version}'")


def get_field(c, name, field):
    c: Context
    result = c.run(f'op item get "{name}" --field label="{field}"', hide='both')
    return result.stdout


def get_username(c, name):
    c: Context
    result = c.run(f'op item get "{name}" --field label="username"', hide='both')
    return result.stdout


def get_password(c, name):
    c: Context
    result = c.run(f'op item get "{name}" --field label="password"', hide='both')
    return result.stdout


def get_otp(c, name):
    c: Context
    result = c.run(f'op item get "{name}" --otp', hide='both')
    return result.stdout

