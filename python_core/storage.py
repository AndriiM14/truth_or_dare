import firebase_admin
from firebase_admin import credentials, db
from python_core.utils import get_scrpaer_uuid, get_firebasedb_url, SingletonMeta
from python_core.consts import FIREBASE_CREDS_PATH
from uuid import uuid4
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class Writable(ABC):
    @abstractmethod
    def to_json(self) -> dict:
        pass


class TruthDareTypes(Enum):
    Original = "original"
    Teen = "teen"
    Party = "party"
    Extreme = "exteme"


@dataclass
class TruthDareEntry(Writable):
    type: TruthDareTypes = TruthDareTypes.Original
    content: str = ""

    def to_json(self) -> dict:
        return {f"{uuid4()}": self.content}


class StorageService(metaclass=SingletonMeta):
    def __init__(self):
        self._creds = credentials.Certificate(FIREBASE_CREDS_PATH)
        firebase_admin.initialize_app(self._creds, {
            "databaseURL": get_firebasedb_url(),
            "databaseAuthVariableOverride": {
                "uid": get_scrpaer_uuid()
            }
        })

        self._truth_ref = db.reference("/truth")
        self._dares_ref = db .reference("/dares")

    def _update(self, item: Writable, ref) -> None:
        try:
            ref.update(item.to_json())
        except Exception as e:
            print("Coudn't update db")
            print(e)

    def add_truth(self, truth: TruthDareEntry) -> None:
        subtype_ref = self._truth_ref.child(truth.type.value)
        self._update(truth, subtype_ref)

    def add_dare(self, dare: TruthDareEntry) -> None:
        subtype_ref = self._dares_ref.child(dare.type.value)
        self._update(dare, subtype_ref)
