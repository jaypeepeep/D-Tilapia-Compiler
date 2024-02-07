from constants import *
from dtilapia import Lexer

class ResParse:
    def __init__(self, line, code, errorName, errorDesc):
        self.line = line
        self.code = code
        self.errorName = errorName
        self.errorDesc = errorDesc
    
    def __repr__(self):
        if self.errorName: return f'{self.line}:{self.code}:{self.errorName}: {self.errorDesc}'
        return f'{self.line}:{self.code}:No Error:No Error'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_token = self.tokens[self.idx]

    def parse(self):
        declarations = []
        if self.current_token.type == TT_KEYWORD and self.current_token.value == "let":
            declaration = self.parse_declaration()
            declarations.append(declaration)
        elif self.current_token.type == TT_KEYWORD and self.current_token.value == "when":
            declaration = self.parse_conditional()
            declarations.append(declaration)
        elif self.current_token.type == TT_KEYWORD and self.current_token.value == "output":
            declaration = self.parse_output()
            declarations.append(declaration)
        else:
            raise Exception("Invalid token at line {}: Expected 'let' keyword".format(self.current_token.line))
        return declarations

    def parse_declaration(self):
        self.advance()  # Move past 'let' keyword
        store = "let" + " "
        identifier_token = self.current_token

        if identifier_token.type == TT_IDENTIFIER:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past identifier
            if self.current_token.type == TT_KEYWORD and self.current_token.value == "be":
                store += str(self.current_token.value) + " "
                self.advance()  # Move past 'be' keyword
                if self.current_token.type == TT_KEYWORD:
                    if self.current_token.value in KEYWORDS_DATA_TYPE:  # Check if the token type is one of the data types
                        store += str(self.current_token.value) + " "
                        data_type = self.current_token.value  # Get the value of the data type token
                        self.advance()
                        if self.current_token.type == TT_PERIOD:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == TT_KEYWORD:
                                if self.current_token.value == 'array':
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_LSQBRAC:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        if self.current_token.type == TT_INT:
                                            size = self.current_token.value
                                            store += str(self.current_token.value) + " "
                                            self.advance()
                                            if self.current_token.type == TT_RSQBRAC:
                                                store += str(self.current_token.value) + " "
                                                self.advance()
                                                if self.current_token.type == TT_ASSIGNMENT:
                                                    store += str(self.current_token.value) + " "
                                                    self.advance()
                                                    if self.current_token.type == TT_LCBRAC:
                                                        store += str(self.current_token.value) + " "
                                                        self.advance()
                                                        if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                            value = [self.current_token.value]
                                                            data_type = self.current_token.type
                                                            store += str(self.current_token.value) + " "
                                                            self.advance()
                                                            if self.current_token.type == TT_RCBRAC:
                                                                store += str(self.current_token.value) + " "
                                                                self.advance()
                                                                return ResParse(self.current_token.line, store, "No Error", "No Error")
                                                            elif self.current_token.type == TT_COMMA:
                                                                size_allowed = size
                                                                while self.current_token.type == TT_COMMA:
                                                                    store += str(self.current_token.value) + " "
                                                                    self.advance()
                                                                    if self.current_token.type == data_type:
                                                                        value.append(self.current_token.value)
                                                                        store += str(self.current_token.value) + " "
                                                                        self.advance()                
                                                                        size_allowed -= 1                                  
                                                                    else:
                                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                                if size_allowed == 0:
                                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                                elif self.current_token.type == TT_RCBRAC:
                                                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                                                                else:
                                                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                            else:
                                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                        else:
                                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                    else:
                                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                                else:
                                                    return ResParse(self.current_token.line, store, "No Error", "No Error")
                                            else:
                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                        else:
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                        elif self.current_token.value not in KEYWORDS_DATA_TYPE:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                        else:
                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                    elif self.current_token.value == 'set':
                        store += str(self.current_token.value) + " "
                        self.advance()
                        if self.current_token.type == TT_ASSIGNMENT:
                            store += str(self.current_token.value) + " "
                            self.advance()
                            if self.current_token.type == TT_LCBRAC:
                                store += str(self.current_token.value) + " "
                                self.advance()
                                if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                    value = [self.current_token.value]
                                    data_type = [self.current_token.type]
                                    store += str(self.current_token.value) + " "
                                    self.advance()
                                    if self.current_token.type == TT_RCBRAC:
                                        store += str(self.current_token.value) + " "
                                        self.advance()
                                        return ResParse(self.current_token.line, store, "No Error", "No Error")
                                    elif self.current_token.type == TT_COMMA:
                                        while self.current_token.type == TT_COMMA:
                                            store += str(self.current_token.value) + " "
                                            self.advance()
                                            if self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING or self.current_token.type == TT_CHAR or self.current_token.type == TT_COMPL:
                                                value.append(self.current_token.value)
                                                data_type.append(self.current_token.type)
                                                store += str(self.current_token.value) + " "
                                                self.advance()                                           
                                            else:
                                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                        if self.current_token.type == TT_RCBRAC:
                                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                                        else:
                                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                    else:
                                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                                else:
                                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                            else:
                                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")


                        elif self.current_token.type == TT_IDENTIFIER:
                            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                        else:
                            return ResParse(self.current_token.line, store, "No Error", "No Error")
                    else:
                        return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
                else:
                    return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")
        else:
            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ']'.")


