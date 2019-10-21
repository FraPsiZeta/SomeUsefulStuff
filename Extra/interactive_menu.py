from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError


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

        self.questions = [
            {
                'type': 'checkbox',
                'qmark': '',
                'message': 'Seleziona i test da effettuare',
                'name': 'tests',
                'choices': [ 
                    Separator('Test Hardware:'),
                    {
                        'name': 'cpu'
                    },
                    {
                        'name' : 'ram'
                    },
                    {
                        'name' : 'hdd' 
                    },
                    {
                        'name' : 'ups' 
                    },
                    Separator('Test Software'),
                    {
                        'name' : 'bios' 
                    },
                    {
                        'name' : 'smartalim_fw' 
                    },
                    {
                        'name' : 'swkit' 
                    },
                    Separator('Test Esterni'),
                    {
                        'name' : 'reset'
                    },
                    {
                        'name' : 'lan' 
                    },
                    {
                        'name' : 'usb' 
                    },
                    {
                        'name' : 'hdmi' 
                    },
                    {
                        'name' : 'serial_usb' 
                    }
                ],
                'validate': lambda answer: 'Scegli almeno un test da effettuare.' \
                    if len(answer) == 0 else True
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
        }
                ]
        
        self.answer = prompt(self.questions, style=self.custom_style_2)
        

# answers = prompt(questions, style=custom_style_2)
# print(answers)
