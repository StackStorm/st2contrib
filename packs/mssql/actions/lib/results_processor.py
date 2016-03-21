from _mssql import ROW_FORMAT_DICT
from tempfile import NamedTemporaryFile
import csv
import os
import sys

__all__ = [
    'ResultsProcessor'
]


# noinspection PyUnusedLocal
# noinspection PyMethodMayBeStaticInspection
class ResultsProcessor(object):
    """
    Utility for processing action response, e.g. changing returned results or passing data via disk
    """

    NO_DATA = 2

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def execute_scalar(self, response, cursor):
        """
        Returns the scalar response.
        """
        if not response:
            sys.exit(self.NO_DATA)
        return response

    def execute_row(self, response, cursor):
        """
        Returns a mapping of column name to value for a row.
        """
        row = self._filter_numbered_columns(response or {})
        if not row:
            sys.exit(self.NO_DATA)
        return row

    def execute_insert(self, response, cursor):
        """
        Returns identity value of the inserted row.
        """
        return cursor.identity

    def execute_non_query(self, response, cursor):
        """
        Returns the number of rows affected by the non-query.
        """
        if cursor.rows_affected == 0:
            sys.exit(self.NO_DATA)
        return cursor.rows_affected

    def execute_query(self, response, cursor):
        """
        Writes results to CSV for downstream processing. Each result set is written to its own file.
        Returns a list of all file names in order of result set for use by downstream actions.

        Checks `output_csv` section in `config.yaml` to determine where to write CSV files. You can
        specify the output `directory` as well as the file `prefix` and `suffix`.

        Tries writing to `$TMPDIR`, `$TEMP`, and `$TMP` in order before falling back to platform-
        specific locations. See https://docs.python.org/2/library/tempfile.html#tempfile.tempdir.
        """
        output_files = []
        while True:
            with self._get_output_file() as csv_file:
                # Since pythonrunner runs as root, only root can read and write CSV file by default
                # Let's chmod it so downstream processes which run as stanley can read and write
                os.chmod(csv_file.name, 0o666)  # race condition w/ open() OK since increasing perms
                try:
                    # Grab the first row so we can read the headers and write them to the CSV
                    first_row = self._filter_numbered_columns(
                        next(cursor.get_iterator(ROW_FORMAT_DICT)))
                except StopIteration:
                    # the last result set will always be empty, so remove the file created for it
                    os.unlink(csv_file.name)
                    # we're done, no more result sets
                    break
                output_files.append(csv_file.name)
                writer = csv.DictWriter(csv_file, fieldnames=first_row.keys())
                writer.writeheader()
                writer.writerow(first_row)
                for row in cursor:
                    writer.writerow(self._filter_numbered_columns(row))
        if not output_files:
            self.logger.info("Query returned no results, failing")
            sys.exit(self.NO_DATA)
        return {"output_files": output_files}

    def _filter_numbered_columns(self, row):
        """only return columns by name, not column number"""
        return {k: v for k, v in row.iteritems() if not isinstance(k, (int, long))}

    def _get_output_file(self, prefix='mssql-query.', suffix='.csv'):
        output_config = self.config.get('output_csv', {})
        return NamedTemporaryFile(
            dir=output_config.get('directory', None),
            prefix=output_config.get('output_prefix', prefix),
            suffix=output_config.get('output_suffix', suffix),
            delete=False)
