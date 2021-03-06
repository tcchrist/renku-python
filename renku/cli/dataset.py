# -*- coding: utf-8 -*-
#
# Copyright 2017-2020 - Swiss Data Science Center (SDSC)
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
r"""Renku CLI commands for handling of datasets.

Manipulating datasets
~~~~~~~~~~~~~~~~~~~~~

Creating an empty dataset inside a Renku project:

.. code-block:: console

    $ renku dataset create my-dataset
    Creating a dataset ... OK

You can pass the following options to this command to set various metadata for
the dataset.

+-------------------+------------------------------------------------------+
| Option            | Description                                          |
+===================+======================================================+
| -t, --title       | A human-readable title for the dataset.              |
+-------------------+------------------------------------------------------+
| -d, --description | Dataset's description.                               |
+-------------------+------------------------------------------------------+
| -c, --creator     | Creator's name, email, and an optional affiliation.  |
|                   | Accepted format is                                   |
|                   | 'Forename Surname <email> [affiliation]'. Pass       |
|                   | multiple times for a list of creators.               |
+-------------------+------------------------------------------------------+
| -k, --keyword     | Dataset's keywords. Pass multiple times for a list   |
|                   | of keywords.                                         |
+-------------------+------------------------------------------------------+

Editing a dataset's metadata

Use ``edit`` subcommand to change metadata of a dataset. You can edit the same
set of metadata as the create command by passing the options described in the
table above.

.. code-block:: console

    $ renku dataset edit my-dataset --title 'New title'
    Successfully updated: title.

Listing all datasets:

.. code-block:: console

    $ renku dataset ls
    ID        NAME           TITLE          VERSION
    --------  -------------  -------------  ---------
    0ad1cb9a  some-dataset   Some Dataset
    9436e36c  my-dataset     My Dataset

You can select which columns to display by using ``--columns`` to pass a
comma-separated list of column names:

.. code-block:: console

    $ renku dataset ls --columns id,name,date_created,creators
    ID        NAME           CREATED              CREATORS
    --------  -------------  -------------------  ---------
    0ad1cb9a  some-dataset   2020-03-19 16:39:46  sam
    9436e36c  my-dataset     2020-02-28 16:48:09  sam

Displayed results are sorted based on the value of the first column.

To inspect the state of the dataset on a given commit we can use ``--revision``
flag for it:

.. code-block:: console

    $ renku dataset ls --revision=1103a42bd3006c94efcaf5d6a5e03a335f071215
    ID        NAME                 TITLE               VERSION
    a1fd8ce2  201901_us_flights_1  2019-01 US Flights  1
    c2d80abe  ds1                  ds1


Deleting a dataset:

.. code-block:: console

    $ renku dataset rm some-dataset
    OK


Working with data
~~~~~~~~~~~~~~~~~


Adding data to the dataset:

.. code-block:: console

    $ renku dataset add my-dataset http://data-url

This will copy the contents of ``data-url`` to the dataset and add it
to the dataset metadata.

You can create a dataset when you add data to it for the first time by passing
``--create`` flag to add command:

.. code-block:: console

    $ renku dataset add --create new-dataset http://data-url

To add data from a git repository, you can specify it via https or git+ssh
URL schemes. For example,

.. code-block:: console

    $ renku dataset add my-dataset git+ssh://host.io/namespace/project.git

Sometimes you want to add just specific paths within the parent project.
In this case, use the ``--source`` or ``-s`` flag:

.. code-block:: console

    $ renku dataset add my-dataset --source path/within/repo/to/datafile \
        git+ssh://host.io/namespace/project.git

The command above will result in a structure like

.. code-block:: console

    data/
      my-dataset/
        datafile

You can use shell-like wildcards (e.g. *, **, ?) when specifying paths to be
added. Put wildcard patterns in quotes to prevent your shell from expanding
them.

.. code-block:: console

    $ renku dataset add my-dataset --source 'path/**/datafile' \
        git+ssh://host.io/namespace/project.git

You can use ``--destination`` or ``-d`` flag to set the location where the new
data is copied to. This location be will under the dataset's data directory and
will be created if does not exists. You will get an error message if the
destination exists and is a file.

.. code-block:: console

    $ renku dataset add my-dataset \
        --source path/within/repo/to/datafile \
        --destination new-dir/new-subdir \
        git+ssh://host.io/namespace/project.git

will yield:

.. code-block:: console

    data/
      my-dataset/
        new-dir/
          new-subdir/
            datafile

To add a specific version of files, use ``--ref`` option for selecting a
branch, commit, or tag. The value passed to this option must be a valid
reference in the remote Git repository.

Adding external data to the dataset:

Sometimes you might want to add data to your dataset without copying the
actual files to your repository. This is useful for example when external data
is too large to store locally. The external data must exist (i.e. be mounted)
on your filesystem. Renku creates a symbolic to your data and you can use this
symbolic link in renku commands as a normal file. To add an external file pass
``--external`` or ``-e`` when adding local data to a dataset:

.. code-block:: console

    $ renku dataset add my-dataset -e /path/to/external/file

Updating a dataset:

After adding files from a remote Git repository or importing a dataset from a
provider like Dataverse or Zenodo, you can check for updates in those files by
using ``renku dataset update`` command. For Git repositories, this command
checks all remote files and copies over new content if there is any. It does
not delete files from the local dataset if they are deleted from the remote Git
repository; to force the delete use ``--delete`` argument. You can update to a
specific branch, commit, or tag by passing ``--ref`` option.
For datasets from providers like Dataverse or Zenodo, the whole dataset is
updated to ensure consistency between the remote and local versions. Due to
this limitation, the ``--include`` and ``--exclude`` flags are not compatible
with those datasets. Modifying those datasets locally will prevent them from
being updated.

You can limit the scope of updated files by specifying dataset names, using
``--include`` and ``--exclude`` to filter based on file names, or using
``--creators`` to filter based on creators. For example, the following command
updates only CSV files from ``my-dataset``:

.. code-block:: console

    $ renku dataset update -I '*.csv' my-dataset

Note that putting glob patterns in quotes is needed to tell Unix shell not
to expand them.

External data are not updated automatically because they require a checksum
calculation which can take a long time when data is large. To update external
files pass ``--external`` or ``-e`` to the update command:

.. code-block:: console

    $ renku dataset update -e

Tagging a dataset:

A dataset can be tagged with an arbitrary tag to refer to the dataset at that
point in time. A tag can be added like this:

.. code-block:: console

    $ renku dataset tag my-dataset 1.0 -d "Version 1.0 tag"

A list of all tags can be seen by running:

.. code-block:: console

    $ renku dataset ls-tags my-dataset
    CREATED              NAME    DESCRIPTION      DATASET     COMMIT
    -------------------  ------  ---------------  ----------  ----------------
    2020-09-19 17:29:13  1.0     Version 1.0 tag  my-dataset  6c19a8d31545b...


A tag can be removed with:

.. code-block:: console

    $ renku dataset rm-tags my-dataset 1.0


Importing data from other Renku projects:

To import all data files and their metadata from another Renku dataset use:

.. code-block:: console

    $ renku dataset import \
        https://renkulab.io/projects/<username>/<project>/datasets/<dataset-id>

or

.. code-block:: console

    $ renku dataset import \
        https://renkulab.io/datasets/<dataset-id>

You can get the link to a dataset form the UI or you can construct it by
knowing the dataset's ID.


Importing data from an external provider:

.. code-block:: console

    $ renku dataset import 10.5281/zenodo.3352150

This will import the dataset with the DOI (Digital Object Identifier)
``10.5281/zenodo.3352150`` and make it locally available.
Dataverse and Zenodo are supported, with DOIs (e.g. ``10.5281/zenodo.3352150``
or ``doi:10.5281/zenodo.3352150``) and full URLs (e.g.
``http://zenodo.org/record/3352150``). A tag with the remote version of the
dataset is automatically created.

Exporting data to an external provider:

.. code-block:: console

    $ renku dataset export my-dataset zenodo

This will export the dataset ``my-dataset`` to ``zenodo.org`` as a draft,
allowing for publication later on. If the dataset has any tags set, you
can chose if the repository `HEAD` version or one of the tags should be
exported. The remote version will be set to the local tag that is being
exported.

To export to a Dataverse provider you must pass Dataverse server's URL and
the name of the parent dataverse where the dataset will be exported to.
Server's URL is stored in your Renku setting and you don't need to pass it
every time.


Listing all files in the project associated with a dataset.

.. code-block:: console

    $ renku dataset ls-files
    DATASET NAME         ADDED                PATH                           LFS
    -------------------  -------------------  -----------------------------  ----
    my-dataset           2020-02-28 16:48:09  data/my-dataset/addme          *
    my-dataset           2020-02-28 16:49:02  data/my-dataset/weather/file1  *
    my-dataset           2020-02-28 16:49:02  data/my-dataset/weather/file2
    my-dataset           2020-02-28 16:49:02  data/my-dataset/weather/file3  *

You can select which columns to display by using ``--columns`` to pass a
comma-separated list of column names:

.. code-block:: console

    $ renku dataset ls-files --columns name,creators, path
    DATASET NAME         CREATORS   PATH
    -------------------  ---------  -----------------------------
    my-dataset           sam        data/my-dataset/addme
    my-dataset           sam        data/my-dataset/weather/file1
    my-dataset           sam        data/my-dataset/weather/file2
    my-dataset           sam        data/my-dataset/weather/file3

Displayed results are sorted based on the value of the first column.

Sometimes you want to filter the files. For this we use ``--dataset``,
``--include`` and ``--exclude`` flags:

.. code-block:: console

    $ renku dataset ls-files --include "file*" --exclude "file3"
    DATASET NAME        ADDED                PATH                           LFS
    ------------------- -------------------  -----------------------------  ----
    my-dataset          2020-02-28 16:49:02  data/my-dataset/weather/file1  *
    my-dataset          2020-02-28 16:49:02  data/my-dataset/weather/file2  *

Unlink a file from a dataset:

.. code-block:: console

    $ renku dataset unlink my-dataset --include file1
    OK

Unlink all files within a directory from a dataset:

.. code-block:: console

    $ renku dataset unlink my-dataset --include "weather/*"
    OK

Unlink all files from a dataset:

.. code-block:: console

    $ renku dataset unlink my-dataset
    Warning: You are about to remove following from "my-dataset" dataset.
    .../my-dataset/weather/file1
    .../my-dataset/weather/file2
    .../my-dataset/weather/file3
    Do you wish to continue? [y/N]:

.. note:: The ``unlink`` command does not delete files,
    only the dataset record.
"""
from functools import partial

