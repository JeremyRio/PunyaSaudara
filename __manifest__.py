# -*- coding: utf-8 -*-
{
    'name': "Asset",
    'summary': 'Catatan stok aset perusahaan.',
    'description': 'Catatana kuantitas barang, penyewaan barang, dan pengembalian barang dalam stok aset perusahaan.',
    'sequence': -100,
    'author': "Punya Saudara",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/barang_menus.xml',
        'views/barang_trees.xml',
        'views/barang_forms.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [

    ],
    "web.assets_backend": [
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
