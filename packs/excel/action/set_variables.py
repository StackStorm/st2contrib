import json
from lib import ExcelAction, ExcelReader

class GetExcelVariablesAction(ExcelAction):
    def __init__(self, config):
        super(GetExcelVariablesAction, self).__init__(config)

    def run(self, sheet, key, variables, strict):
        data = json.loads(variables)
        excel = ExcelReader(self._excel_file, sheet,
                                          key_column=self._key_column,
                                          variable_name_row=self._variable_name_row,
                                          strict=strict,lock=True)
        excel.set_values_for_variables(key, data)
        excel.save()
        return (True, 'Success')
