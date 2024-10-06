import re 


class tee_OfN_Analyze:
    dataTypes = {"int", "float", "double", "char", "bool", "void"}

    count_Statement = 0
    cnting_Statement = True
    
    # def __init__(self):
        
    def line_type_checker(self, line):
        self.check_statements(line)
        
    def is_statement(self, line):
        operators = {"=", ">>", "<<", "+=", "++" "--","<", ">"}
        return any(op in line for op in operators)
    
    def countTeeStatement(self, line):
        operators = r'(?<!\w)(?:>>|<<|[=+\-*/%&|^<>!]+)(?!\w)'  # Matches operators while ignoring negative signs in numbers
        # Find all matches of operators
        matches = re.findall(operators, line)
        # Count the number of matches
        return len(matches)

    def scan_condition(self,line):
        line = line.replace("if", "").replace("{", "").replace("(", "").replace(")", "").strip()
        self.count_Statement += self.countTeeStatement(line)
        
    def one_if_block(self, line):
        if "{" in line:
            line = line.strip("}")
            line_split = line.split("{")
            if line_split:
                condition = line_split.pop(0)
                self.scan_condition(condition)
                # print("if statements:")
                if line_split:
                    line =line_split[0]
                    self.line_type_checker(line)
        
        else:
            line_split = line.split(")")
            if line_split:
                self.scan_condition(line_split[0] + ")")
                # print("")
                line = line_split[1]
                self.line_type_checker(line)
    
    def check_statements(self, line):
        Statements = []
        
        split_line = [part.strip() for part in line.split(";") if part.strip()]         # split and strip lines between ;
        Statements = [stmt.strip() for line in split_line for stmt in line.split(",") if stmt.strip()]      # split and strip lines between , in split_line list
        Statements = [statement for statement in Statements if self.is_statement(statement)]
        
        for statement in Statements:
            for dataType in self.dataTypes:
                if dataType in statement:
                    statement = statement.replace(dataType, "")
                    break
            
            if "if" not in statement:
                statement = statement.strip()
                self.count_Statement += self.countTeeStatement(statement)
                
            else:
                self.cnting_statement = False
                self.one_if_block(statement)

        

tee_OfN = tee_OfN_Analyze()
num_lines = int(input())
for _ in range(num_lines):
    line = input()
    tee_OfN.line_type_checker(line)
    
print(f"T(n) = {tee_OfN.count_Statement}")
print("")