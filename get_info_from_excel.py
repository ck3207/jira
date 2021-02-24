import xlrd

class GetInfoFromExcel:
    """从excel文档获取bug记录"""
    def __init__(self, filename):
        self.workbook = xlrd.open_workbook(filename=filename)

    def get_data(self, table):
        row, cols = table.nrows, table.ncols
        headers = {}
        data = {}
        for i in range(row):
            for j in range(cols):
                if i == 0:
                   headers.setdefault(j, table.cell(i, j).value)
                else:
                    value = table.cell(i, j).value
                    data.setdefault("{0}-{1}".format(i, j), value)
                # if headers.get(j) == "计划完成日期" and i != 0 :
                #     pass
        return headers, data


if __name__ == "__main__":
    get_info_from_excel = GetInfoFromExcel(filename="config/jira_template.xls")
    table = get_info_from_excel.workbook.sheet_by_name("bugs")


