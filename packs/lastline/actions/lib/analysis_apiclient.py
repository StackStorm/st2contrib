#!/usr/bin/python
# flake8: noqa
# pylint: skip-file
"""
This is a Python client for the Lastline Analyst API.

The :py:class:`AnalysisClient` class implements
the client side of the Lastline Analyst API methods.
It can be imported into Python client code
that uses the API.

The client is available at
https://analysis.lastline.com/docs/llapi_client/analysis_apiclient.py.

Requirements
+++++++++++++++++++

The Analysis API client requires:

- python 2.6 or 2.7.
- The python requests module.
- The python pycurl module.
- To use the client as a python shell, the ipython module.

Required python modules can be installed
using tools such as easy_install or pip, e.g.::

    easy_install requests
    pip install ipython

Analysis Client Shell
+++++++++++++++++++++++

Running the analysis API client from the command line,
it provides a shell for manually sending requests
to the Lastline Analyst API. This can be used to
try out the API by analyzing files or URLs.

This is an IPython shell, so you can take
advantage of tab auto-completion and other
convenient features of IPython.

Once the shell is started, the current context
contains an 'analysis' object. This is an :py:class:`AnalysisClient`,
which can be used to access the functionality
of the lastline Analysis API.

To start the shell, invoke::

    python analysis_apiclient.py API_KEY API_TOKEN

replacing API_KEY and API_TOKEN with your API credentials.

By default, the client connects to an API instance running in the Lastline cloud
at https://analysis.lastline.com . To connect to a different instance, for
example when using a Lastline On-Premise installation, please use the
*--api-url* parameter to point to the URL of the On-Premise API. For example, to
connect to a Lastline Analyst On-Premise running at *analyst.lastline.local*,
use::

    python analysis_apiclient.py --api-url https://analyst.lastline.local/ API_KEY API_TOKEN

"""
import collections
import datetime
import sys
import time

try:
    import json
    import StringIO
    import requests
    if __name__ == "__main__":
        import optparse
        import IPython
except ImportError, e:
    if __name__ == "__main__":
        print >> sys.stderr, \
            "A module required for running the analysis API example \
            shell was not found:"
        print >> sys.stderr, "\t'%s'" % str(e)
        print >> sys.stderr, "Please install the missing module."
        print >> sys.stderr, "For this, you can use tools such as easy_install or pip:"
        print >> sys.stderr, "\t easy_install <MODULE_NAME>"
        print >> sys.stderr, "\t pip install <MODULE_NAME>"
        sys.exit(1)
    else:
        raise

try:
    from llapi_client import get_proxies_from_config
except ImportError:
    # Non-Lastline environment. Reading from config not support/needed.
    get_proxies_from_config = None

try:
    requests_version = requests.__version__
    if not requests_version.startswith('2.2'):
        raise Exception()
except Exception:
    requests_version = '?'
    print >> sys.stderr, "Warning: Your version of requests (%s) might not " \
                         "be compatible with this module." % requests_version
    print >> sys.stderr, "Officially supported are versions 2.2.x"


# copied these values from Lastline utility code (llapi) to make them available
# to users of client code. please keep in sync!
ANALYSIS_API_FILE_NOT_AVAILABLE = 101
ANALYSIS_API_UNKNOWN_RESOURCE_TYPE = 102
ANALYSIS_API_UNKNOWN_ANALYSIS_TYPE = 103
ANALYSIS_API_INVALID_CREDENTIALS = 104
ANALYSIS_API_INVALID_UUID = 105
ANALYSIS_API_NO_RESULT_FOUND = 106
ANALYSIS_API_TEMPORARILY_UNAVAILABLE = 107
ANALYSIS_API_PERMISSION_DENIED = 108
ANALYSIS_API_FILE_TOO_LARGE = 109
ANALYSIS_API_INVALID_DOMAIN = 110
ANALYSIS_API_INVALID_D_METADATA = 112
ANALYSIS_API_INVALID_FILE_TYPE = 113
ANALYSIS_API_INVALID_ARTIFACT_UUID = 114
ANALYSIS_API_SUBMISSION_LIMIT_EXCEEDED = 115
ANALYSIS_API_INVALID_HASH_ALGORITHM = 116
ANALYSIS_API_INVALID_URL = 117
ANALYSIS_API_INVALID_REPORT_VERSION = 118
ANALYSIS_API_FILE_EXTRACTION_FAILED = 119


class Error(Exception):
    """
    Base exception class for this module.
    """


class InvalidSubApiType(Error):
    """
    Exception for invalid sub API operations.

    The analysis API consists of a number of views (sub APIs):
    (only analysis for now)
    Operations involving parts other than these will
    raise this exceptions.
    """
    def __init__(self, sub_api_type):
        Error.__init__(self)
        self.sub_api_type = sub_api_type

    def __str__(self):
        return "Invalid sub API '%s', expecting one of (%s)" % \
            (self.sub_api_type, ','.join(AnalysisClientBase.SUB_APIS))


class InvalidFormat(Error):
    """
    Invalid format requested.
    """
    def __init__(self, requested_format):
        Error.__init__(self)
        self.format = requested_format

    def __str__(self):
        return "Requested Invalid Format '%s', expecting one of (%s)" % \
            (self.format, ','.join(AnalysisClientBase.FORMATS))


class CommunicationError(Error):
    """
    Contacting Malscape failed.
    """
    def __init__(self, msg=None, error=None):
        Error.__init__(self, msg or error or '')
        self.__error = error

    def internal_error(self):
        return self.__error


class InvalidAnalysisAPIResponse(Error):
    """
    An AnalysisAPI response was not in the expected format
    """


class AnalysisAPIError(Error):
    """
    Analysis API returned an error.

    The `error_code` member of this exception
    is the :ref:`error code returned by the API<error_codes>`.
    """
    def __init__(self, msg, error_code):
        Error.__init__(self)
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return "Analysis API error (%s): %s" % (self.error_code, self.msg)
        return "Analysis API error: %s" % self.msg


class RequestError(AnalysisAPIError):
    """
    Exception class to group errors that are permanent request errors when
    following the "malscape protocol". These errors indicate a problem with the
    request sent to the server - if you repeat the same request, you cannot
    expect a different error.

    This group excludes temporary errors, such as authentication problems.
    """


class SubmissionInvalidError(RequestError):
    """
    Exception class to group errors that are permanent submission errors. See
    `RequestError` for details.
    """


class FileNotAvailableError(AnalysisAPIError):
    def __init__(self, msg, error_code=ANALYSIS_API_FILE_NOT_AVAILABLE):
        AnalysisAPIError.__init__(self, msg, error_code)


class InvalidCredentialsError(AnalysisAPIError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_CREDENTIALS):
        AnalysisAPIError.__init__(self, msg, error_code)


class InvalidUUIDError(RequestError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_UUID):
        RequestError.__init__(self, msg, error_code)


class NoResultFoundError(AnalysisAPIError):
    def __init__(self, msg, error_code=ANALYSIS_API_NO_RESULT_FOUND):
        AnalysisAPIError.__init__(self, msg, error_code)


class TemporarilyUnavailableError(AnalysisAPIError):
    def __init__(self, msg, error_code=ANALYSIS_API_TEMPORARILY_UNAVAILABLE):
        AnalysisAPIError.__init__(self, msg, error_code)


class PermissionDeniedError(AnalysisAPIError):
    def __init__(self, msg, error_code=ANALYSIS_API_PERMISSION_DENIED):
        AnalysisAPIError.__init__(self, msg, error_code)


class FileTooLargeError(SubmissionInvalidError):
    def __init__(self, msg, error_code=ANALYSIS_API_FILE_TOO_LARGE):
        SubmissionInvalidError.__init__(self, msg, error_code)


