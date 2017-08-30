from lib import actions


class SubmitFileHashAction(actions.BaseAction):
    def run(self, md5=None, sha1=None, download_ip=None, download_port=None,
            download_url=None, download_host=None, download_path=None,
            download_agent=None, download_referer=None, download_request=None,
            full_report_score=None, bypass_cache=None, backend=None,
            require_file_analysis=True, mime_type=None, analysis_timeout=None,
            analysis_env=None, allow_network_traffic=None, filename=None,
            keep_file_dumps=None, keep_memory_dumps=None,
            keep_behavior_log=None, push_to_portal_account=None, raw=False,
            verify=True, server_ip=None, server_port=None, server_host=None,
            client_ip=None, client_port=None, is_download=True,
            protocol='http', apk_package_name=None, report_version=None):

        response = self.client.submit_file_hash(md5, sha1, download_ip,
                                                download_port, download_url,
                                                download_host, download_path,
                                                download_agent,
                                                download_referer,
                                                download_request,
                                                full_report_score,
                                                bypass_cache, backend,
                                                require_file_analysis,
                                                mime_type,
                                                analysis_timeout, analysis_env,
                                                allow_network_traffic, filename,
                                                keep_file_dumps,
                                                keep_memory_dumps,
                                                keep_behavior_log,
                                                push_to_portal_account, raw,
                                                verify, server_ip, server_port,
                                                server_host, client_ip,
                                                client_port, is_download,
                                                protocol, apk_package_name,
                                                report_version)

        return response
