# -*- coding: utf-8 -*-
#
# Copyright 2018 - Swiss Data Science Center (SDSC)
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
"""Represent a ``Process`` from the Common Workflow Language."""

import attr


@attr.s(init=False)
class Process(object):
    """Represent a process."""

    inputs = attr.ib(default=attr.Factory(list))  # list InputParameter
    outputs = attr.ib(default=attr.Factory(list))  # list OutputParameter
    requirements = attr.ib(default=attr.Factory(list))
    # list ProcessRequirement
    hints = attr.ib(default=attr.Factory(list))  # list Any
    label = attr.ib(default=None)  # str
    doc = attr.ib(default=None)  # str
    cwlVersion = attr.ib(default='v1.0')  # derive from a parent