class InvalidFileTypeError(SubmissionInvalidError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_FILE_TYPE):
        SubmissionInvalidError.__init__(self, msg, error_code)


class InvalidMetadataError(SubmissionInvalidError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_D_METADATA):
        SubmissionInvalidError.__init__(self, msg, error_code)


class InvalidArtifactError(RequestError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_ARTIFACT_UUID):
        RequestError.__init__(self, msg, error_code)


class SubmissionLimitExceededError(AnalysisAPIError):
    def __init__(self, msg, error_code=ANALYSIS_API_SUBMISSION_LIMIT_EXCEEDED):
        AnalysisAPIError.__init__(self, msg, error_code)


class InvalidHashAlgorithmError(RequestError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_HASH_ALGORITHM):
        RequestError.__init__(self, msg, error_code)


class InvalidURLError(SubmissionInvalidError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_URL):
        SubmissionInvalidError.__init__(self, msg, error_code)


class InvalidReportVersionError(RequestError):
    def __init__(self, msg, error_code=ANALYSIS_API_INVALID_REPORT_VERSION):
        RequestError.__init__(self, msg, error_code)


class FileExtractionFailedError(SubmissionInvalidError):
    def __init__(self, msg, error_code=ANALYSIS_API_FILE_EXTRACTION_FAILED):
        SubmissionInvalidError.__init__(self, msg, error_code)


#################
# client
#################

__COMPLETED_TASK_FIELDS = [
    "task_uuid",
    "score"
]
CompletedTask = collections.namedtuple("CompletedTask", __COMPLETED_TASK_FIELDS)


def get_time():
    """
    trivial wrapper around time.time to make testing easier
    """
    return time.time()


def purge_none(d):
    """
    Purge None entries from a dictionary
    """
    for k in d.keys():
        if d[k] is None:
            del d[k]
    return d


def parse_datetime(d):
    """
    Parse a datetime as formatted in one of the following formats:

    date: %Y-%m-%d'
    datetime: '%Y-%m-%d %H:%M:%S'
    datetime with microseconds: '%Y-%m-%d %H:%M:%S.%f'

    Can also handle a datetime.date or datetime.datetime object,
    (or anything that has year, month and day attributes)
    and converts it to datetime.datetime
    """
    if hasattr(d, "year") and hasattr(d, "month") and hasattr(d, "day"):
        return datetime.datetime(d.year, d.month, d.day)

    try:
        return datetime.datetime.strptime(
            d, AnalysisClientBase.DATETIME_MSEC_FMT)
    except ValueError: pass

    try:
        return datetime.datetime.strptime(d, AnalysisClientBase.DATETIME_FMT)
    except ValueError: pass

    try:
        return datetime.datetime.strptime(d, AnalysisClientBase.DATE_FMT)
    except ValueError:
        raise ValueError("Date '%s' does not match format '%s'" % (
                         d, "%Y-%m-%d[ %H:%M:%S[.%f]]'"))


class TaskCompletion(object):
    """
    Helper class to get score for all completed tasks

    :param analysis_client: analysis_apiclient.AnalysisClientBase

    Sample usage:

    tc = TaskCompletion(my_analysis_client)
    for completed_task in tc.get_completed(start,end):
        print completed_task.task_uuid, completed_task.score

    """
    def __init__(self, analysis_client):
        self.__analysis_client = analysis_client

    def get_completed(self, after, before):
        """
        Return scores of tasks completed in the specified time range.

        This takes care of using the analysis API's pagination
        to make sure it gets all tasks.

        :param after: datetime.datetime
        :param before: datetime.datetime

        :yield: sequence of `CompletedTask`

        :raise: InvalidAnalysisAPIResponse if response
            does not have the format we expect
        """
        try:
            while True:
                result = self.__analysis_client.get_completed(
                    after=after,
                    before=before,
                    include_score=True)

                data = result["data"]
                tasks = data["tasks"]
                if not tasks:
                    break

                for task_uuid, score  in tasks.iteritems():
                    yield CompletedTask(task_uuid=task_uuid,
                                        score=score)

                more = int(data["more_results_available"])
                if not more:
                    break

                last_ts = parse_datetime(data["before"])
                if last_ts >= before:
                    break

                after = last_ts

        except (KeyError, ValueError, TypeError, AttributeError):
            # attributeError needed in case iteritems is missing (not a dict)
            # let's give it the trace of the original exception, so we know
            # what the specific problem is!
            trace = sys.exc_info()[2]
            raise InvalidAnalysisAPIResponse("Unable to parse response to get_completed()"), None, trace


