import json
import semver

from pathlib import Path
from invoke import task


@task
def brew(c):
    if not Path("/opt/homebrew/bin/brew").exists():
        c.run("open https://brew.sh/")
        print("You have to install homebrew now, which involves a shell restart.")
        raise SyntaxError("User needs to install homebrew")


@task
def op(c):
    if not Path("/usr/local/bin/op").exists():
        c.run("brew install 1password-cli")

def get_field(c, name, field):
    c: Context
    result = c.run(f'op item get "{name}" --field label="{field}"', hide='both')
    return result.stdout.strip()


def get_username(c, name):
    c: Context
    result = c.run(f'op item get "{name}" --field label="username"', hide='both')
    return result.stdout.strip()


def get_password(c, name):
    c: Context
    result = c.run(f'op item get "{name}" --field label="password"', hide='both')
    return result.stdout.strip()


def get_otp(c, name):
    c: Context
    result = c.run(f'op item get "{name}" --otp', hide='both')
    return result.stdout.strip()


@task
def build_only_local_platform(c):
    c.run("goreleaser build --single-target --rm-dist")


@task(op)
def prepublish(c):
    """Publish a prerelease"""
    token = get_field(c, "Github", "api token for goreleaser").strip()
    c.run(f'GITHUB_TOKEN="{token}" goreleaser release --snapshot --rm-dist')


@task(op)
def publish(c):
    """Publish the latest tag"""
    c.run(f"git push --follow-tags")
    token = get_field(c, "Github", "api token for goreleaser").strip()
    c.run(f'GITHUB_TOKEN="{token}" goreleaser release --rm-dist')
    # part 2: npm - update version, get OTP to clipboard, publish
    code = get_otp(c, "NPM registry")
    c.run(f'npm publish --otp {code}')


def read_version():
    with Path("package.json").open("r", encoding='utf-8') as pjhandle:
        loaded = json.load(pjhandle)
    # does not include the v
    return loaded['version']


def write_version(version):
    with Path("package.json").open("r", encoding='utf-8') as pjhandle:
        loaded = json.load(pjhandle)
        loaded['version'] = version
    with Path("package.json").open("w", encoding='utf-8') as pjhandle:
        pjhandle.write(json.dumps(loaded, indent=4))


@task
def update_pj(c, version):
    write_version(version)
    c.run(f"git add package.json ; git commit -m 'Update version to v{version}'")


@task
def tag(c, version):
    """State a release version"""
    update_pj(c, version)
    c.run(f"git tag -a v{version} -m 'Version v{version}'")


@task
def bump_patch(c):
    ver = semver.VersionInfo.parse(read_version())
    updated = str(ver.bump_patch())
    # reminder: no v on the semver here
    tag(c, updated)


@task(op)
def op_check(c):
    """Fail fast on a stale 1password login"""
    try:
        get_otp(c, "NPM registry")
    except:
        c.run("1password-login")


@task(op_check, bump_patch, publish)
def ship_patch(c):
    """Bump a patch and release it."""
    pass
