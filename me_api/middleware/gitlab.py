#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, jsonify, request, redirect

from me_api.cache import cache
from me_api.middleware.noneedauth import NoNeedAuthView
from me_api.middleware.utils import MiddlewareConfig, token_required, reject_duplicated_auth

import gitlab
import json

config = MiddlewareConfig('gitlab')
gitlab_api = Blueprint('gitlab', __name__, url_prefix=config.path)

api_version = config.api_version.strip('v')
url = config.url.rstrip('/')
access_token = config.access_token

if api_version is "":
    api_version = "4"
elif api_version != "4" and api_version != "3":
    raise(TypeError('GitLab API Version needs to be either "v4" or "v3"'))

if url is "":
    raise(TypeError('GitLab URL not defined!'))

if access_token is "":
    raise(TypeError('GitLab Access Token not defined!'))

gl = gitlab.Gitlab(url, access_token, api_version=api_version)
display_gl = {
         'api_version': gl.api_version,
         'version': gl.version()
        }

class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, gitlab.GitlabObject):
            return obj.as_dict()
        elif isinstance(obj, gitlab.Gitlab):
            return {'url': obj._url}
        return json.JSONEncoder.default(self, obj)

@gitlab_api.route('/')
@cache.cached(timeout=60*60)
@token_required(config)
def index():
    response = display_gl
    return jsonify(gitlab=response)

@gitlab_api.route('/projects')
@cache.cached(timeout=60*60)
@token_required(config)
def get_projects():
    projects = list()
    for project in gl.projects.list():
        projects.append(project._attrs)
    response = projects
    #response = json.dumps(projects, cls=jsonEncoder)
    return jsonify(gitlab=response)

@gitlab_api.route('/groups')
@cache.cached(timeout=60*60)
@token_required(config)
def get_groups():
    groups = list()
    for group in gl.groups.list():
        groups.append(group._attrs)
    response = groups
    return jsonify(gitlab=response)

@gitlab_api.route('/todos')
@cache.cached(timeout=60*60)
@token_required(config)
def get_todos():
    todos = list()
    for todo in gl.todos.list():
        todos.append(todo._attrs)
    response = todos
    return jsonify(gitlab=response)

@gitlab_api.route('/users')
@cache.cached(timeout=60*60)
@token_required(config)
def get_users():
    users = list()
    for user in gl.users.list():
        users.append(user._attrs)
    response = users
    return jsonify(gitlab=response)

@gitlab_api.route('/issues')
@cache.cached(timeout=60*60)
@token_required(config)
def get_issues():
    issues = list()
    for issue in gl.issues.list():
        issues.append(issue._attrs)
    response = issues
    return jsonify(gitlab=response)