class AnalysisClientBase(object):
    """
    A client for the Lastline analysis API.

    This is an abstract base class: concrete
    subclasses just need to implement the _api_request
    method to actually send the API request to the server.

    :param base_url: URL where the lastline analysis API is located. (required)
    :param logger: if provided, should be a python logging.Logger object
        or object with similar interface.
    """
    SUB_APIS = ('analysis', 'management', 'research')

    DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
    DATETIME_MSEC_FMT = DATETIME_FMT + '.%f'
    DATE_FMT = '%Y-%m-%d'

    FORMATS = ["json", "xml", "pdf", "rtf"]

    REQUEST_PERFDATA = False

    ERRORS = {
        ANALYSIS_API_FILE_NOT_AVAILABLE: FileNotAvailableError,
        ANALYSIS_API_INVALID_CREDENTIALS: InvalidCredentialsError,
        ANALYSIS_API_INVALID_UUID: InvalidUUIDError,
        ANALYSIS_API_NO_RESULT_FOUND: NoResultFoundError,
        ANALYSIS_API_TEMPORARILY_UNAVAILABLE: TemporarilyUnavailableError,
        ANALYSIS_API_PERMISSION_DENIED: PermissionDeniedError,
        ANALYSIS_API_FILE_TOO_LARGE: FileTooLargeError,
        ANALYSIS_API_INVALID_FILE_TYPE: InvalidFileTypeError,
        ANALYSIS_API_INVALID_DOMAIN: InvalidMetadataError,
        ANALYSIS_API_INVALID_D_METADATA: InvalidMetadataError,
        ANALYSIS_API_INVALID_ARTIFACT_UUID: InvalidArtifactError,
        ANALYSIS_API_SUBMISSION_LIMIT_EXCEEDED: SubmissionLimitExceededError,
        ANALYSIS_API_INVALID_HASH_ALGORITHM: InvalidHashAlgorithmError,
        ANALYSIS_API_INVALID_URL: InvalidURLError,
        ANALYSIS_API_INVALID_REPORT_VERSION: InvalidReportVersionError,
        ANALYSIS_API_FILE_EXTRACTION_FAILED: FileExtractionFailedError,
      }

    def __init__(self, base_url, logger=None, config=None):
        self.__logger = logger
        self.__base_url = base_url
        self.__config = config

    def _logger(self):
        return self.__logger

    def __build_url(self, sub_api, parts, requested_format="json"):
        if sub_api not in AnalysisClientBase.SUB_APIS:
            raise InvalidSubApiType(sub_api)
        if requested_format not in AnalysisClientBase.FORMATS:
            raise InvalidFormat(requested_format)
        num_parts = 2 + len(parts)
        pattern = "/".join(["%s"] * num_parts) + ".%s"
        params = [self.__base_url, sub_api] + parts + [requested_format]
        return pattern % tuple(params)

    def __build_file_download_url(self, sub_api, parts):
        """
        Generate a URL to a direct file download
        """
        if sub_api not in AnalysisClientBase.SUB_APIS:
            raise InvalidSubApiType(sub_api)
        num_parts = 2 + len(parts)
        pattern = "/".join(["%s"] * num_parts)
        params = [self.__base_url, sub_api] + parts
        return pattern % tuple(params)

    def _check_file_like(self, f, param_name):
        if not hasattr(f, 'read'):
            raise AttributeError("The %s parameter is not a file-like " \
                                 "object" % param_name)

    def submit_exe_hash(self,
                        md5=None,
                        sha1=None,
                        download_ip=None,
                        download_port=None,
                        download_url=None,
                        download_host=None,
                        download_path=None,
                        download_agent=None,
                        download_referer=None,
                        download_request=None,
                        full_report_score=None,
                        bypass_cache=None,
                        raw=False,
                        verify=True):
        """
        Submit a file by hash.

        Deprecated version of submit_file_hash() - see below
        """
        return self.submit_file_hash(md5, sha1,
                        download_ip=download_ip,
                        download_port=download_port,
                        download_url=download_url,
                        download_host=download_host,
                        download_path=download_path,
                        download_agent=download_agent,
                        download_referer=download_referer,
                        download_request=download_request,
                        full_report_score=full_report_score,
                        bypass_cache=bypass_cache,
                        raw=raw,
                        verify=verify)

    def submit_file_hash(self,
                        md5=None,
                        sha1=None,
                        download_ip=None,
                        download_port=None,
                        download_url=None,
                        download_host=None,
                        download_path=None,
                        download_agent=None,
                        download_referer=None,
                        download_request=None,
                        full_report_score=None,
                        bypass_cache=None,
                        backend=None,
                        require_file_analysis=True,
                        mime_type=None,
                        analysis_timeout=None,
                        analysis_env=None,
                        allow_network_traffic=None,
                        filename=None,
                        keep_file_dumps=None,
                        keep_memory_dumps=None,
                        keep_behavior_log=None,
                        push_to_portal_account=None,
                        raw=False,
                        verify=True,
                        server_ip=None,
                        server_port=None,
                        server_host=None,
                        client_ip=None,
                        client_port=None,
                        is_download=True,
                        protocol="http",
                        apk_package_name=None,
                        report_version=None):
        """
        Submit a file by hash.

        Either an md5 or a sha1 parameter must be provided.
        If both are provided, they should be consistent.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.submit_file`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param md5: md5 hash of file.
        :param sha1: sha1 hash of file.
        :param download_ip: DEPRECATED! Use server_ip instead.
        :param download_port: DEPRECATED! Use server_port instead.
        :param download_url: DEPRECATED! replaced by the download_host
            and download_path parameters
        :param download_host: DEPRECATED! Use server_host instead.
        :param download_path: host path from which the submitted file
            was originally downloaded, as a string of bytes (not unicode)
        :param download_agent: HTTP user-agent header that was used
            when the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param download_referer: HTTP referer header that was used
            when the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param download_request: full HTTP request with
            which the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param full_report_score: if set, this value (between -1 and 101)
            determines starting at which scores a full report is returned.
            -1 and 101 indicate "never return full report";
            0 indicates "return full report at all times"
        :param bypass_cache: if True, the API will not serve a cached
            result. NOTE: This requires special privileges.
        :param require_file_analysis: if True, the submission requires an
            analysis run to be started. If False, the API will attempt to
            base a decision solely on static information such as
            download source reputation and hash lookups. Requires special
            permissions
        :param mime_type: the mime-type of the file; This value should be
            set when require_file_analysis is True to enforce getting the
            most information available
        :param analysis_timeout: timeout in seconds after which to terminate
            analysis. The analysis engine might decide to extend this timeout
            if necessary. If all analysis subjects terminate before this timeout
            analysis might be shorter
        :param analysis_env: environment in which to run analysis. This includes
            the operating system as well as version of tools such as Microsoft
            Office. Example usage:
            - windows7:office2003, or
            - windowsxp
            By default, analysis will run on all available operating systems
            using the most applicable tools.
        :param allow_network_traffic: if False, all network connections will be
            redirected to a honeypot. Requires special permissions.
        :param filename: filename to use during analysis. If none is passed,
            the analysis engine will pick an appropriate name automatically.
            An easy way to pass this value is to use 'file_stream.name' for most
            file-like objects
        :param keep_file_dumps: if True, all files generated during
            analysis will be kept for post-processing. NOTE: This can generate
            large volumes of data and is not recommended. Requires special
            permissions
        :param keep_memory_dumps: if True, all buffers allocated during
            analysis will be kept for post-processing. NOTE: This can generate
            *very* large volumes of data and is not recommended. Requires
            special permissions
        :param keep_behavior_log: if True, the raw behavior log extracted during
            analysis will be kept for post-processing. NOTE: This can generate
            *very very* large volumes of data and is not recommended. Requires
            special permissions
        :param push_to_portal_account: if set, a successful submission will be
            pushed to the web-portal using the specified account
        :param backend: DEPRECATED! Don't use
        :param verify: if False, disable SSL-certificate verification
        :param raw: if True, return the raw json results of the API query
        :param server_ip: ASCII dotted-quad representation of the IP address of
            the server-side endpoint.
        :param server_port: integer representation of the port number
            of the server-side endpoint of the flow tuple.
        :param server_host: hostname of the server-side endpoint of
            the connection, as a string of bytes (not unicode).
        :param client_ip: ASCII dotted-quad representation of the IP address of
            the client-side endpoint.
        :param client_port: integer representation of the port number
            of the client-side endpoint of the flow tuple.
        :param is_download: Boolean; True if the transfer happened in the
            server -> client direction, False otherwise (client -> server).
        :param protocol: app-layer protocol in which the file got
            transferred. Short ASCII string.
        :param apk_package_name: package name for APK files. Don't specify
            manually.
        :param report_version: Version name of the Report that will be returned
                               (optional);
        """
        if self.__logger and backend:
            self.__logger.warning("Ignoring deprecated parameter 'backend'")

        url = self.__build_url("analysis", ["submit", "file"])
        # These options require special permissions, so we should not set them
        # if not specified
        if allow_network_traffic is not None:
            allow_network_traffic = allow_network_traffic and 1 or 0
        if keep_file_dumps is not None:
            keep_file_dumps = keep_file_dumps and 1 or 0
        if keep_memory_dumps is not None:
            keep_memory_dumps = keep_memory_dumps and 1 or 0
        if keep_behavior_log is not None:
            keep_behavior_log = keep_behavior_log and 1 or 0
        params = purge_none({
            "md5": md5,
            "sha1": sha1,
            "full_report_score": full_report_score,
            "bypass_cache": bypass_cache and 1 or None,
            "require_file_analysis": require_file_analysis and 1 or 0,
            "mime_type": mime_type,
            "download_ip": download_ip,
            "download_port": download_port,
            # analysis-specific options:
            "analysis_timeout": analysis_timeout or None,
            "analysis_env": analysis_env,
            "allow_network_traffic": allow_network_traffic,
            "filename": filename,
            "keep_file_dumps": keep_file_dumps,
            "keep_memory_dumps": keep_memory_dumps,
            "keep_behavior_log": keep_behavior_log,
            "push_to_portal_account": push_to_portal_account or None,
            "server_ip": server_ip,
            "server_port": server_port,
            "server_host": server_host,
            "client_ip": client_ip,
            "client_port": client_port,
            "is_download": is_download,
            "protocol": protocol,
            "apk_package_name": apk_package_name,
            "report_version": report_version,
          })
        # using and-or-trick to convert to a StringIO if it is not None
        # this just wraps it into a file-like object
        files = purge_none({
            "download_url": download_url is not None and \
                               StringIO.StringIO(download_url) or None,
            "download_host": download_host is not None and \
                               StringIO.StringIO(download_host) or None,
            "download_path": download_path is not None and \
                               StringIO.StringIO(download_path) or None,
            "download_agent": download_agent is not None and \
                               StringIO.StringIO(download_agent) or None,
            "download_referer": download_referer is not None and \
                               StringIO.StringIO(download_referer) or None,
            "download_request": download_request is not None and \
                               StringIO.StringIO(download_request) or None,
            "server_host": server_host is not None and \
                               StringIO.StringIO(server_host) or None,
          })
        return self._api_request(url, params, files=files, post=True,
                                 raw=raw, verify=verify)

    def submit_exe_file(self,
                        file_stream,
                        download_ip=None,
                        download_port=None,
                        download_url=None,
                        download_host=None,
                        download_path=None,
                        download_agent=None,
                        download_referer=None,
                        download_request=None,
                        full_report_score=None,
                        bypass_cache=None,
                        delete_after_analysis=False,
                        raw=False,
                        verify=True):
        """
        Submit a file by uploading it.

        Deprecated version of submit_file() - see below
        """
        return self.submit_file(file_stream,
                        download_ip=download_ip,
                        download_port=download_port,
                        download_url=download_url,
                        download_host=download_host,
                        download_path=download_path,
                        download_agent=download_agent,
                        download_referer=download_referer,
                        download_request=download_request,
                        full_report_score=full_report_score,
                        bypass_cache=bypass_cache,
                        delete_after_analysis=delete_after_analysis,
                        raw=raw,
                        verify=verify)

    def submit_file(self, file_stream,
                    download_ip=None,
                    download_port=None,
                    download_url=None,
                    download_host=None,
                    download_path=None,
                    download_agent=None,
                    download_referer=None,
                    download_request=None,
                    full_report_score=None,
                    bypass_cache=None,
                    delete_after_analysis=None,
                    backend=None,
                    analysis_timeout=None,
                    analysis_env=None,
                    allow_network_traffic=None,
                    filename=None,
                    keep_file_dumps=None,
                    keep_memory_dumps=None,
                    keep_behavior_log=None,
                    push_to_portal_account=None,
                    raw=False,
                    verify=True,
                    server_ip=None,
                    server_port=None,
                    server_host=None,
                    client_ip=None,
                    client_port=None,
                    is_download=True,
                    protocol="http",
                    apk_package_name=None,
                    password=None,
                    report_version=None):
        """
        Submit a file by uploading it.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.submit_file`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param file_stream: file-like object containing
            the file to upload.
        :param download_ip: DEPRECATED! Use server_ip instead.
        :param download_port: DEPRECATED! Use server_port instead.
        :param download_url: DEPRECATED! replaced by the download_host
            and download_path parameters
        :param download_host: DEPRECATED! Use server_host instead.
        :param download_path: host path from which the submitted file
            was originally downloaded, as a string of bytes (not unicode)
        :param download_agent: HTTP user-agent header that was used
            when the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param download_referer: HTTP referer header that was used
            when the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param download_request: full HTTP request with
            which the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param full_report_score: if set, this value (between -1 and 101)
            determines starting at which scores a full report is returned.
            -1 and 101 indicate "never return full report";
            0 indicates "return full report at all times"
        :param bypass_cache: if True, the API will not serve a cached
            result. NOTE: This requires special privileges.
        :param delete_after_analysis: if True, the backend will delete the
            file after analysis is done (and noone previously submitted
            this file with this flag set)
        :param analysis_timeout: timeout in seconds after which to terminate
            analysis. The analysis engine might decide to extend this timeout
            if necessary. If all analysis subjects terminate before this timeout
            analysis might be shorter
        :param analysis_env: environment in which to run analysis. This includes
            the operating system as well as version of tools such as Microsoft
            Office. Example usage:
            - windows7:office2003, or
            - windowsxp
            By default, analysis will run on all available operating systems
            using the most applicable tools.
        :param allow_network_traffic: if False, all network connections will be
            redirected to a honeypot. Requires special permissions.
        :param filename: filename to use during analysis. If none is passed,
            the analysis engine will pick an appropriate name automatically.
            An easy way to pass this value is to use 'file_stream.name' for most
            file-like objects
        :param keep_file_dumps: if True, all files generated during
            analysis will be kept for post-processing. NOTE: This can generate
            large volumes of data and is not recommended. Requires special
            permissions
        :param keep_memory_dumps: if True, all buffers allocated during
            analysis will be kept for post-processing. NOTE: This can generate
            large volumes of data and is not recommended. Requires special
            permissions
        :param keep_behavior_log: if True, the raw behavior log extracted during
            analysis will be kept for post-processing. NOTE: This can generate
            *very very* large volumes of data and is not recommended. Requires
            special permissions
        :param push_to_portal_account: if set, a successful submission will be
            pushed to the web-portal using the specified username
        :param backend: DEPRECATED! Don't use
        :param verify: if False, disable SSL-certificate verification
        :param raw: if True, return the raw JSON results of the API query
        :param server_ip: ASCII dotted-quad representation of the IP address of
            the server-side endpoint.
        :param server_port: integer representation of the port number
            of the server-side endpoint of the flow tuple.
        :param server_host: hostname of the server-side endpoint of
            the connection, as a string of bytes (not unicode).
        :param client_ip: ASCII dotted-quad representation of the IP address of
            the client-side endpoint.
        :param client_port: integer representation of the port number
            of the client-side endpoint of the flow tuple.
        :param is_download: Boolean; True if the transfer happened in the
            server -> client direction, False otherwise (client -> server).
        :param protocol: app-layer protocol in which the file got
            transferred. Short ASCII string.
        :param report_version: Version name of the Report that will be returned
                               (optional);
        :param apk_package_name: package name for APK files. Don't specify
            manually.
        :param password: password used to unpack encrypted archives
        """
        if self.__logger and backend:
            self.__logger.warning("Ignoring deprecated parameter 'backend'")

        self._check_file_like(file_stream, "file_stream")
        url = self.__build_url("analysis", ["submit", "file"])
        # These options require special permissions, so we should not set them
        # if not specified
        if allow_network_traffic is not None:
            allow_network_traffic = allow_network_traffic and 1 or 0
        if keep_file_dumps is not None:
            keep_file_dumps = keep_file_dumps and 1 or 0
        if keep_memory_dumps is not None:
            keep_memory_dumps = keep_memory_dumps and 1 or 0
        if keep_behavior_log is not None:
            keep_behavior_log = keep_behavior_log and 1 or 0
        params = purge_none({
            "bypass_cache": bypass_cache and 1 or None,
            "full_report_score": full_report_score,
            "delete_after_analysis": delete_after_analysis and 1 or 0,
            "download_ip": download_ip,
            "download_port": download_port,
            # analysis-specific options:
            "analysis_timeout": analysis_timeout or None,
            "analysis_env": analysis_env,
            "allow_network_traffic": allow_network_traffic,
            "filename": filename,
            "keep_file_dumps": keep_file_dumps,
            "keep_memory_dumps": keep_memory_dumps,
            "keep_behavior_log": keep_behavior_log,
            "push_to_portal_account": push_to_portal_account or None,
            "server_ip": server_ip,
            "server_port": server_port,
            "server_host": server_host,
            "client_ip": client_ip,
            "client_port": client_port,
            "is_download": is_download,
            "protocol": protocol,
            "apk_package_name": apk_package_name,
            "password": password,
            "report_version": report_version,
          })

        # If an explicit filename was provided, we can pass it down to
        # python-requests to use it in the multipart/form-data.
        # This avoids having python-requests trying to guess the filename
        # based on stream attributes.
        named_stream = (filename, file_stream) if filename else file_stream

        # using and-or-trick to convert to a StringIO if it is not None
        # this just wraps it into a file-like object
        files = purge_none({
            "file": named_stream,
            "download_url": download_url is not None and \
                                  StringIO.StringIO(download_url) or None,
            "download_host": download_host is not None and \
                                  StringIO.StringIO(download_host) or None,
            "download_path": download_path is not None and \
                                  StringIO.StringIO(download_path) or None,
            "download_agent": download_agent is not None and \
                                  StringIO.StringIO(download_agent) or None,
            "download_referer": download_referer is not None and \
                                  StringIO.StringIO(download_referer) or None,
            "download_request": download_request is not None and \
                                  StringIO.StringIO(download_request) or None,
            "server_host": server_host is not None and \
                                  StringIO.StringIO(server_host) or None,
          })
        return self._api_request(url, params, files=files, post=True,
                                 raw=raw, verify=verify)


    def submit_file_metadata(self, md5, sha1,
                                   download_ip,
                                   download_port,
                                   download_host=None,
                                   download_path=None,
                                   download_agent=None,
                                   download_referer=None,
                                   download_request=None,
                                   raw=False,
                                   verify=True):
        """
        Submit metadata regarding a file download.

        Both the md5 and the sha1 parameter must be provided.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param md5: md5 hash of the downloaded file.
        :param sha1: sha1 hash of the downloaded file.
        :param download_ip: ASCII dotted-quad representation of the IP address
            from which the file has been downloaded
        :param download_port: integer representation of the port number
            from which the file has been downloaded
        :param download_host: host from which the submitted file
            was originally downloaded, as a string of bytes (not unicode)
        :param download_path: host path from which the submitted file
            was originally downloaded, as a string of bytes (not unicode)
        :param download_agent: HTTP user-agent header that was used
            when the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param download_referer: HTTP referer header that was used
            when the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param download_request: full HTTP request with
            which the submitted file was originally downloaded,
            as a string of bytes (not unicode)
        :param verify: if False, disable SSL-certificate verification
        :param raw: if True, return the raw json results of the API query
        """
        url = self.__build_url("analysis", ["submit", "download"])
        params = {
            "md5": md5,
            "sha1": sha1,
            "download_ip": download_ip,
            "download_port": download_port
          }
        #using and-or-trick to convert to a StringIO if it is not None
        #this just wraps it into a file-like object
        files = {
            "download_host": download_host is not None and \
                                   StringIO.StringIO(download_host) or None,
            "download_path": download_path is not None and \
                                   StringIO.StringIO(download_path) or None,
            "download_agent": download_agent is not None and \
                                   StringIO.StringIO(download_agent) or None,
            "download_referer": download_referer is not None and \
                                   StringIO.StringIO(download_referer) or None,
            "download_request": download_request is not None and \
                                   StringIO.StringIO(download_request) or None

          }
        purge_none(files)
        purge_none(params)
        return self._api_request(url, params, files=files, post=True,
                                 raw=raw, verify=verify)


    def submit_url(self,
                   url,
                   referer=None,
                   full_report_score=None,
                   bypass_cache=None,
                   backend=None,
                   analysis_timeout=None,
                   push_to_portal_account=None,
                   raw=False,
                   verify=True,
                   user_agent=None,
                   report_version=None):
        """
        Submit a url.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.submit_url`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param url: url to analyze
        :param referer: referer header to use for analysis
        :param full_report_score: if set, this value (between -1 and 101)
            determines starting at which scores a full report is returned.
            -1 and 101 indicate "never return full report";
            0 indicates "return full report at all times"
        :param bypass_cache: if True, the API will not serve a cached
            result. NOTE: This requires special privileges.
        :param analysis_timeout: timeout in seconds after which to terminate
            analysis. The analysis engine might decide to extend this timeout
            if necessary. If all analysis subjects terminate before this timeout
            analysis might be shorter
        :param push_to_portal_account: if set, a successful submission will be
            pushed to the web-portal using the specified account
        :param backend: DEPRECATED! Don't use
        :param verify: if False, disable SSL-certificate verification
        :param raw: if True, return the raw JSON results of the API query
        :param report_version: Version name of the Report that will be returned
                               (optional);
        :param user_agent: user agent header to use for analysis
        """
        if self.__logger and backend:
            self.__logger.warning("Ignoring deprecated parameter 'backend'")

        api_url = self.__build_url("analysis", ["submit", "url"])
        params = purge_none({
            "url":url,
            "referer":referer,
            "full_report_score":full_report_score,
            "bypass_cache":bypass_cache and 1 or None,
            "analysis_timeout": analysis_timeout or None,
            "push_to_portal_account": push_to_portal_account or None,
            "user_agent": user_agent or None,
            "report_version" : report_version,
          })
        return self._api_request(api_url, params, post=True,
                                 raw=raw, verify=verify)

    def get_result(self,
                   uuid,
                   report_uuid=None,
                   full_report_score=None,
                   include_scoring_components=None,
                   raw=False,
                   requested_format="json",
                   verify=True,
                   report_version=None):
        """
        Get results for a previously submitted
        analysis task.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.get_results`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param uuid: the unique identifier of the submitted task,
            as returned in the task_uuid field of submit methods.
        :param report_uuid: if set, include this report in the result.
        :param full_report_score: if set, this value (between -1 and 101)
            determines starting at which scores a full report is returned.
            -1 and 101 indicate "never return full report";
            0 indicates "return full report at all times"
        :param include_scoring_components: if True, the result will contain
            details of all components contributing to the overall score.
            Requires special permissions
        :param raw: if True, return the raw JSON/XML results of the API query.
        :param requested_format: JSON, XML, PDF, or RTF.
            If format is not JSON, this implies `raw`.
        :param report_version: Version of the report to be returned
                               (optional)
        """
        # better: use 'get_results()' but that would break
        # backwards-compatibility
        url = self.__build_url('analysis', ['get'],
                               requested_format=requested_format)
        params = purge_none({
            'uuid': uuid,
            'report_uuid': report_uuid,
            'full_report_score': full_report_score,
            'include_scoring_components': include_scoring_components and 1 or 0,
            'report_version': report_version
          })
        if requested_format.lower() != 'json':
            raw = True
        return self._api_request(url,
                                 params,
                                 raw=raw,
                                 requested_format=requested_format,
                                 post=True,
                                 verify=verify)

    def get_result_summary(self, uuid, raw=False,
                           requested_format="json",
                           score_only=False,
                           verify=True):
        """
        Get result summary for a previously submitted analysis task.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.get_result`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param uuid: the unique identifier of the submitted task,
            as returned in the task_uuid field of submit methods.
        :param raw: if True, return the raw JSON/XML results of the API query.
        :param requested_format: JSON or XML. If format is not JSON, this
            implies `raw`.
        :param score_only: if True, return even less data (only score and
            threat/threat-class classification).
        """
        url = self.__build_url("analysis", ["get_result"],
                               requested_format=requested_format)
        params = {
            'uuid': uuid,
            'score_only': score_only and 1 or 0,
          }
        if requested_format.lower() != "json":
            raw = True
        return self._api_request(url,
                                 params,
                                 raw=raw,
                                 requested_format=requested_format,
                                 post=True,
                                 verify=verify)

    def get_result_artifact(self, uuid, report_uuid, artifact_name,
                            raw=False, verify=True):
        """
        Get artifact generated by an analysis result for a previously
        submitted analysis task.

        :param uuid: the unique identifier of the submitted task,
            as returned in the task_uuid field of submit methods.
        :param report_uuid: the unique report identifier returned as part of
            the dictionary returned by get_result()
        :param artifact_name: the name of the artifact as mentioned in the
            given report in the dictionary returned by get_result()
        :param raw: if True, return the raw JSON/XML results of the API query.
        """
        url = self.__build_file_download_url("analysis",
                                             ["get_result_artifact"])
        params = {
            'uuid': uuid,
            'artifact_uuid': "%s:%s" % (report_uuid, artifact_name)
          }

        # NOTE: This API request is completely different because it
        # returns real HTTP status-codes (and errors) directly
        try:
            result = self._api_request(url, params, requested_format='raw',
                                       raw=raw, post=True, verify=verify)
            if not result:
                raise InvalidArtifactError()

        except CommunicationError, exc:
            internal_error = str(exc.internal_error())
            if internal_error == '410':
                raise InvalidArtifactError("The artifact is no longer " \
                                           "available")
            if internal_error == '404':
                raise InvalidArtifactError("The artifact could not be found")

            if internal_error == '412':
                raise InvalidUUIDError()

            if internal_error == '412':
                raise InvalidUUIDError()

            if internal_error == '401':
                raise PermissionDeniedError()

            # we have nothing more specific to say -- raise the
            # original CommunicationError
            raise

        return StringIO.StringIO(result)

    def query_task_artifact(self, uuid, artifact_name, raw=False, verify=True):
        """
        Query if a specific task artifact is available for download.

        :param uuid: the unique identifier of the submitted task,
            as returned in the task_uuid field of submit methods.
        :param artifact_name: the name of the artifact
        :param raw: if True, return the raw JSON/XML results of the API query.
        """
        url = self.__build_url("analysis", ["query_task_artifact"])
        params = purge_none({
            'uuid': uuid,
            'artifact_name': artifact_name,
          })
        return self._api_request(url, params, raw=raw, verify=verify)

    def completed(self, after, before=None, raw=False, verify=True):
        """
        Deprecated. Use 'get_completed()'
        """
        return self.get_completed(after, before=before,
                                  verify=verify, raw=raw)

    def get_completed(self, after, before=None, raw=False, verify=True,
                      include_score=False):
        """
        Get the list of uuids of tasks that were completed
        within a given time frame.

        The main use-case for this method is to periodically
        request a list of uuids completed since the last
        time this method was invoked, and then fetch
        each result with `get_results()`.

        Date parameters to this method can be:
         - date string: %Y-%m-%d'
         - datetime string: '%Y-%m-%d %H:%M:%S'
         - datetime.datetime object

        All times are in UTC.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.get_completed`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param after: Request tasks completed after this time.
        :param before: Request tasks completed before this time.
        :param include_score: If True, the response contains scores together
            with the task-UUIDs that have completed
        :param raw: if True, return the raw JSON results of the API query.
        """
        # better: use 'get_completed()' but that would break
        # backwards-compatibility
        url = self.__build_url("analysis", ["completed"])
        if hasattr(before, "strftime"):
            before = before.strftime(AnalysisClientBase.DATETIME_FMT)
        if hasattr(after, "strftime"):
            after = after.strftime(AnalysisClientBase.DATETIME_FMT)
        params = purge_none({
            'before': before,
            'after': after,
            'include_score': include_score and 1 or 0,
          })
        return self._api_request(url, params, raw=raw, post=True, verify=verify)

    def get_progress(self, uuid, raw=False):
        """
        Get a progress estimate for a previously submitted analysis task.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.get_results`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param uuid: the unique identifier of the submitted task,
            as returned in the task_uuid field of submit methods.
        :param raw: if True, return the raw JSON/XML results of the API query.
        :param requested_format: JSON or XML. If format is not JSON, this implies `raw`.
        """
        url = self.__build_url('analysis', ['get_progress'])
        params = { 'uuid': uuid }
        return self._api_request(url, params, raw=raw, post=True)

    def query_file_hash(self, hash_value=None, algorithm=None, block_size=None,
                        md5=None, sha1=None, mmh3=None, raw=False):
        """
        Search for existing analysis results with the given file-hash.

        :param hash_value: The (partial) file-hash.
        :param algorithm: One of MD5/SHA1/MMH3
        :param block_size: Size of the block (at file start) used for generating
            the hash-value. By default (or if 0), the entire file is assumed.
        :param md5: Helper to quickly set `hash_value` and `algorithm`
        :param sha1: Helper to quickly set `hash_value` and `algorithm`
        :param mmh3: Helper to quickly set `hash_value` and `algorithm`
        :param raw: if True, return the raw JSON/XML results of the API query.
        :param requested_format: JSON or XML. If format is not JSON, this
            implies `raw`.
        """
        if md5 or sha1 or mmh3:
            if hash_value or algorithm:
                raise TypeError("Conflicting values passed for hash/algorithm")
            if md5 and not sha1 and not mmh3:
                hash_value = md5
                algorithm = 'md5'
            elif sha1 and not md5 and not mmh3:
                hash_value = sha1
                algorithm = 'sha1'
            elif mmh3 and not md5 and not sha1:
                hash_value = mmh3
                algorithm = 'mmh3'
            else:
                raise TypeError("Conflicting values passed for hash/algorithm")
        elif not hash_value or not algorithm:
            raise TypeError("Missing values for hash_value/algorithm")

        url = self.__build_url('analysis', ['query/file_hash'])
        params = purge_none({
            'hash_value': hash_value,
            'hash_algorithm': algorithm,
            'hash_block_size': block_size,
          })
        return self._api_request(url, params, raw=raw, post=True)

    def is_blocked_file_hash(self, hash_value=None, algorithm=None,
                             block_size=None, md5=None, sha1=None, mmh3=None,
                             raw=False):
        """
        Check if the given file-hash belongs to a malicious file and we have
        gathered enough information to block based on this (partial) hash.

        :param hash_value: The (partial) file-hash.
        :param algorithm: One of MD5/SHA1/MMH3
        :param block_size: Size of the block (at file start) used for generating
            the hash-value. By default (or if 0), the entire file is assumed.
        :param md5: Helper to quickly set `hash_value` and `algorithm`
        :param sha1: Helper to quickly set `hash_value` and `algorithm`
        :param mmh3: Helper to quickly set `hash_value` and `algorithm`
        :param raw: if True, return the raw JSON/XML results of the API query.
        :param requested_format: JSON or XML. If format is not JSON, this implies `raw`.
        """
        if md5 or sha1 or mmh3:
            if hash_value or algorithm:
                raise TypeError("Conflicting values passed for hash/algorithm")
            if md5 and not sha1 and not mmh3:
                hash_value = md5
                algorithm = 'md5'
            elif sha1 and not md5 and not mmh3:
                hash_value = sha1
                algorithm = 'sha1'
            elif mmh3 and not md5 and not sha1:
                hash_value = mmh3
                algorithm = 'mmh3'
            else:
                raise TypeError("Conflicting values passed for hash/algorithm")
        elif not hash_value or not algorithm:
            raise TypeError("Missing values for hash_value/algorithm")

        url = self.__build_url('analysis', ['query/is_blocked_file_hash'])
        params = purge_none({
            'hash_value': hash_value,
            'hash_algorithm': algorithm,
            'hash_block_size': block_size,
          })
        return self._api_request(url, params, raw=raw, post=True)

    def query_analysis_engine_tasks(self, analysis_engine_task_uuids,
                                    analysis_engine='analyst', raw=False):
        """
        Provide a set of task UUIDs from an analysis engine (such as Analyst
        Scheduler or Anubis) and find completed tasks that contain this analysis
        engine task.

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.query_analysis_engine_tasks`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param analysis_engine_task_uuids: List of analysis engine task UUIDs to
            search.
        :param analysis_engine: The analysis engine the task refers to.
        :param raw: if True, return the raw JSON results of the API query.
        """
        url = self.__build_url('analysis', ['query/analysis_engine_tasks'])
        params = purge_none({
            'analysis_engine_task_uuids': ','.join(analysis_engine_task_uuids),
            'analysis_engine': analysis_engine,
        })
        return self._api_request(url, params, post=True, raw=raw)

    def analyze_sandbox_result(self, analysis_task_uuid,
                               analysis_engine='anubis',
                               full_report_score=None,
                               bypass_cache=False,
                               raw=False):
        """
        Provide a task UUID from an analysis engine (such as Analyst Scheduler
        or Anubis) and trigger scoring of the activity captured by the analysis
        report.

        Similar to submitting by exe hash (md5/sha1) but we can enforce
        the precise analysis result (if there are multiple) that we want
        to score

        For return values and error codes please
        see :py:meth:`malscape.api.views.analysis.analyze_sandbox_result`.

        If there is an error and `raw` is not set,
        a :py:class:`AnalysisAPIError` exception will be raised.

        :param analysis_task_uuid: The sandbox task UUID to analyze/import.
        :param analysis_engine: The sandbox the task refers to.
        :param full_report_score: if set, this value (between -1 and 101)
            determines starting at which scores a full report is returned.
            -1 and 101 indicate "never return full report";
            0 indicates "return full report at all times"
        :param bypass_cache: if True, the API will not serve a cached
            result. NOTE: This requires special privileges.
        :param raw: if True, return the raw JSON results of the API query.
        """
        url = self.__build_url('analysis', ['analyze_sandbox_result'])
        params = {
            'analysis_task_uuid':analysis_task_uuid,
            'analysis_engine': analysis_engine,
            'full_report_score': full_report_score,
            'bypass_cache': bypass_cache and 1 or None,
          }
        purge_none(params)
        return self._api_request(url, params, raw=raw)

    def _api_request(self,
                     url,
                     params=None,
                     files=None,
                     timeout=None,
                     post=False,
                     raw=False,
                     requested_format="json",
                     verify=True):
        """
        Send an API request and return the results.

        :param url: API URL to fetch.
        :param params: GET or POST parameters.
        :param files: files to upload with request.
        :param timeout: request timeout in seconds.
        :param post: use HTTP POST instead of GET
        :param raw: return the raw json results of API query
        :param requested_foramt: JSON or XML. If format is not JSON, this implies `raw`.
        """
        raise NotImplementedError("%s does not implement api_request()" % self.__class__.__name__)

    def _process_response_page(self, page, raw, requested_format):
        """
        Helper for formatting/processing api response before returning it.
        """
        if raw or requested_format.lower() != "json":
            return page

        #why does pylint think result is a bool??
        #pylint: disable=E1103
        result = json.loads(page)
        success = result['success']
        if success:
            return result
        else:
            error_code = result.get('error_code', None)
            # raise the most specific error we can
            exception_class = AnalysisClientBase.ERRORS.get(error_code) or \
                              AnalysisAPIError
            raise exception_class(result['error'], error_code)

    def rescore_task(self, uuid=None, md5=None, sha1=None,
                     min_score=0, max_score=100,
                     threat=None, threat_class=None,
                     force_local=False, raw=False):
        """
        Enforce re-scoring of a specific task or multiple tasks based on the
        submitted file. Requires specific permissions.

        At least one of uuid/md5 must be provided. If sha1 is given, it must
        match with the md5 that was provided. Existing manual-score threat/
        threat-class information will not be overwritten unless an empty-
        string ('') is passed to this function.

        This API-call returns the task-UUIDs that were triggered for rescoring.

        NOTE: Even when a single task-UUID is passed, the API might decide to
        re-score all tasks for the same file!

        :param uuid: the unique identifier of the submitted task,
            as returned in the task_uuid field of submit methods.
        :param md5: the md5 hash of the submitted file.
        :param sha1: the sha1 hash of the submitted file.
        :param force_local: if True, enforce that the manual score is applied
            only locally. This is the default for on-premise instances and
            cannot be enforced there. Requires special permissions.
        :param raw: if True, return the raw JSON/XML results of the API query.
        """
        assert uuid or md5, "Please provide task-uuid/md5"
        url = self.__build_url('management', ['rescore'])
        params = purge_none({
            'uuid': uuid,
            'md5': md5,
            'sha1': sha1,
            'min_score': min_score,
            'max_score': max_score,
            'threat': threat,
            'threat_class': threat_class,
            # use the default if no force is set
            'force_local': force_local and 1 or None,
        })
        return self._api_request(url, params, raw=raw, post=True)

    def rescore_scanner(self, scanner, after, before,
                         min_score=0, max_score=100,
                         min_scanner_score=0, max_scanner_score=100,
                         max_version=None, test_flag=None, force=False,
                         raw=False):
        """
        Find tasks that triggered a certain scanner and mark them for
        reprocessing.

        This API-call returns the task-UUIDs that were triggered for rescoring.

        :param scanner: Name of the scanner.
        :param after: Reprocess tasks completed after this time.
        :param before: Reprocess tasks completed before this time.
        :param min_score: Minimum score of tasks to reprocess.
        :param max_score: Maximum score of tasks to reprocess.
        :param min_scanner_score: Minimum score of scanner detection (on backend
            task) to reprocess.
        :param max_scanner_score: Maximum score of scanner detection (on backend
            task) to reprocess.
        :param max_version: Maximum version of scanner to reprocess.
        :param test_flag: If True, only affect backend-tasks where the scanner
            was in *test* mode; if False, only affect backend-tasks where the
            scanner was in *real* mode; otherwise affect all backend-tasks
            regardless of the *test* flag.
        :param force: By default, the API will refuse rescoring any scanners that
            affect more than 100 tasks. To rescore large amounts, distribute the
            work over multiple time-windows. This safety can be disabled by
            setting the *force* parameter to True.
        """
        if hasattr(before, "strftime"):
            before = before.strftime(AnalysisClientBase.DATETIME_FMT)
        if hasattr(after, "strftime"):
            after = after.strftime(AnalysisClientBase.DATETIME_FMT)

        url = self.__build_url('management', ['rescore_scanner'])
        params = purge_none({
            'scanner': scanner,
            'after': after,
            'before': before,
            'min_score': min_score,
            'max_score': max_score,
            'min_scanner_score': min_scanner_score,
            'max_scanner_score': max_scanner_score,
            'max_version': max_version,
        })
        if test_flag is not None:
            params['test_flag'] = test_flag and 1 or 0
        if force:
            params['force'] = 1
        return self._api_request(url, params, raw=raw, post=True)

    def suppress_scanner(self, scanner, max_version, raw=False):
        """
        Mark a scanner as suppressed.

        :param scanner: Name of the scanner.
        :param max_version: Version of scanner up to which it is supposed to be
            suppressed. So, if the first scanner-version that should be used
            for scoring is X, provide (X-1).
        """
        url = self.__build_url('management', ['suppress_scanner'])
        params = purge_none({
            'scanner': scanner,
            'max_version': max_version,
        })
        return self._api_request(url, params, raw=raw, post=True)

    def create_ticket(self, uuid=None, md5=None, sha1=None,
                      min_score=0, max_score=100, summary=None, labels=None,
                      is_false_negative=False, is_false_positive=False,
                      is_from_customer=False, is_from_partner=False,
                      force=False, raw=False):
        """
        Enforce re-scoring of a specific task or multiple tasks based on the
        submitted file. Requires specific permissions.

        At least one of uuid/md5/sha1 must be provided. If both file-hashes are
        provided, they must match the same file.

        :param uuid: the unique identifier of the submitted task,
            as returned in the task_uuid field of submit methods.
        :param md5: the md5 hash of the submitted file.
        :param sha1: the sha1 hash of the submitted file.
        :param force: if True, enforce the generation of a ticket, even if none
            of the task-analysis rules would have generated a ticket
        :param min_score: Limit generation of tickets to tasks above the given
            threshold
        :param max_score: Limit generation of tickets to tasks below the given
            threshold
        :param summary: Optional summary (title) to use for the ticket.
        :param labels: Optional set of labels to assign to a task
        :param is_false_negative: Helper parameter to add the standard FN label
        :param is_false_positive: Helper parameter to add the standard FP label
        :param is_from_customer: Helper parameter to add the standard
            from-customer label
        :param is_from_partner: Helper parameter to add the standard
            from-partner label
        :param raw: if True, return the raw JSON/XML results of the API query.
        """
        assert uuid or md5 or sha1, "Please provide task-uuid/md5/sha1"
        url = self.__build_url('management', ['create_ticket'])
        if labels:
            labels = set(labels)
        else:
            labels = set()
        if is_false_negative:
            labels.add('false_negatives')
        if is_false_positive:
            labels.add('false_positives')
        if is_from_customer:
            labels.add('from-customer')
        if is_from_partner:
            labels.add('from-partner')
        if labels:
            labels_list = ','.join(labels)
        else:
            labels_list = None
        params = purge_none({
            'uuid': uuid,
            'md5': md5,
            'sha1': sha1,
            'min_score': min_score,
            'max_score': max_score,
            'force': force and 1 or 0,
            'summary': summary,
            'labels': labels_list,
        })
        return self._api_request(url, params, raw=raw, post=True)

    # pylint: disable=W0613
    # raw, query_end, query_start are unused
    def get_license_activity(self, query_start=None, query_end=None,
                             raw=False):
        """
        Fetch license activity information.

        DEPRECATED. DO NOT USE
        """
        assert False, "Call to deprecated API function"
    # pylint: enable=W0613

    def get_detections(self, report_uuid, raw=False):
        """
        Retrieve full internal scoring details. Requires special permissions

        :param report_uuid: Backend-report UUID as returned by `get_result`
        :returns: Dictionary with detailed detection information
        """
        url = self.__build_url('research', [ 'get_detections' ])
        params = { 'report_uuid': report_uuid }
        return self._api_request(url, params, raw=raw, post=True)

    def get_backend_scores(self, md5=None, sha1=None, raw=False):
        """
        Download detailed detection information for all backend results for a
        file.

        :param md5: MD5 of the file to query
        :param sha1: SHA1 of the file to query
        :returns: Dictionary with detailed detection information
        """
        assert md5 or sha1, "Need to provide one of md5/sha1"
        url = self.__build_url('research', [ 'get_backend_scores' ])
        params = purge_none({
            'file_md5': md5,
            'file_sha1': sha1,
        })
        return self._api_request(url, params, raw=raw, post=True)


