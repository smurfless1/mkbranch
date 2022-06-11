import json

from invoke import task

@task
def publish(c):
    token = get_field(c, "Github", "api token for goreleaser").strip()
    c.run(f'GITHUB_TOKEN="{token}" goreleaser release')

@task
def build_only_local_platform(c):
    c.run("goreleaser build --single-target --rm-dist")

@task
def tag(c, version):
    c.run(f"git tag v{version}")
    c.run(f"git push origin v{version}")


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