import click
import requests
from tqdm import tqdm

from renku.core.commands.dataset import (
    add_file,
    create_dataset,
    dataset_remove,
    edit_dataset,
    export_dataset,
    file_unlink,
    import_dataset,
    list_datasets,
    list_files,
    list_tags,
    remove_dataset_tags,
    tag_dataset_with_client,
    update_datasets,
)
from renku.core.commands.echo import WARNING, progressbar
from renku.core.commands.format.dataset_files import DATASET_FILES_COLUMNS, DATASET_FILES_FORMATS
from renku.core.commands.format.dataset_tags import DATASET_TAGS_FORMATS
from renku.core.commands.format.datasets import DATASETS_COLUMNS, DATASETS_FORMATS
from renku.core.errors import DatasetNotFound, InvalidAccessToken
from renku.core.management.datasets import DownloadProgressCallback


def prompt_access_token(exporter):
    """Prompt user for an access token for a provider.

    :return: The new access token
    """
    text_prompt = "You must configure an access token\n"
    text_prompt += "Create one at: {0}\n".format(exporter.access_token_url())
    text_prompt += "Access token"

    return click.prompt(text_prompt, type=str)


def prompt_tag_selection(tags):
    """Prompt user to chose a tag or <HEAD>."""
    # Prompt user to select a tag to export
    tags = sorted(tags, key=lambda t: t.created)

    text_prompt = "Tag to export: \n\n<HEAD>\t[1]\n"

    text_prompt += "\n".join("{}\t[{}]".format(t.name, i) for i, t in enumerate(tags, start=2))

    text_prompt += "\n\nTag"
    selection = click.prompt(text_prompt, type=click.IntRange(1, len(tags) + 1), default=1)

    if selection > 1:
        return tags[selection - 2]
    return None


