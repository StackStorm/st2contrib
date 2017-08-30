"""
Copyright 2016 Brocade Communications Systems, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from lib import excel_action, excel_reader


class GetExcelSheetsAction(excel_action.ExcelAction):
    def run(self, excel_file=None):

        self.replace_defaults(excel_file, None, None)

        excel = excel_reader.ExcelReader(self._excel_file)

        return excel.get_sheets()
