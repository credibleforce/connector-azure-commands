"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

from az.cli import az
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('azure-commands')


def list_vm(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"vm list {_command_reformat('--resource-group', params.get('resource_group'))}"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)
        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_vm(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"vm show {_command_reformat('--ids', params.get('id'))} {_command_reformat('--resource-group', params.get('resource_group'))}"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_vm(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"vm delete {_command_reformat('--ids', params.get('id'))} {_command_reformat('--resource-group', params.get('resource_group'))} --yes"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def list_resource(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"resource list {_command_reformat('--location', params.get('location'))}"
        query = _handle_optional_params(params, query)
        exit_code, result_dict, logs = az(query)
        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_resource(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"resource show {_command_reformat('--ids', params.get('id'))} {_command_reformat('--resource-group', params.get('resource_group'))} {_command_reformat('--resource-type', params.get('resource_type'))} {_command_reformat('--name', params.get('name'))}"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_resource(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"resource delete {_command_reformat('--ids', params.get('id'))} {_command_reformat('--resource-group', params.get('resource_group'))} --yes"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def generic_command(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = params.get('command')
        query = _handle_optional_params(params, query)
        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def list_webapp(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"webapp list {_command_reformat('--resource-group', params.get('resource_group'))}"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def list_ssh_keys(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"sshkey list {_command_reformat('--resource-group', params.get('resource_group'))}"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def list_storage_fs_directory(config: dict, params: dict):
    try:
        params = _build_payload_and_authenticate(config, params)

        query = f"storage fs directory list {_command_reformat('--file-system', params.get('file_system'))}"
        query = _handle_optional_params(params, query)

        exit_code, result_dict, logs = az(query)

        if exit_code == 0:
            return result_dict
        raise ConnectorError(str(logs))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def _login_az_cli(config: dict):
    try:
        query = f"login --service-principal -u {config.get('client_id')} -p {config.get('client_secret')} --tenant {config.get('tenant_id')}"
        exit_code, result_dict, logs = az(query)
        if exit_code == 0:
            return result_dict, True
        else:
            raise ConnectorError("Invalid Credentials")
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def _check_if_right_user(config: dict) -> bool:
    try:
        exit_code, result_dict, logs = az("account show")
        # On 0 (SUCCESS) check result_dict if its same as client secret, otherwise return false
        if exit_code == 0:
            # Check if client_id currently logged in is equal to current configuration
            if config.get('client_id') == result_dict.get('user').get('name'):
                return True
            else:
                # If current client_id is not equal to current configuration, Run once the login.
                return _login_az_cli(config)[1]
        return False
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def _build_payload_and_authenticate(config: dict, params: dict) -> dict:
    if not _check_if_right_user(config):
        raise ConnectorError(f"Wrong/Someone else's User credentials for {config.get('client_id')}")

    return {key: val for key, val in params.items() if val is not None and val != ''}


def _command_reformat(command_name: str, command_value: str) -> str:
    return f"{command_name} {command_value}" if (command_value != '' and command_value is not None) else ""


def _handle_optional_params(params: dict, query: str) -> str:
    if params.get('optional_parameters') is not None:
        query = f"{query} {params.get('optional_parameters')}"
    logger.info(f"Query Executing is: {query}")
    return query


operations = {
    "list_vm": list_vm,
    "get_vm": get_vm,
    "delete_vm": delete_vm,
    "list_resource": list_resource,
    "get_resource": get_resource,
    "delete_resource": delete_resource,
    "generic_command": generic_command,
    "list_webapp": list_webapp,
    "list_ssh_keys": list_ssh_keys,
    "list_storage_fs_directory": list_storage_fs_directory
}