@click.group()
def dataset():
    """Dataset commands."""
    pass


@dataset.command("ls")
@click.option("--revision", default=None)
@click.option("--format", type=click.Choice(DATASETS_FORMATS), default="tabular", help="Choose an output format.")
@click.option(
    "-c",
    "--columns",
    type=click.STRING,
    default="id,name,title,version",
    metavar="<columns>",
    help="Comma-separated list of column to display: {}.".format(", ".join(DATASETS_COLUMNS.keys())),
    show_default=True,
)
@click.pass_context
def list_dataset(ctx, revision, format, columns):
    """Handle datasets."""
    click.echo(list_datasets(revision=revision, format=format, columns=columns))


@dataset.command()
@click.argument("name")
@click.option("-t", "--title", default=None, type=click.STRING, help="Title of the dataset.")
@click.option("-d", "--description", default=None, type=click.STRING, help="Dataset's description.")
@click.option(
    "-c",
    "--creator",
    "creators",
    default=None,
    multiple=True,
    help="Creator's name, email, and affiliation. " "Accepted format is 'Forename Surname <email> [affiliation]'.",
)
@click.option("-k", "--keyword", default=None, multiple=True, type=click.STRING, help="List of keywords or tags.")
def create(name, title, description, creators, keyword):
    """Create an empty dataset in the current repo."""
    creators = creators or ()

    new_dataset = create_dataset(name=name, title=title, description=description, creators=creators, keywords=keyword,)

    click.echo(f'Use the name "{new_dataset.name}" to refer to this dataset.')
    click.secho("OK", fg="green")