class AnalysisClient(AnalysisClientBase):
    """
    Client for the Analysis API.

    A client for the Analysis API that accesses the API through the web,
    using key and api token for authentication, and the python
    requests module for sending requests.

    :param base_url: URL where the lastline analysis API is located. (required)
    :param key: API key for the Lastline Analyst API (required)
    :param api_token: API token for the Lastline Analyst API (required)
    :param logger: if provided, should be a python logging.Logger object
        or object with similar interface.
    :param ca_bundle: if provided, location of Certification Authority bundle
        to use for authentication. This should not be required
        if certificates are properly setup on the system.
    :param verify_ssl: if True, verify SSL certificates. This overrides the
        per-call parameter
    :param proxies: dictionay with per-protocol proxy to use to use
        (e.g. { 'http': 'localhost:3128', 'https': 'localhost:3128' }
    :param timeout: default timeout (in seconds) to use for network requests.
        Set to None to disable timeouts
    """
    def __init__(self,
                 base_url,
                 key,
                 api_token,
                 logger=None,
                 ca_bundle=None,
                 verify_ssl=True,
                 use_curl=False,
                 timeout=60,
                 proxies=None,
                 config=None):
        AnalysisClientBase.__init__(self, base_url, logger, config)
        self.__key = key
        self.__api_token = api_token
        self.__ca_bundle = ca_bundle
        self.__verify_ssl = verify_ssl
        self.__logger = logger
        self.__timeout = timeout
        if use_curl and logger:
            logger.warning("Ingoring deprecated use_curl option")
        if proxies is None and config:
            self.__proxies = get_proxies_from_config(config)
        else:
            self.__proxies = proxies
        self.__session = requests.session()

    def set_key(self, key):
        self.__key = key

    def _api_request(self,
                     url,
                     params=None,
                     files=None,
                     timeout=None,
                     post=False,
                     raw=False,
                     requested_format="json",
                     verify=True):
        if self._logger():
            self._logger().info("Requesting %s" % url)
        if requested_format.lower() != "json":
            raw = True
        if not params:
            params = {}
        params["key"] = self.__key
        # NOTE: certain functions allow access without an api-token. Then,
        # a valid license-key is sufficient. We must not pass an invalid
        # or empty, however
        if self.__api_token:
            params["api_token"] = self.__api_token
        if self.REQUEST_PERFDATA:
            # we allow anyone setting this flag, but only admins will get
            # any data back
            params['perfdata'] = 1

        method = "GET"
        data = None
        if post or files:
            method = "POST"
            data = params
            params = None

        if not self.__verify_ssl or not verify:
            verify_ca_bundle = False
        elif self.__ca_bundle:
            verify_ca_bundle = self.__ca_bundle
        else:
            verify_ca_bundle = True

        try:
            response = self.__session.\
                request(method, url,
                        params=params, data=data, files=files,
                        timeout=timeout or self.__timeout,
                        verify=verify_ca_bundle,
                        proxies=self.__proxies)
            # raise if anything went wrong
            response.raise_for_status()
        except requests.RequestException, exc:
            if self.__logger:
                self.__logger.error("Error contacting Malscape API: %s", exc)
            # raise a wrapped exception
            raise CommunicationError(error=exc)

        # Get the response content, as a unicode string if the response is
        # textual, as a regular string otherwise.
        content_type = response.headers.get("content-type")
        if content_type and \
                (content_type.startswith("application/json") or
                 content_type.startswith("text/")):
            data = response.text
        else:
            data = response.content

        return self._process_response_page(data, raw, requested_format)


