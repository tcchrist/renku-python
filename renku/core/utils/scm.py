# -*- coding: utf-8 -*-
#
# Copyright 2020 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Helpers utils for interacting with remote source code management tools."""
import re


def strip_and_lower(input):
    """Adjust chars to make the input compatible as scm source."""
    return re.sub(r"\s", r"-", input.strip()).lower()


def git_unicode_unescape(s, encoding="utf-8"):
    """Undoes git/gitpython unicode encoding."""
    if s.startswith('"'):
        return s.strip('"').encode("latin1").decode("unicode-escape").encode("latin1").decode(encoding)
    return s
