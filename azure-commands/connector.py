"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

from connectors.core.connector import Connector, get_logger, ConnectorError

from .operations import operations, _check_if_right_user, _login_az_cli

logger = get_logger('azure-commands')


class AzureCommands(Connector):

    def execute(self, config, operation, params, **kwargs):
        try:
            logger.debug('Executing Action')
            action = operations.get(operation)
            return action(config, params)
        except Exception as err:
            logger.exception(str(err))
            raise ConnectorError(str(err))

    def check_health(self, config):
        try:
            logger.debug(" check_health() executing")
            _login_az_cli(config)
            status = _check_if_right_user(config)
            logger.info("status: check_health() excecuted ")
            return status
        except Exception as err:
            logger.exception(str(err))
            raise ConnectorError(str(err))