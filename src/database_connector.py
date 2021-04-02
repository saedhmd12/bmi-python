from typing import List, Tuple

import mysql.connector


class DatabaseConnector():
	"""A class that connects to the database and reads information from it."""

	def __init__(self):
		"""Connect to the database and get the cursor."""
		self.db = mysql.connector.connect(host='localhost',
											user='root',
											password='',
											database='BMI')
		self.cursor = self.db.cursor()

	def retrieve_table(self) -> List[Tuple]:
		"""Executes SQL and returns the BMI table in the database."""
		self.cursor.execute('create database if not exists BMI')
		self.cursor.execute("""create table if not exists Report (
								Id_Inc int auto_increment, 
								Name varchar(25) not null,
								Weight int,
								Height float,
								B_Date date,
								primary key(Id_Inc))""")
		self.cursor.execute('SELECT * FROM BMI.Report order by id_inc')
		self.table = self.cursor.fetchall()

		return self.table

	def exit_database(self) -> None:
		"""Exits the database and the cursor."""
		self.db.close()
		self.cursor.close()
