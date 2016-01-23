from fabric.api import *
import fabric.contrib.project as project
import datetime
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import sys
import SocketServer

from pelican.server import ComplexHTTPRequestHandler

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'

# Github Pages configuration
env.github_pages_branch = "gh-pages"

# Port for `serve`
PORT = 8000

def article(title, output_file = "content/posts/{}.rst", template = "templates/blogs/articles.rst", slug = None, overwrite = False, *tags, **kvPairs):
    now = datetime.datetime.now()
    month = now.strftime("%Y-%m")
    post_date = now.strftime("%Y-%m-%d")

    params = {
        "date": post_date,
        "title": title,
        "slug": slug
    }

    if tags is not None:
        for index, tag in enumerate(tags, start = 1):
            key = "tag". index
            params[key] = tag

    if kvPairs is not None:
        for k, v in kvPairs.iteritems():
            params[k] = v

    resolved_file = output_file.format(slug)
    local("mkdir -p '{}'".format( os.path.dirname(resolved_file) ))
    if not os.path.exists(resolved_file) or overwrite:
        render(template, resolved_file, **params)
    else:
        print("{} already exists". format(resolved_file))


def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)

def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')

def rebuild():
    """`clean` then `build`"""
    clean()
    build()

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -r -s pelicanconf.py')

def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')

def cf_upload():
    """Publish to Rackspace Cloud Files"""
    rebuild()
    with lcd(DEPLOY_PATH):
        local('swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
              '-U {cloudfiles_username} '
              '-K {cloudfiles_api_key} '
              'upload -c {cloudfiles_container} .'.format(**env))

@hosts(production)
def publish():
    """Publish to production via rsync"""
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        extra_opts='-c',
    )

def gh_pages():
    """Publish to GitHub Pages"""
    rebuild()
    local("ghp-import -b {github_pages_branch} {deploy_path}".format(**env))
    local("git push origin {github_pages_branch}".format(**env))

def render(template, resolved_file, **params):
    jenv = Environment(loader = FileSystemLoader(['.', template]) )
    file_content = jenv.get_template(template).render(params)
    with open(resolved_file, "w") as output:
        puts("Rendering {} to {}".format(template, resolved_file))
        output.write(file_content.encode("UTF-8"))