## OUTPUT ##
    def parse_output(self):
        self.advance()  # Move past 'OUTPUT' keyword
        store = "output" + " "
        # if self.current_token.type == TT_KEYWORD and self.current_token.value == "output":
        #     self.advance()  # Move past 'output' keyword
        if self.current_token.type == TT_COLON:
            store += str(self.current_token.value) + " "
            self.advance()  # Move past ':'
            if self.current_token.type == TT_IDENTIFIER:
                store += str(self.current_token.value) + " "
                identifier_token = self.current_token
                self.advance()
                return {'type': 'output', 'identifier': identifier_token.value}
            elif self.current_token.type == TT_INT:
                store += str(self.current_token.value) + " "
                int_token = self.current_token
                self.advance()
                return {'type': 'output', 'int': int_token.value}
            elif self.current_token.type == TT_FLOAT:
                store += str(self.current_token.value) + " "
                float_token = self.current_token
                self.advance()
                return {'type': 'output', 'float': float_token.value}
            elif self.current_token.type == TT_STRING:
                store += str(self.current_token.value) + " "
                string_token = self.current_token
                self.advance()
                return {'type': 'output', 'string': string_token.value}
            elif self.current_token.type == TT_CHAR:
                store += str(self.current_token.value) + " "
                char_token = self.current_token
                self.advance()
                return {'type': 'output', 'char': char_token.value}
            elif self.current_token.type == TT_COMPL:
                store += str(self.current_token.value) + " "
                complex_token = self.current_token
                self.advance()
                return {'type': 'output', 'complex': complex_token.value}
            elif self.current_token.type == TT_BOOL:
                store += str(self.current_token.value) + " "
                bool_token = self.current_token
                self.advance()
                return {'type': 'output', 'complex': bool_token.value}
            else:
                return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected an identifier or expression.")
        else:
            return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected ':'.")
    # else:
    #     return ResParse(self.current_token.line, store, f'Invalid token at line {self.current_token.line}', "Expected 'output keyword'.")


# ## CONDITIONAL STATEMENTS ##
#     def parse_conditional(self):
#         if self.current_token.type == TT_KEYWORD and self.current_token.value == "when":
#             self.advance()  # Move past 'when' keyword
#             condition = self.parse_condition()
#             if self.current_token.type == TT_KEYWORD and self.current_token.value == "do":
#                 self.advance()  # Move past 'do' keyword
#                 if self.current_token.type == TT_COLON:
#                     self.advance()
#                     body = self.parse_body()
#                 return {'type': 'when-do', 'condition': condition, 'body': body}
#             else:
#                 raise Exception("Invalid token at line {}: Expected 'do' keyword".format(self.current_token.line))
#         elif self.current_token.type == TT_KEYWORD and self.current_token.value == "when_other":
#             return self.parse_when_other_statement()
#         elif self.current_token.type == TT_KEYWORD and self.current_token.value == "when_multi_other":
#             return self.parse_when_multi_other_statement()
#         else:
#             raise Exception("Invalid token at line {}: Expected 'when', 'when_other', or 'when_multi_other' keyword".format(self.current_token.line))

#     def parse_condition(self):
#         # handling <identifier> <rel_op> <bool_val>
#         identifier_token = self.current_token
#         if identifier_token.type == TT_IDENTIFIER:
#             self.advance()
#             if self.current_token.type in {TT_GREATER_THAN, TT_LESS_THAN, TT_GREATER_THAN_EQUAL, TT_LESS_THAN_EQUAL, TT_EQUAL_TO, TT_NOT_EQUAL_TO}:
#                 rel_op_token = self.current_token
#                 self.advance()
#                 if self.current_token.type == TT_BOOL:
#                     val_token = self.current_token
#                     value_type = 'bool_val'
#                     self.advance()
#                 elif self.current_token.type == TT_INT:
#                     val_token = int(self.current_token.value)
#                     value_type = 'integer'
#                     self.advance()
#                 elif self.current_token.type == TT_IDENTIFIER:
#                     val_token = self.current_token.value
#                     value_type = 'identifier'
#                     self.advance()
#                 else:
#                     raise Exception("Invalid token at line {}: Expected boolean, digit, or identifier value".format(self.current_token.line))
                
#                 # Check for logical operator
#                 if self.current_token.type in {TT_NEGATION, TT_DISJUNCTION, TT_CONJUNCTION, TT_CONDITIONAL, TT_IMPLICATION, TT_BICONDITIONAL}:
#                     logical_op_token = self.current_token
#                     self.advance()
#                 else:
#                     logical_op_token = None
#             else:
#                 raise Exception("Invalid token at line {}: Expected relational operator".format(self.current_token.line))
#         else:
#             raise Exception("Invalid token at line {}: Expected identifier".format(self.current_token.line))
#         return {'identifier': identifier_token.value, 'rel_op': rel_op_token.value, 'value_type': value_type, 'value': val_token, 'logical_op': logical_op_token.value if logical_op_token else None}

#     def parse_body(self):
#         body = ''
################################
#
    def parse_data_type(self):
        data_type = ''
        while self.current_token.type in (TT_IDENTIFIER, TT_PERIOD):
            data_type += self.current_token.value
            self.advance()
        return data_type

def main():
    while True:
        # Take input from the user
        print("Enter your code (type 'exit' to quit):")
        input_text = input()
        
        if input_text.lower() == 'exit':
            print("Exiting...")
            break

        # Generate tokens using the lexer
        lexer = Lexer("dtilapia.py", input_text)
        tokens, error = lexer.make_tokens()

        if error:
            print(error.as_string())
        else:
            # Instantiate the parser with the generated tokens
            parser = Parser(tokens)
            
            try:
                # Parse the tokens and retrieve the declarations
                declarations = parser.parse()
                
                # Print the parsed declarations
                for declaration in declarations:
                    print(declaration)
            except Exception as e:
                print("Parser error:", str(e))


if __name__ == "__main__":
    main()