#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, QFileInfo, pyqtSlot, QFile, QMimeDatabase, QMimeType, QVariant
from PyQt5.QtQml import qmlRegisterType, QQmlEngine, QQmlComponent
from PyQt5.QtQuick import QQuickView
from api import Taskhive as TaskhiveAPI

class FileInfo(QObject):
    def __init__(self):
            QObject.__init__(self)
            self._filesize = None

    @pyqtSlot(str, result=int)
    def get_filesize(self, path):
        if path.startswith('file:///'):
            path = path.strip('file:///')
        file = QFileInfo(QFile(path))
        self._filesize = file.size()
        return self._filesize

    @pyqtSlot(str, result=str)
    def get_MIMETYPE(self, path):
        if path.startswith('file:///'):
            path = path.strip('file:///')
        file = QFileInfo(QFile(path))
        db = QMimeDatabase()
        MimeType = db.mimeTypeForFile(file)
        return MimeType.name()

    @pyqtSlot(str, result=str)
    def get_filename(self, path):
        if path.startswith('file:///'):
            path = path.strip('file:///')
        file = QFileInfo(QFile(path))
        return file.fileName()


class TaskhiveAddress(QObject):
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot(result=str)
    def generateAddress(self):
        API.generate_and_store_keys()


class TaskhiveCategories(QObject):
    def __init__(self):
            QObject.__init__(self)

    @pyqtSlot(result=QVariant)
    def getCategories(self):
        categories =  [
                {
                    "name": "Audio / Video", 
                    "sub_categories": [
                        {
                            "name": "Video",
                            "sub_categories": [
                                {
                                    "name":"Recording",
                                    "sub_categories": [
                                        {
                                            "name": "Acting"
                                        },
                                        {
                                            "name": "Footage"
                                        }
                                    ]
                                },
                                {
                                    "name": "Editing"
                                },
                                {
                                    "name": "Rendering"
                                },
                                {
                                    "name": "Animation"
                                }
                            ]
                        },
                        {
                            "name": "Audio",
                            "sub_categories": [
                                {
                                    "name": "Editing & Mastering"
                                },
                                {
                                    "name": "Voiceovers / Acting"
                                },
                                {
                                    "name": "Composition",
                                    "sub_categories": [
                                        {
                                            "name": "Soundtrack"
                                        },
                                        {
                                            "name": "Jingles"
                                        },
                                        {
                                            "name": "Pop"
                                        },
                                        {
                                            "name": "Jazz"
                                        },
                                        {
                                            "name": "Other"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Graphics",
                    "sub_categories": [
                        {
                            "name": "2D",
                            "sub_categories": [
                                {
                                    "name": "Design",
                                    "sub_categories": [
                                        {
                                            "name": "Characters"
                                        },
                                        {
                                            "name": "Enviroments"
                                        },
                                        {
                                            "name": "Clothing (Fashion)"
                                        }
                                    ]
                                },
                                {
                                    "name": "Photography"
                                },
                                {
                                    "name": "Editing",
                                    "sub_categories": [
                                        {
                                            "name": "Photograpy Retouching"
                                        }
                                    ]
                                },
                                {
                                    "name": "Illustration",
                                    "sub_categories": [
                                        {
                                            "name": "Digital"
                                        },
                                        {
                                            "name": "Physical Media"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "3D",
                            "sub_categories": [
                                {
                                    "name": "Dead Matter",
                                    "sub_categories": [
                                        {
                                            "name": "Objects"
                                        },
                                        {
                                            "name": "Enviroments",
                                            "sub_categories": [
                                                {
                                                    "name": "Terrain"
                                                },
                                                {
                                                    "name": "Architecture"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        categoriesInfo = {}
        categoriesInfo['depth_level'] = 5
        categoriesInfo['categories'] = categories
        return QVariant(categoriesInfo)

class Taskhive(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)



test_json = '''{
  "task_type":"offer",
  "task_categories":["A1", "C4C1", "F122"],
  "task_title":"Write a short story for my cat blog",
  "task_body":"I have a cat blog that needs a story written for it. I will pay for a story about cats.",
  "task_keywords":[ "cats", "blog", "writing"],
  "task_references":[ "URL1", "URL2"],
  "task_cost":"0.001",
  "task_currency":"BTC",
  "task_payment_rate_type":"task",
  "task_payment_methods":[ "BTC", "DOGE"],
  "task_deadline":1482710400,
  "task_license":"CC BY 4.0",
  "task_escrow_required":1,
  "task_escrow_recommendation":"BITCOIN-PUBKEY",
  "task_address":"TEMP-BM-ADDRESS",
  "task_owner":"BITCOIN-PUBKEY",
  "task_id":"YsBGsF3dc9But9GN5mXOTwEFIZWZ8=",
  "task_entropy":"LATEST-BLOCKCHAIN-HASH",
  "task_expiration":1482710400
  }'''


def main(argv, app):

    engine = QQmlEngine(app)
    engine.quit.connect(app.quit)
    component = QQmlComponent(engine)
    API = TaskhiveAPI()
    BitMessage = API.create_bitmessage_api()
    if BitMessage in ['invalid keys_file settings', 'keyfile does not exist']:
        API.create_settings()
    BitMessageAPI = API.run_bitmessage()
    if API.run_bm.poll() is None:
        print(API.find_running_bitmessage_port())
        print('Bitmessage is running')
        API.generate_and_store_keys()
        API.create_request_json(test_json)

    component.loadUrl(QUrl('UI/main.qml'))
    if component.isReady():
        mainWindow = component.create()
        file = FileInfo()
        categories = TaskhiveCategories()
        context = engine.rootContext()
        context.setContextProperty('FileInfo', file)
        context.setContextProperty('TaskhiveCategories', categories)

    else:
        print(component.errorString())


    sys.exit(app.exec_())

if __name__ == "__main__":
    app = Taskhive(sys.argv)
    main(sys.argv, app)

