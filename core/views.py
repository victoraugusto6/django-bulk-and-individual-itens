import csv
import logging
from io import TextIOWrapper
from time import time

from core.models import Pessoa
from django.db import IntegrityError
from more_itertools import batched


def read_csv_file(file):
    file_wrapper = TextIOWrapper(file, encoding="utf-8")

    csv_reader = csv.reader(file_wrapper, delimiter=",")
    header = next(csv_reader)
    return [dict(zip(header, row)) for row in csv_reader]


def import_csv_file(file, qtd_itens_batched):
    start_time = time()

    data = read_csv_file(file)
    chunks = batched(data, max(len(data) // qtd_itens_batched, 1))

    for batch in chunks:
        try:
            instace_pessoas = [
                Pessoa(
                    nome=item.get("nome"),
                    sobrenome=item.get("sobrenome"),
                    cpf=item.get("cpf"),
                    idade=item.get("idade"),
                )
                for item in batch
            ]
            Pessoa.objects.bulk_create(instace_pessoas)
        except (IntegrityError, ValueError):
            for instance in instace_pessoas:
                try:
                    instance.save()
                except (IntegrityError, ValueError):
                    logging.error(
                        f"Error for {instance.nome} {instance.sobrenome} - {instance.cpf}"
                    )
                    continue

    end_time = time()
    elapsed_time_minutes = (end_time - start_time) / 60.0
    logging.info(f"Import took {elapsed_time_minutes:.2f} minutes")


def import_individual_csv_file(file):
    start_time = time()

    data = read_csv_file(file)
    instace_pessoas = [
        Pessoa(
            nome=item.get("nome"),
            sobrenome=item.get("sobrenome"),
            cpf=item.get("cpf"),
            idade=item.get("idade"),
        )
        for item in data
    ]
    for instance in instace_pessoas:
        try:
            instance.save()
        except (IntegrityError, ValueError):
            continue

    end_time = time()
    elapsed_time_minutes = (end_time - start_time) / 60.0
    logging.info(f"Import took {elapsed_time_minutes:.2f} minutes")
