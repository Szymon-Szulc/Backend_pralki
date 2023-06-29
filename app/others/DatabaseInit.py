from datetime import datetime

from flask_restful import Resource
from ..Data import Problems
from ..Data import Mongo
from ..common import get_message, get_api_key


class DB_init(Resource):
    def post(self, token):
        if token != get_api_key():
            print(token)
            return get_message("błędny token"), 403
        languages = ["pl", "en", "ua"]
        machines = [
            {
                "DevName": "Pralka 1, Virtual Akademik Kalisz",
                "Data": {
                    "id": 0,
                    "model": "xiaomi"
                },
                "Flags": {
                    "turn_on": False,
                    "lock": False,
                    "type": 0,
                    "broken": False
                },
                "TuyaData": {
                    "ip": "10.0.0.2",
                    "localKey": "VirtualLocalKey1",
                    "id": "VirtualDeviceID1",
                },
            },
            {
                "DevName": "Pralka 2, Virtual Akademik Kalisz",
                "Data": {
                    "id": 1,
                    "model": "samsung"
                },
                "Flags": {
                    "turn_on": False,
                    "lock": False,
                    "type": 0,
                    "broken": False
                },
                "TuyaData": {
                    "ip": "10.0.0.3",
                    "localKey": "VirtualLocalKey2",
                    "id": "VirtualDeviceID2",
                },
            },
            {
                "DevName": "Suszarka 1, Virtual Akademik Kalisz",
                "Data": {
                    "id": 2,
                    "model": "xiaomi"
                },
                "Flags": {
                    "turn_on": False,
                    "lock": False,
                    "type": 1,
                    "broken": False
                },
                "TuyaData": {
                    "ip": "10.0.0.4",
                    "localKey": "VirtualLocalKey3",
                    "id": "VirtualDeviceID3",
                },
            },
            {
                "DevName": "Suszarka 2, Virtual Akademik Kalisz",
                "Data": {
                    "id": 3,
                    "model": "samsung"
                },
                "Flags": {
                    "turn_on": False,
                    "lock": False,
                    "type": 1,
                    "broken": False
                },
                "TuyaData": {
                    "ip": "10.0.0.5",
                    "localKey": "VirtualLocalKey4",
                    "id": "VirtualDeviceID4",
                },
            },
        ]
        dorms = [
            {
                "did": 0,
                "name": "empty",
                "code": "123456",
                "location": "Sosnowiec",
                "Contact": {
                    "number": "000000000",
                    "email": "this_email@dont.exists"
                }
            },
            {
                "did": 1,
                "name": "Virtual Akademik Kalisz",
                "code": "11111",
                "location": "Kalisz",
                "Contact": {
                    "number": "123123123",
                    "email": "kalisz@laundry.pl"
                }
            }
        ]
        notify_table = [
            {
                "date": datetime(2001, 9, 11, 8, 47),
                "uid": 1,
                "machine-number": 1,
                "type": "short_wash",
            },
            {
                "uid": 1,
                "date": datetime(2001, 9, 11, 8, 47),
                "machine-number": 1,
                "type": "short_dry",
            },
            {
                "uid": 1,
                "date": datetime(2001, 9, 11),
                "machine-number": 1,
                "type": "timer_wash"
            },
            {
                "uid": 1,
                "date": datetime(2001, 9, 11),
                "machine-number": 1,
                "type": "timer_dry"
            },
            {
                "uid": 1,
                "date": datetime(2001, 9, 11),
                "machine-number": 1,
                "type": "released_wash"
            },
            {
                "uid": 1,
                "date": datetime(2001, 9, 11),
                "machine-number": 1,
                "type": "released_dry"
            }]
        wash_questions = {
            "pl": [
                {
                    "screens": {
                        "q1": {
                            "header": "Kliknij trzy razy przycisk z numerem pralki i otrzymasz 20 sekund za darmo. (Możesz włączyć tę opcję trzy razy).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy pralka kontynuuje program prania?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Pralka nie zakończyła programu prania. Kup więcej czasu.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Włącz pralkę i sprawdź, czy na wyświetlaczu pralki widnieje czerwona ikona klucza.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy na wyświetlaczu pralki widnieje czerwona ikona klucza?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Poczekaj chwilę, aż pralka odblokuje drzwi.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Naciśnij drzwi pralki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi pralki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Naciśnij drzwi pralki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi pralki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem rozwiązany",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Proszę skontaktować się z zespołem wsparcia",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Prawdopodobnie uchwyt jest uszkodzony. Obejrzyj wideo, jak otworzyć drzwi za pomocą specjalnej metody awaryjnej.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Xiaomi Nie mogę otworzyć drzwiczek pralki",
                    "model": "xiaomi"
                },
                {
                    "screens": {
                        "q1": {
                            "header": "Kliknij trzy razy przycisk z numerem pralki i otrzymasz 20 sekund za darmo. (Możesz włączyć tę opcję trzy razy).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy pralka kontynuuje program prania?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Pralka nie zakończyła programu prania. Kup więcej czasu.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Włącz pralkę i sprawdź, czy na wyświetlaczu pralki widnieje czerwona ikona klucza.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy na wyświetlaczu pralki widnieje czerwona ikona klucza?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Poczekaj chwilę, aż pralka odblokuje drzwi.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Naciśnij drzwi pralki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi pralki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Naciśnij drzwi pralki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi pralki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem rozwiązany",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Proszę skontaktować się z zespołem wsparcia",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Prawdopodobnie uchwyt jest uszkodzony. Obejrzyj wideo, jak otworzyć drzwi za pomocą specjalnej metody awaryjnej.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Samsung nie mogę otworzyć drzwiczek pralki",
                    "model": "samsung"
                }
            ],
            "en": [
                {
                    "screens": {
                        "q1": {
                            "header": "Click the washing machine number button three times and you will get 20 seconds for free. (You can activate this option three times).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Does the washing machine continue the washing program?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "The washing machine did not finish the washing program. Buy more time.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Turn on the washing machine and check if there is a red key icon on the display.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Is there a red key icon on the washing machine display?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Wait for a moment until the washing machine unlocks the door.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Press the washing machine door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the washing machine door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Press the washing machine door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the washing machine door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem solved",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Please contact the support team",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "The handle is likely damaged. Watch the video on how to open the door using the emergency method.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Xiaomi Cannot Open Washing Machine Door",
                    "model": "xiaomi"
                },
                {
                    "screens": {
                        "q1": {
                            "header": "Click the washing machine number button three times and you will get 20 seconds for free. (You can activate this option three times).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Does the washing machine continue the washing program?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "The washing machine did not finish the washing program. Buy more time.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Turn on the washing machine and check if there is a red key icon on the display.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Is there a red key icon on the washing machine display?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Wait for a moment until the washing machine unlocks the door.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Press the washing machine door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the washing machine door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Press the washing machine door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the washing machine door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem solved",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Please contact the support team",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "The handle is likely damaged. Watch the video on how to open the door using the emergency method.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Samsung Cannot Open Washing Machine Door",
                    "model": "samsung"
                }
            ],
            "ua": [
                {
                    "screens": {
                        "q1": {
                            "header": "Натисніть кнопку з номером пральної машини тричі, і отримаєте 20 секунд безкоштовно. (Ви можете скористатись цією опцією тричі).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Пральна машина продовжує програму прання?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Пральна машина не завершила програму прання. Придбайте більше часу.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Увімкніть пральну машину та переконайтеся, що на дисплеї пральної машини відображається червона ікона ключа.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "На дисплеї пральної машини відображається червона ікона ключа?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Зачекайте декілька секунд, поки пральна машина розблокує дверцята.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Натисніть на дверцята пральної машини правою рукою і потягніть за ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята пральної машини?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Натисніть на дверцята пральної машини правою рукою і потягніть за ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята пральної машини?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Проблема вирішена",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Будь ласка, зв'яжіться зі службою підтримки",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Ймовірно, ручка пошкоджена. Перегляньте відео, як відкрити дверцята за допомогою спеціального аварійного методу.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Xiaomi Не можу відкрити дверцята пральної машини",
                    "model": "xiaomi"
                },
                {
                    "screens": {
                        "q1": {
                            "header": "Натисніть кнопку з номером пральної машини тричі, і отримаєте 20 секунд безкоштовно. (Ви можете скористатись цією опцією тричі).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Пральна машина продовжує програму прання?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Пральна машина не завершила програму прання. Придбайте більше часу.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Увімкніть пральну машину та переконайтеся, що на дисплеї пральної машини відображається червона ікона ключа.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "На дисплеї пральної машини відображається червона ікона ключа?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Зачекайте декілька секунд, поки пральна машина розблокує дверцята.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Натисніть на дверцята пральної машини правою рукою і потягніть за ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята пральної машини?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Натисніть на дверцята пральної машини правою рукою і потягніть за ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята пральної машини?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Проблема вирішена",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Будь ласка, зв'яжіться зі службою підтримки",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Ймовірно, ручка пошкоджена. Перегляньте відео, як відкрити дверцята за допомогою спеціального аварійного методу.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Samsung не можу відкрити дверцята пральної машини",
                    "model": "samsung"
                }
            ]
        }
        dry_questions = {
            "pl": [
                {
                    "screens": {
                        "q1": {
                            "header": "Kliknij trzy razy przycisk z numerem suszarki i otrzymasz 20 sekund za darmo. (Możesz włączyć tę opcję trzy razy).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy suszarka kontynuuje program suszenia?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Suszarka nie zakończyła programu prania. Kup więcej czasu.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Włącz suszarkę i sprawdź, czy na wyświetlaczu suszarki widnieje czerwona ikona klucza.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy na wyświetlaczu suszarki widnieje czerwona ikona klucza?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Poczekaj chwilę, aż suszarka odblokuje drzwi.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Naciśnij drzwi suszarki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi suszarki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Naciśnij drzwi suszarki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi suszarki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem rozwiązany",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Proszę skontaktować się z zespołem wsparcia",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Prawdopodobnie uchwyt jest uszkodzony. Obejrzyj wideo, jak otworzyć drzwi za pomocą specjalnej metody awaryjnej.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Xiaomi Nie mogę otworzyć drzwiczek suszarki",
                    "model": "xiaomi"
                },
                {
                    "screens": {
                        "q1": {
                            "header": "Kliknij trzy razy przycisk z numerem suszarki i otrzymasz 20 sekund za darmo. (Możesz włączyć tę opcję trzy razy).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy suszarka kontynuuje program suszenia?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Suszarka nie zakończyła programu prania. Kup więcej czasu.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Włącz suszarkę i sprawdź, czy na wyświetlaczu suszarki widnieje czerwona ikona klucza.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy na wyświetlaczu suszarki widnieje czerwona ikona klucza?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Poczekaj chwilę, aż suszarka odblokuje drzwi.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy to rozwiązało problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Naciśnij drzwi suszarki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi suszarki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Naciśnij drzwi suszarki prawą ręką i pociągnij za uchwyt lewą ręką.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy otworzyłeś drzwi suszarki?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem rozwiązany",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Proszę skontaktować się z zespołem wsparcia",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Prawdopodobnie uchwyt jest uszkodzony. Obejrzyj wideo, jak otworzyć drzwi za pomocą specjalnej metody awaryjnej.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Samsung Nie mogę otworzyć drzwiczek suszarki",
                    "model": "samsung"
                },
            ],
            "en": [
                {
                    "screens": {
                        "q1": {
                            "header": "Click the dryer number button three times and you will receive 20 seconds for free. (You can activate this option three times).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Is the dryer continuing the drying program?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "The dryer did not finish the drying program. Purchase more time.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Turn on the dryer and check if there is a red key icon on the dryer display.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Is there a red key icon on the dryer display?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Wait a moment for the dryer to unlock the door.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Press the dryer door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the dryer door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Press the dryer door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the dryer door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem solved",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Please contact the support team",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "The handle is likely damaged. Watch the video on how to open the door using the emergency method.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Xiaomi Can't open the dryer door",
                    "model": "xiaomi"
                },
                {
                    "screens": {
                        "q1": {
                            "header": "Click the dryer number button three times and you will receive 20 seconds for free. (You can activate this option three times).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Is the dryer continuing the drying program?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "The dryer did not finish the drying program. Purchase more time.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Turn on the dryer and check if there is a red key icon on the dryer display.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Is there a red key icon on the dryer display?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Wait a moment for the dryer to unlock the door.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did this solve the problem?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Press the dryer door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the dryer door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Press the dryer door with your right hand and pull the handle with your left hand.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Did you open the dryer door?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Problem solved",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Please contact the support team",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "The handle is likely damaged. Watch the video on how to open the door using the emergency method.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Samsung Can't open the dryer door",
                    "model": "samsung"
                }
            ],
            "ua": [
                {
                    "screens": {
                        "q1": {
                            "header": "Натисніть кнопку з номером сушарки тричі, і ви отримаєте 20 секунд безкоштовно. (Ви можете активувати цю опцію тричі).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Сушарка продовжує програму сушіння?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Сушарка не закінчила програму сушіння. Придбайте більше часу.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Увімкніть сушарку та перевірте, чи є червона іконка ключа на дисплеї сушарки.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Чи є червона іконка ключа на дисплеї сушарки?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Зачекайте кілька моментів, поки сушарка розблокує двері.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Натисніть дверцята сушарки правою рукою і потягніть ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята сушарки?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Натисніть дверцята сушарки правою рукою і потягніть ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята сушарки?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Проблему вирішено",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Будь ласка, зв'яжіться зі службою підтримки",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Можливо, ручка пошкоджена. Перегляньте відео про те, як відкрити дверцята за допомогою аварійного методу.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Samsung Не можу відкрити дверцята сушарки",
                    "model": "samsung"
                },
                {
                    "screens": {
                        "q1": {
                            "header": "Натисніть кнопку з номером сушарки тричі, і ви отримаєте 20 секунд безкоштовно. (Ви можете активувати цю опцію тричі).",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Сушарка продовжує програму сушіння?",
                            "answers": {
                                "yes": "q2",
                                "no": "q3"
                            }
                        },
                        "q2": {
                            "header": "Сушарка не закінчила програму сушіння. Придбайте більше часу.",
                            "video_link": "https://youtu.be/plleUH4wg40",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "contact"
                            }
                        },
                        "q3": {
                            "header": "Увімкніть сушарку та перевірте, чи є червона іконка ключа на дисплеї сушарки.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Чи є червона іконка ключа на дисплеї сушарки?",
                            "answers": {
                                "yes": "q4",
                                "no": "q5"
                            }
                        },
                        "q4": {
                            "header": "Зачекайте кілька моментів, поки сушарка розблокує двері.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Це вирішило проблему?",
                            "answers": {
                                "yes": "ok",
                                "no": "q6"
                            }
                        },
                        "q5": {
                            "header": "Натисніть дверцята сушарки правою рукою і потягніть ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята сушарки?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        },
                        "q6": {
                            "header": "Натисніть дверцята сушарки правою рукою і потягніть ручку лівою рукою.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Ви відкрили дверцята сушарки?",
                            "answers": {
                                "yes": "ok",
                                "no": "emergency"
                            }
                        }
                    },
                    "solutions": {
                        "ok": {
                            "header": "Проблему вирішено",
                            "video_link": ""
                        },
                        "contact": {
                            "header": "Будь ласка, зв'яжіться зі службою підтримки",
                            "video_link": ""
                        },
                        "emergency": {
                            "header": "Можливо, ручка пошкоджена. Перегляньте відео про те, як відкрити дверцята за допомогою аварійного методу.",
                            "video_link": "https://youtu.be/xvFZjo5PgG0"
                        }
                    },
                    "root": "q1",
                    "name": "Xiaomi Не можу відкрити дверцята сушарки",
                    "model": "xiaomi"
                }
            ],
        }
        payment_questions = {
            "pl": [{
                "screens": {
                    "q1": {
                        "header": "Sprawdź swoje monety",
                        "video_link": "https://youtu.be/xvFZjo5PgG0",
                        "question": "Czy wkładasz odpowiednie monety?",
                        "answers": {
                            "yes": "yes",
                            "no": "no"
                        }
                    }
                },
                "solutions": {
                    "no": {
                        "header": "Problem rozwiązany, włóż prawidłowe ;)",
                        "video_link": ""
                    },
                    "yes": {
                        "header": "Skontaktuj się z nami!",
                        "video_link": ""
                    }
                },
                "root": "q1",
                "name": "Nie przyjmuje monet"
            }],
            "en": [{
                "screens": {
                    "q1": {
                        "header": "Sprawdź swoje monety",
                        "video_link": "https://youtu.be/xvFZjo5PgG0",
                        "question": "Czy wkładasz odpowiednie monety?",
                        "answers": {
                            "yes": "yes",
                            "no": "no"
                        }
                    }
                },
                "solutions": {
                    "no": {
                        "header": "Problem rozwiązany, włóż prawidłowe ;)",
                        "video_link": ""
                    },
                    "yes": {
                        "header": "Skontaktuj się z nami!",
                        "video_link": ""
                    }
                },
                "root": "q1",
                "name": "en Nie przyjmuje monet"
            }],
            "ua": [{
                "screens": {
                    "q1": {
                        "header": "Sprawdź swoje monety",
                        "video_link": "https://youtu.be/xvFZjo5PgG0",
                        "question": "Czy wkładasz odpowiednie monety?",
                        "answers": {
                            "yes": "yes",
                            "no": "no"
                        }
                    }
                },
                "solutions": {
                    "no": {
                        "header": "Problem rozwiązany, włóż prawidłowe ;)",
                        "video_link": ""
                    },
                    "yes": {
                        "header": "Skontaktuj się z nami!",
                        "video_link": ""
                    }
                },
                "root": "q1",
                "name": "ua Nie przyjmuje monet"
            }]
        }
        laundry_questions = {
            "pl": [{
                "screens": {
                    "q1": {
                        "header": "Sprawdź czy na podłodze jest woda",
                        "video_link": "https://youtu.be/xvFZjo5PgG0",
                        "question": "Czy na podłodze jest woda?",
                        "answers": {
                            "yes": "yes",
                            "no": "no"
                        }
                    }
                },
                "solutions": {
                    "no": {
                        "header": "Nie zalało!",
                        "video_link": ""
                    },
                    "yes": {
                        "header": "To nie fajnie ://",
                        "video_link": ""
                    }
                },
                "root": "q1",
                "name": "Pralnie zalało"
            }],
            "en": [{
                "screens": {
                    "q1": {
                        "header": "Sprawdź czy na podłodze jest woda",
                        "video_link": "https://youtu.be/xvFZjo5PgG0",
                        "question": "Czy na podłodze jest woda?",
                        "answers": {
                            "yes": "yes",
                            "no": "no"
                        }
                    }
                },
                "solutions": {
                    "no": {
                        "header": "Nie zalało!",
                        "video_link": ""
                    },
                    "yes": {
                        "header": "To nie fajnie ://",
                        "video_link": ""
                    }
                },
                "root": "q1",
                "name": "en Pralnie zalało"
            }],
            "ua": [{
                "screens": {
                    "q1": {
                        "header": "Sprawdź czy na podłodze jest woda",
                        "video_link": "https://youtu.be/xvFZjo5PgG0",
                        "question": "Czy na podłodze jest woda?",
                        "answers": {
                            "yes": "yes",
                            "no": "no"
                        }
                    }
                },
                "solutions": {
                    "no": {
                        "header": "Nie zalało!",
                        "video_link": ""
                    },
                    "yes": {
                        "header": "To nie fajnie ://",
                        "video_link": ""
                    }
                },
                "root": "q1",
                "name": "ua Pralnie zalało"
            }]
        }
        other_questions = {
            "pl": [{
                    "screens": {
                        "q1": {
                            "header": "Użyj maści na ból dupy",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy użyłeś maści na ból dupy?",
                            "answers": {
                                "yes": "yes",
                                "no": "q2"
                            }
                        },
                        "q2": {
                            "header": "Kup maść na ból dupy",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy użyłeś maści na ból dupy?",
                            "answers": {
                                "yes": "yes",
                                "no": "no"
                            }
                        }
                    },
                    "solutions": {
                        "no": {
                            "header": "Kup ją pod adressem laundry.app/masc_bol_dupy",
                            "video_link": ""
                        },
                        "yes": {
                            "header": "Nie masz bólu dupy!",
                            "video_link": ""
                        }
                    },
                    "root": "q1",
                    "name": "Mam ból dupy"
                }],
            "en": [{
                    "screens": {
                        "q1": {
                            "header": "Użyj maści na ból dupy",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy użyłeś maści na ból dupy?",
                            "answers": {
                                "yes": "yes",
                                "no": "q2"
                            }
                        },
                        "q2": {
                            "header": "Kup maść na ból dupy",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy użyłeś maści na ból dupy?",
                            "answers": {
                                "yes": "yes",
                                "no": "no"
                            }
                        }
                    },
                    "solutions": {
                        "no": {
                            "header": "Kup ją pod adressem laundry.app/masc_bol_dupy",
                            "video_link": ""
                        },
                        "yes": {
                            "header": "Nie masz bólu dupy!",
                            "video_link": ""
                        }
                    },
                    "root": "q1",
                    "name": "EN Mam ból dupy"
                }],
            "ua": [{
                    "screens": {
                        "q1": {
                            "header": "Użyj maści na ból dupy",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy użyłeś maści na ból dupy?",
                            "answers": {
                                "yes": "yes",
                                "no": "q2"
                            }
                        },
                        "q2": {
                            "header": "Kup maść na ból dupy",
                            "video_link": "https://youtu.be/xvFZjo5PgG0",
                            "question": "Czy użyłeś maści na ból dupy?",
                            "answers": {
                                "yes": "yes",
                                "no": "no"
                            }
                        }
                    },
                    "solutions": {
                        "no": {
                            "header": "Kup ją pod adressem laundry.app/masc_bol_dupy",
                            "video_link": ""
                        },
                        "yes": {
                            "header": "Nie masz bólu dupy!",
                            "video_link": ""
                        }
                    },
                    "root": "q1",
                    "name": "UA Mam ból dupy"
                }],
        }
        for lang in languages:
            Problems.delete_many("drying_{}".format(lang), {})
            Problems.delete_many("washing_{}".format(lang), {})
            Problems.delete_many("payment_{}".format(lang), {})
            Problems.delete_many("laundry_{}".format(lang), {})
            Problems.delete_many("other_{}".format(lang), {})
        Mongo.delete_many("users", {})
        Mongo.delete_many("cache_users", {})
        Mongo.delete_many("notify", {})
        Mongo.delete_many("notify_table", {})
        Mongo.delete_many("machines", {})
        Mongo.delete_many("dorms", {})

        for lang in wash_questions:
            for q in wash_questions[lang]:
                Problems.save_obj("washing_{}".format(lang), q)

        for lang in dry_questions:
            for q in dry_questions[lang]:
                Problems.save_obj("drying_{}".format(lang), q)

        for lang in payment_questions:
            for q in payment_questions[lang]:
                Problems.save_obj("payment_{}".format(lang), q)

        for lang in laundry_questions:
            for q in laundry_questions[lang]:
                Problems.save_obj("laundry_{}".format(lang), q)

        for lang in other_questions:
            for q in other_questions[lang]:
                Problems.save_obj("other_{}".format(lang), q)

        dorm_id = ""

        for dorm in dorms:
            dorm_id = Mongo.save_obj("dorms", dorm)

        for machine in machines:
            machine["Data"]["did"] = dorm_id
            Mongo.save_obj("machines", machine)

        for notify in notify_table:
            Mongo.save_obj("notify_table", notify)

        return get_message("Wyczyszczono bazę danych i uzupełnioną ją o przykładowe dane"), 200