@dataset.command()
@click.argument("name")
@click.option("-t", "--title", default=None, type=click.STRING, help="Title of the dataset.")
@click.option("-d", "--description", default=None, type=click.STRING, help="Dataset's description.")
@click.option(
    "-c",
    "--creator",
    "creators",
    default=None,
    multiple=True,
    help="Creator's name, email, and affiliation. " "Accepted format is 'Forename Surname <email> [affiliation]'.",
)
@click.option("-k", "--keyword", default=None, multiple=True, type=click.STRING, help="List of keywords or tags.")
def edit(name, title, description, creators, keyword):
    """Edit dataset metadata."""
    creators = creators or ()
    keywords = keyword or ()

    updated, no_email_warnings = edit_dataset(
        name=name, title=title, description=description, creators=creators, keywords=keywords,
    )

    if not updated:
        click.echo(
            (
                "Nothing to update. "
                "Check available fields with `renku dataset edit --help`\n\n"
                'Hint: `renku dataset edit --title "new title"`'
            )
        )
    else:
        click.echo("Successfully updated: {}.".format(", ".join(updated)))
        if no_email_warnings:
            click.echo(WARNING + "No email or wrong format for: " + ", ".join(no_email_warnings))


@dataset.command()
@click.argument("name")
@click.argument("urls", nargs=-1)
@click.option("-e", "--external", is_flag=True, help="Creates a link to external data.")
@click.option("--force", is_flag=True, help="Allow adding otherwise ignored files.")
@click.option("-o", "--overwrite", is_flag=True, help="Overwrite existing files.")
@click.option("-c", "--create", is_flag=True, help="Create dataset if it does not exist.")
@click.option(
    "-s", "--src", "--source", "sources", default=None, multiple=True, help="Path(s) within remote git repo to be added"
)
@click.option(
    "-d",
    "--dst",
    "--destination",
    "destination",
    default="",
    help="Destination file or directory within the dataset path",
)
@click.option("--ref", default=None, help="Add files from a specific commit/tag/branch.")
def add(name, urls, external, force, overwrite, create, sources, destination, ref):
    """Add data to a dataset."""
    progress = partial(progressbar, label="Adding data to dataset")
    add_file(
        urls=urls,
        name=name,
        external=external,
        force=force,
        overwrite=overwrite,
        create=create,
        sources=sources,
        destination=destination,
        ref=ref,
        urlscontext=progress,
        progress=_DownloadProgressbar,
        interactive=True,
    )
    click.secho("OK", fg="green")


@dataset.command("ls-files")
@click.argument("names", nargs=-1)
@click.option(
    "--creators",
    help="Filter files which where authored by specific creators. " "Multiple creators are specified by comma.",
)
@click.option("-I", "--include", default=None, multiple=True, help="Include files matching given pattern.")
@click.option("-X", "--exclude", default=None, multiple=True, help="Exclude files matching given pattern.")
@click.option("--format", type=click.Choice(DATASET_FILES_FORMATS), default="tabular", help="Choose an output format.")
@click.option(
    "-c",
    "--columns",
    type=click.STRING,
    default="dataset_name,added,size,path,lfs",
    metavar="<columns>",
    help="Comma-separated list of column to display: {}.".format(", ".join(DATASET_FILES_COLUMNS.keys())),
    show_default=True,
)
def ls_files(names, creators, include, exclude, format, columns):
    """List files in dataset."""
    click.echo(list_files(names, creators, include, exclude, format, columns))


@dataset.command()
@click.argument("name")
@click.option("-I", "--include", multiple=True, help="Include files matching given pattern.")
@click.option("-X", "--exclude", multiple=True, help="Exclude files matching given pattern.")
@click.option("-y", "--yes", is_flag=True, help="Confirm unlinking of all files.")
def unlink(name, include, exclude, yes):
    """Remove matching files from a dataset."""
    file_unlink(name=name, include=include, exclude=exclude, yes=yes, interactive=True)

    click.secho("OK", fg="green")