def init_shell(banner):
    """Set up the iPython shell."""
    try:
        #this import can fail, that's why it's in a try block!
        #pylint: disable=E0611
        #pylint: disable=F0401
        from IPython.frontend.terminal.embed import InteractiveShellEmbed #@UnresolvedImport
        #pylint: enable=E0611
        #pylint: enable=F0401
        shell = InteractiveShellEmbed(banner1=banner)
    except ImportError: # iPython < 0.11
        # iPython <0.11 does have a Shell member
        shell = IPython.Shell.IPShellEmbed() #pylint: disable=E1101
        shell.set_banner(banner)

    return shell


BANNER = """
--------------------------------------
Lastline Analyst API shell
--------------------------------------

The 'analysis' object is an AnalysisClient,
which can be used to access the functionality
of the lastline Analysis API.

This is an IPython shell, so you can take
advantage of tab auto-completion and other
convenient features of IPython.
"""
URL = "https://analysis.lastline.com"
def main(argv):
    parser = optparse.OptionParser(usage="""
Run client for analysis api with the provided credentials

    %prog access_key api_token

""")
    parser.add_option("-u", "--api-url", dest="api_url",
        type="string", default=URL,
        help="send API requests to this URL (debugging purposes)")

    (cmdline_options, args) = parser.parse_args(argv[1:])
    if len(args) != 2:
        parser.print_help()
        return 1

    namespace = {}
    namespace["analysis"] = AnalysisClient(cmdline_options.api_url,
                                           key=args[0],
                                           api_token=args[1])

    shell = init_shell(BANNER)
    shell(local_ns=namespace, global_ns=namespace)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
