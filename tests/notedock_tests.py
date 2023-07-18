import inspect
import logging
import sys
import unittest
from datetime import date
from shutil import rmtree

sys.path.append('..')
from notedock.notedock import *
from notedock.helpers import create_dir, remove_file

create_dir('../logs')
create_dir('../logs/Tests')
logs_path = f'../logs/Tests/{date.today()}.log'

remove_file(logs_path)
logger.enable_logger('Notedock Tests', logs_path, logging.DEBUG)


def log_test(test_name: str):
    logger.logger.info(f'--- Running test {test_name} ---')


class NotedockTest(unittest.TestCase):

    def setUp(self) -> None:
        self.notes = load_workspace('tests')

    def tearDown(self) -> None:
        logger.logger.info(f'--- Stopped test ---\n')
        rmtree('workspaces')

    def test_duplicate_name_validation(self) -> None:
        log_test(inspect.currentframe().f_code.co_name)

        d = {}
        d[get_valid_name(d, 'A')] = {}
        d[get_valid_name(d, 'A')] = {}
        self.assertTrue(len(d) == 2)

    def test_adding_notebook(self) -> None:
        log_test(inspect.currentframe().f_code.co_name)

        add_notebook('Test Notebook')
        self.assertIn('Test Notebook', self.notes)

    def test_renaming_notebook(self) -> None:
        log_test(inspect.currentframe().f_code.co_name)

        add_notebook('Test Notebook')
        add_note('Test Notebook', 'New Note', 'Some content')
        notes_copy = self.notes['Test Notebook'].copy()
        rename_notebook('Test Notebook', 'New Notebook')
        self.assertIn('New Notebook', self.notes)
        self.assertEqual(notes_copy, self.notes['New Notebook'])

    def test_deleting_notebook(self) -> None:
        log_test(inspect.currentframe().f_code.co_name)

        add_notebook('Test Notebook')
        delete_notebook('Test Notebook')
        self.assertNotIn('Test Notebook', self.notes)

    def test_adding_note(self) -> None:
        log_test(inspect.currentframe().f_code.co_name)

        add_notebook('Test Notebook')
        add_note('Test Notebook', 'New Note', 'Some Content')
        self.assertIn('New Note', self.notes['Test Notebook'])

    def test_editing_note(self) -> None:
        log_test(inspect.currentframe().f_code.co_name)

        add_notebook('Test Notebook')
        add_note('Test Notebook', 'Test Note', 'Some Content')
        original_content = self.notes['Test Notebook']['Test Note']
        edit_note('Test Notebook', 'Test Note', 'New Note', original_content)
        self.assertNotIn('Test Note', self.notes)
        self.assertIn('New Note', self.notes['Test Notebook'])
        self.assertEqual(original_content, self.notes['Test Notebook']['New Note'])
        edit_note('Test Notebook', 'New Note', 'New Note', 'Some Other Content')
        self.assertNotEqual(original_content, self.notes['Test Notebook']['New Note'])

    def test_deleting_note(self) -> None:
        log_test(inspect.currentframe().f_code.co_name)

        add_notebook('Test Notebook')
        add_note('Test Notebook', 'Test Note', 'Test Content')
        delete_note('Test Notebook', 'Test Note')
        self.assertNotIn('Test Note', self.notes['Test Notebook'])