@dataset.command("rm")
@click.argument("name")
def remove(name):
    """Delete a dataset."""
    dataset_remove(name)
    click.secho("OK", fg="green")


@dataset.command("tag")
@click.argument("name")
@click.argument("tag")
@click.option("-d", "--description", default="", help="A description for this tag")
@click.option("--force", is_flag=True, help="Allow overwriting existing tags.")
def tag(name, tag, description, force):
    """Create a tag for a dataset."""
    tag_dataset_with_client(name, tag, description, force)
    click.secho("OK", fg="green")


@dataset.command("rm-tags")
@click.argument("name")
@click.argument("tags", nargs=-1)
def remove_tags(name, tags):
    """Remove tags from a dataset."""
    remove_dataset_tags(name, tags)
    click.secho("OK", fg="green")


@dataset.command("ls-tags")
@click.argument("name")
@click.option("--format", type=click.Choice(DATASET_TAGS_FORMATS), default="tabular", help="Choose an output format.")
def ls_tags(name, format):
    """List all tags of a dataset."""
    tags_output = list_tags(name, format)
    click.echo(tags_output)


@dataset.command("export")
@click.argument("name")
@click.argument("provider")
@click.option("-p", "--publish", is_flag=True, help="Automatically publish exported dataset.")
@click.option("-t", "--tag", help="Dataset tag to export")
@click.option("--dataverse-server", default=None, help="Dataverse server URL.")
@click.option("--dataverse-name", default=None, help="Dataverse name to export to.")
def export_(name, provider, publish, tag, dataverse_server, dataverse_name):
    """Export data to 3rd party provider."""
    try:
        output = export_dataset(
            name=name,
            provider=provider,
            publish=publish,
            tag=tag,
            handle_access_token_fn=prompt_access_token,
            handle_tag_selection_fn=prompt_tag_selection,
            dataverse_server_url=dataverse_server,
            dataverse_name=dataverse_name,
        )
    except (ValueError, InvalidAccessToken, DatasetNotFound, requests.HTTPError) as e:
        raise click.BadParameter(e)

    click.echo(output)
    click.secho("OK", fg="green")


@dataset.command("import")
@click.argument("uri")
@click.option("--short-name", "--name", "name", default=None, help="A convenient name for dataset.")
@click.option("-x", "--extract", is_flag=True, help="Extract files before importing to dataset.")
@click.option("-y", "--yes", is_flag=True, help="Bypass download confirmation.")
def import_(uri, name, extract, yes):
    """Import data from a 3rd party provider or another renku project.

    Supported providers: [Dataverse, Renku, Zenodo]
    """
    import_dataset(uri=uri, name=name, extract=extract, with_prompt=True, yes=yes, progress=_DownloadProgressbar)
    click.secho(" " * 79 + "\r", nl=False)
    click.secho("OK", fg="green")


class _DownloadProgressbar(DownloadProgressCallback):
    def __init__(self, description, total_size):
        """Default initializer."""
        self._progressbar = tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            desc=description,
            leave=False,
            bar_format="{desc:.32}: {percentage:3.0f}%|{bar}{r_bar}",
        )

    def update(self, size):
        """Update the status."""
        if self._progressbar:
            self._progressbar.update(size)

    def finalize(self):
        """Called once when the download is finished."""
        if self._progressbar:
            self._progressbar.close()


@dataset.command("update")
@click.argument("names", nargs=-1)
@click.option(
    "--creators",
    help="Filter files which where authored by specific creators. " "Multiple creators are specified by comma.",
)
@click.option("-I", "--include", default=None, multiple=True, help="Include files matching given pattern.")
@click.option("-X", "--exclude", default=None, multiple=True, help="Exclude files matching given pattern.")
@click.option("--ref", default=None, help="Update to a specific commit/tag/branch.")
@click.option("--delete", is_flag=True, help="Delete local files that are deleted from remote.")
@click.option("-e", "--external", is_flag=True, help="Update external data.")
def update(names, creators, include, exclude, ref, delete, external):
    """Updates files in dataset from a remote Git repo."""
    progress_context = partial(progressbar, label="Checking files for updates")
    update_datasets(
        names=list(names),
        creators=creators,
        include=include,
        exclude=exclude,
        ref=ref,
        delete=delete,
        external=external,
        progress_context=progress_context,
    )
    click.secho("OK", fg="green")
