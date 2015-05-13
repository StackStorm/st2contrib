from st2actions.runners.pythonrunner import Action

from prettytable import PrettyTable

__all__ = [
    'St2ChatOpsFormatListResult'
]


class St2ChatOpsFormatListResult(Action):
    def run(self, result, attributes):
        table = PrettyTable()

        if not result:
            return 'No results.'

        # Add headers
        header = []
        for attribute in attributes:
            name = self._get_header_attribute_name(attribute=attribute)
            header.append(name)
        table.field_names = header

        # Add rows
        for item in result:
            row = []
            for attribute in attributes:
                value = self._get_attribute_value(attribute=attribute, item=item)
                row.append(value)

            table.add_row(row)

        result = table.get_string()
        return result

    def _get_header_attribute_name(self, attribute):
        name = attribute.replace('_', ' ').replace('.', ' ').title()
        return name

    def _get_attribute_value(self, attribute, item):
        if '.' in attribute:
            value = self._get_complex_attribute_value(attribute=attribute, item=item)
        else:
            value = item.get(attribute, None)

        return value

    def _get_complex_attribute_value(self, attribute, item):
        attribute_names = attribute.split('.')

        for index in range(0, (len(attribute_names) - 1)):
            attribute_name = attribute_names[index]
            item = item.get(attribute_name, {})

        attribute_name = attribute_names[-1]
        value = item.get(attribute_name, None)

        return value
