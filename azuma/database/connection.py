# Azuma - Discord Bot
# Copyright (C) 2022 VincentRPS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import logging
import os

from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection, management
from dotenv import load_dotenv

from azuma.database.models import guilds

BUNDLE_LOC = os.getcwd() + r'\private\cass-bundle.zip'

if not os.getenv('CLIENT_ID'):
    load_dotenv()

cloud = {'secure_connect_bundle': BUNDLE_LOC}
auth_provider = PlainTextAuthProvider(
    os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET')
)


def connect():
    try:
        if os.getenv('SAFE', 'true') == 'true':
            connection.setup(
                None,
                'azuma',
                cloud=cloud,
                auth_provider=auth_provider,
                connect_timeout=100,
                retry_connect=True,
            )
        else:
            connection.setup(
                None,
                'azuma',
                connect_timeout=100,
                retry_connect=True,
                compression=False,
            )
    except (RuntimeError):
        return
    except:
        connect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    connect()
    management.sync_table(guilds.Guild)
    management.sync_table(guilds.Prefix)
