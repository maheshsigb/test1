{
    'name': 'Contact_Travel',
    'version': '1.0',
    'author': 'ESSID Fatima Zahraa',
    'category': 'Custom Modules',
    'license': 'LGPL-3',
    'summary': 'Management of contacts and their travels',
    'description': """
    This module allows you to manage contacts and their travel records.
    You can track travel details and calculate reward levels for contacts.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/travel.xml',
        'views/partner.xml',
        'views/travel_list.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
