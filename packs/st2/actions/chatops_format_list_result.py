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
            name = attribute.title()
            header.append(name)
        table.field_names = header

        # Add rows
        for item in result:
            row = []
            for attribute in attributes:
                value = item.get(attribute, None)
                row.append(value)

            table.add_row(row)

        result = table.get_string()
        return result
