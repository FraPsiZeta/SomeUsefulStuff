from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError


class Menu:
    def __init__(self, device_tests):
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


        self.questions1 = [
            {
                'type': 'list',
                'qmark': '⋄',
                'name': 'devices',
                'message': 'Seleziona il dispositivo da collaudare:',
                'choices': [
                    'MEDIA3N_SERVER',
                    'OBOE',
                ],
            }
            ]

        
        #Dopo aver selezionato il device, queste righe successive definiscono le liste di test per quel dispositiv0
        self.answer = prompt(self.questions1, style=self.custom_style_2)
        self.hardware_tests = [{'name' : t} for t in device_tests[self.answer['devices']]['hardware']] 
        self.software_tests = [{'name' : t} for t in device_tests[self.answer['devices']]['software']] 
        self.esterno_test = [{'name' : t} for t in device_tests[self.answer['devices']]['esterno']] 


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
                'name': 'part_number',
                'message': 'Inserire il Part Number del dispositivo:',
            }
                ]
        self.answer2 = prompt(self.questions2, style=self.custom_style_2)
        self.answer.update(self.answer2)
        

# answers = prompt(questions, style=custom_style_2)
# print(answers)
