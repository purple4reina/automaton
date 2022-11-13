import pytest

from automaton.handlers import LambdaHandler, AutomatonComponentRunError

def test_lambda_handler___call___passes(mock_enabled_component,
        mock_disabled_component):
    handler = LambdaHandler(config_file=None)
    handler.components = [mock_enabled_component, mock_disabled_component]
    handler()
    assert mock_enabled_component.run_called == 1, (
            'enabled component.run not called once')
    assert not mock_disabled_component.run_called, 'disabled component.run called'

def test_lambda_handler___call___fails_once(mock_once_failing_component):
    handler = LambdaHandler(config_file=None)
    handler.components = [mock_once_failing_component]
    handler()
    assert mock_once_failing_component.run_called == 2, (
            'enabled component.run not called two times')

def test_lambda_handler___call___fails_thrice(mock_thrice_failing_component):
    handler = LambdaHandler(config_file=None)
    handler.components = [mock_thrice_failing_component]

    try:
        handler()
    except AutomatonComponentRunError:
        assert mock_thrice_failing_component.run_called == 3, (
                'enabled component.run not called three times')
    else:
        raise AssertionError('should have raised AutomatonComponentRunError')
