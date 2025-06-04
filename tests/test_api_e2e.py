import pytest
from httpx import AsyncClient
from fastapi import status

from api.main import create_app

import os
import sys

import pytest

import asyncio

import nest_asyncio
nest_asyncio.apply()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import logging
logging.basicConfig(level=logging.INFO)

import random
import string

import pytest
from fastapi.testclient import TestClient

app = create_app()

client = TestClient(app)

def test_ascendant_valid():
    response = client.post(
        "/v1/api/horoscope/ascendant",
        json={
            "birth_date": "21 dec 1988",
            "birth_time": "2147",
            "place": "chennai",
            "ayanamsa": "lahiri"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "ascendant" in data or "Ascendant" in data

def test_ascendant_invalid_place():
    response = client.post(
        "/v1/api/horoscope/ascendant",
        json={
            "birth_date": "21 dec 1988",
            "birth_time": "2147",
            "place": "notarealplace123456",
            "ayanamsa": "lahiri"
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "Could not determine coordinates" in data["detail"][0]["msg"]

def test_ascendant_invalid_date():
    response = client.post(
        "/v1/api/horoscope/ascendant",
        json={
            "birth_date": "notadate",
            "birth_time": "2147",
            "place": "chennai",
            "ayanamsa": "lahiri"
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "Invalid birth date format" in data["detail"][0]["msg"]

def test_ascendant_invalid_time():
    response = client.post(
        "/v1/api/horoscope/ascendant",
        json={
            "birth_date": "21 dec 1988",
            "birth_time": "notatime",
            "place": "chennai",
            "ayanamsa": "lahiri"
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "Invalid time format" in data["detail"][0]["msg"] 