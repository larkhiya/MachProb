#I am coding here

class StatementAnalyzer: 
    dataTypes = {"int", "float", "double", "char", "bool", "void"}

    def __init__(self):
        self.statement_header = True
        self.if_block = False
        self.for_block = False
        self.for_continued = False
        self.if_single = False
        self.if_statements_ctr = []

    def scan_condition(self, line):
        line = line.replace("if", "").replace("{", "").replace("(", "").replace(")", "").strip()
        print(f"condition: {line}")

    def one_if_block(self, line):
        if "{" in line:
            line = line.strip("}")
            line_split = line.split("{")
            if line_split:
                condition = line_split.pop(0)
                self.scan_condition(condition)
                print("if statements:")
                if line_split:
                    line = line_split[0]
                    self.line_type_checker(line)
        else:
            line_split = line.split(")")
            if line_split:
                self.scan_condition(line_split[0] + ")")
                print("if statements:")
                line = line_split[1]
                self.line_type_checker(line)

    def for_single_loop(self, line):
        clean_line = line.replace("for", "").replace("}", "").replace("(", "").replace(")", "").strip()
        line_split = clean_line.split("{")
        expression = line_split.pop(0)
        expressions = expression.split(";")
        statements = line_split[0]

        self.scan_expressions(expressions)
        print("for statements:")
        line = statements
        self.check_statements(line)

    def scan_expressions(self, expressions):
        labels = {0: "initializer", 1: "condition", 2: "update"}

        for index, expression in enumerate(expressions):
            if index == 0:
                initializer = next((expression.replace(dataType, "") for dataType in self.dataTypes if dataType in expression), expression)
                print(f"{labels[index]}: {initializer.strip()}")
            elif index in labels:
                print(f"{labels[index]}: {expression.strip()}")

    def expression_parser(self, line) -> list:
        line = line.replace("for", "").replace("{", "").replace("(", "").replace(")", "").strip()
        return line.split(";")

    def line_type_checker(self, line):
        if "if" in line and not any(dtype in line for dtype in self.dataTypes):
            self.statement_header = False
            print("if:")
            if "{" in line and "}" in line:
                line = line.replace("}", "")
                self.one_if_block(line)
            else:
                if "{" not in line:
                    self.if_single = True
                self.scan_condition(line)
                print("if statements:")
                self.if_block = True

        elif "else" in line:
            self.statement_header = False
            print("else statements:")

        elif "for" in line:
            self.statement_header = False
            print("for:")
            if "{" in line and "}" in line:
                self.for_single_loop(line)
            else:
                self.scan_expressions(self.expression_parser(line))
                print("for statements:")
            self.for_block = True

        elif "}" in line and "if" not in line:
            self.statement_header = True
            if self.for_block and not self.if_block:
                self.for_block = False
            elif not self.for_block and self.if_block:
                self.if_block = False
            elif self.for_block and self.if_block:
                self.if_block = False
                self.statement_header = False
                self.for_continued = True

        else:
            if self.statement_header:
                print("statements:")
            if self.for_continued:
                print("for statements continued:")
            if "}" in line:
                line = line.replace("}", "")
            self.check_statements(line)

    def is_statement(self, statement):
        operators = {"=", ">>", "<<", "+=", "++", "--"}
        return any(op in statement for op in operators)

    def check_statements(self, line):
        Statements = []

        split_line = [part.strip() for part in line.split(";") if part.strip()]
        Statements = [stmt.strip() for part in split_line for stmt in part.split(",") if stmt.strip()]
        Statements = [statement for statement in Statements if self.is_statement(statement)]

        for statement in Statements:
            for dataType in self.dataTypes:
                if dataType in statement:
                    statement = statement.replace(dataType, "")
                    break
            if "if" not in statement:
                print(statement.strip())
            else:
                self.statement_header = False
                line = statement
                print("if:")
                self.one_if_block(line)

        self.statement_header = False
        self.for_continued = False

        if self.if_single:
            self.statement_header = True
            self.if_single = False



analyzer = StatementAnalyzer()
num_lines = int(input())
for _ in range(num_lines):
    line = input()
    analyzer.line_type_checker(line)
