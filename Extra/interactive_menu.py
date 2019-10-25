from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
import re


class PartNumberValidator(Validator):
    def validate(self, document):
        ok = re.search('^PS[0-9]{4}-[0-9]{2}$', document.text)
        if ok == None:
            raise ValidationError(
                message='Il Part Number inserito non è corretto. La forma corretta è PSXXXX-XX, dove con X si rappresenta un numero.',
                cursor_position=len(document.text)) # Move cursor to end

class UserNameValidator(Validator):
    def validate(self, document):
        ok = re.search('^[a-z]*\\.[a-z]*$', document.text)
        if ok == None:
            raise ValidationError(
                message='Il nome del collaudatore deve essere della forma "nome.cognome"',
                cursor_position=len(document.text)) # Move cursor to end

class Menu:
    def __init__(self):
        self.custom_style_2 = style_from_dict({
            Token.Separator: '#6C6C6C',
            Token.QuestionMark: '#FF9D00 bold',
            #Token.Selected: '',  # default
            Token.Selected: '#5F819D',
            Token.Pointer: '#FF9D00 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#5F819D bold',
            Token.Question: '',
        })

    def start_menu(self, device_tests, device_names, configurations_name):

        self.questions1 = [
            {
                'type': 'list',
                'qmark': '⋄',
                'name': 'devices',
                'message': 'Seleziona il dispositivo da collaudare:',
                'choices': device_names,
            },
            {
                'type': 'list',
                'qmark': '⋄',
                'name': 'trains',
                'message': 'Seleziona il tipo di treno su cui si installerà il dispositivo:',
                'choices': configurations_name,
            }
            ]

        
        #Dopo aver selezionato il device, queste righe definiscono le liste di test per quel dispositivo
        self.answer = prompt(self.questions1, style=self.custom_style_2)
        try:
            self.hardware_tests = [{'name' : t} for t in device_tests[self.answer['devices']]['hardware']] 
            self.software_tests = [{'name' : t} for t in device_tests[self.answer['devices']]['software']] 
            self.esterno_test = [{'name' : t} for t in device_tests[self.answer['devices']]['esterno']] 
        except:
            pass


        self.questions2 = [
            {
                'type': 'checkbox',
                'qmark': '⋄',
                'message': 'Seleziona i test da effettuare',
                'name': 'tests',
                'choices': [ 
                    Separator('Test Hardware:'),
                    *(self.hardware_tests),
                    Separator('Test Software'),
                    *(self.software_tests),
                    Separator('Test Esterni'),
                    *(self.esterno_test)
                ]
            },
            {
                'type': 'input',
                'qmark': '-',
                'name': 'tester_name',
                'message': 'Inserire il nome del collaudatore:',
                'validate' : UserNameValidator
            },
            {
                'type': 'input',
                'qmark': '-',
                'name': 'test_station',
                'message': 'Inserire la postazione dalla quale si sta eseguendo il collaudo:',
            },
            {
                'type': 'input',
                'qmark': '-',
                'name': 'product_code',
                'message': 'Inserire il codice prodotto:',
            },
            {
                'type': 'input',
                'qmark': '-',
                'name': 'test_number',
                'message': 'Inserire il numero del collaudo:',
            },
            {
                'type': 'input',
                'qmark': '-',
                'name': 'part_number',
                'message': 'Inserire il Part Number del dispositivo:',
                'validate' : PartNumberValidator

            }
                ]
        self.answer2 = prompt(self.questions2, style=self.custom_style_2)
        self.answer.update(self.answer2)
        

# answers = prompt(questions, style=custom_style_2)
# print(answers)
