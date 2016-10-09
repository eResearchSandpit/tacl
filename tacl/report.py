import os.path
import shutil

from jinja2 import Environment, PackageLoader
from pkg_resources import resource_filename, resource_listdir


class Report:

    """Base class for HTML reports."""

    _report_name = ''

    def _copy_static_assets(self, output_dir):
        """Copy assets for the report to `output_dir`.

        :param output_dir: directory to output assets to
        :type output_dir: `str`

        """
        base_directory = 'assets/{}'.format(self._report_name)
        for asset in resource_listdir(__name__, base_directory):
            filename = resource_filename(
                __name__, '{}/{}'.format(base_directory, asset))
            shutil.copy2(filename, output_dir)

    def generate(self, output_dir):
        """Generate the report, writing it to `output_dir`."""
        raise NotImplementedError

    def _get_template(self):
        """Returns a template for this report.

        :rtype: `jinja2.Template`

        """
        loader = PackageLoader('tacl', 'assets/templates')
        env = Environment(loader=loader)
        return env.get_template('{}.html'.format(self._report_name))

    def _write(self, context, report_dir, report_file, assets_dir=None):
        """Writes the data in `context` in the report's template to
        `report_file` in `report_dir`.

        If `assets_dir` is supplied, copies all assets for this report
        to the specified directory.

        :param context: context data to render within the template
        :type context: `dict`
        :param report_dir: directory to write the report to
        :type report_dir: `str`
        :param report_file: file to write the report to
        :type report_file: `str`
        :assets_dir: optional directory to output report assets to
        :type assets_dir: `str`

        """
        template = self._get_template()
        report = template.render(context)
        with open(os.path.join(report_dir, report_file), 'w') as fh:
            fh.write(report)
        if assets_dir:
            self._copy_static_assets(assets_dir)
