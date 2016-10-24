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

from lib import ExcelAction, ExcelReader
import sys, json

class GetExcelVariablesAction(ExcelAction):
    def __init__(self, config):
        super(GetExcelVariablesAction, self).__init__(config)

    def run(self, excel_key, sheet='Sheet1', variables='[]'):
        excel = ExcelReader(self._excel_file, sheet_name=sheet, 
                                          key_column=self._key_column,
                                          variable_name_row=self._variable_name_row,
                                          strict=True)
        vfk = excel.get_variables_for_key(excel_key)
        if variables == '[]':  # default
            return vfk
        variables = json.loads(variables)
        filtered = {}
        for v in variables:
            if v in vfk:
                filtered[v]=vfk[v]
        return filtered
