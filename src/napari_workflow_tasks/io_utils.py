# Need to create function to untar tar.gz files

import os
import tarfile
import tomllib
from pathlib import Path

class PackageImporter:
    """
    Takes in a tar.gz file and unzips it into the defined root_dir
    - Only untars pyproject.toml file and .py files
    """

    def __init__(
        self,
        root_dir=None
    ):
        if root_dir is None:
            self.root_dir = Path.home()
        elif isinstance(root_dir, str):
            self.root_dir = root_dir

        self.wf_dir = os.path.join(self.root_dir, '.napari_workflow_tasks')
        os.makedirs(self.wf_dir, exist_ok=True)

        self.loaded_packages = dict()

    # Register packages into dictionary here to keep track of what already exists
    # When closed, clean up the root dir (with del)

    def open_package(
        self,
        fpath
    ):
        """
        Get fpath to tar.gz file and untar specific files
        """

        file = tarfile.open(fpath)

        file.extractall(self.wf_dir)
        file.close()

        self.package_name = '.'.join(os.path.basename(fpath).split('.')[:-2])

        print(self.package_name)

        with open(os.path.join(self.wf_dir, self.package_name, 'pyproject.toml'), 'rb') as f:
            data = tomllib.load(f)

        src_path_ = data['tool']['hatch']['build']['targets']['wheel']['packages'][0]
        src_path = os.path.join(self.wf_dir, self.package_name, src_path_)
        manifest_path = os.path.join(src_path, '__FRACTAL_MANIFEST__.json')

        self.loaded_packages[self.package_name] = {'src_path': src_path, 'manifest_path': manifest_path}
