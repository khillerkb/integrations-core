import pytest
import os
import subprocess
import requests
import time
import logging
import mock

import common

log = logging.getLogger('test_haproxy')


@pytest.fixture
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator


@pytest.fixture(scope="module")
def haproxy_mock():
    filepath = os.path.join(common.HERE, 'fixtures', 'mock_data')
    with open(filepath, 'r') as f:
        data = f.read()
    p = mock.patch('requests.get', return_value=mock.Mock(content=data))
    yield p.start()
    p.stop()


@pytest.fixture(scope="module")
def haproxy_mock_evil():
    filepath = os.path.join(common.HERE, 'fixtures', 'mock_data_evil')
    with open(filepath, 'r') as f:
        data = f.read()
    p = mock.patch('requests.get', return_value=mock.Mock(content=data))
    yield p.start()
    p.stop()


def wait_for_haproxy():
    for _ in xrange(0, 100):
        res = None
        res_open = None
        try:
            res = requests.get(common.STATUS_URL)
            res.raise_for_status
            res_open = requests.get(common.STATUS_URL_OPEN)
            res_open.raise_for_status
            return
        except Exception as e:
            log.info("exception: {0} res: {1} res_open: {2}".format(e, res, res_open))
            time.sleep(2)
    raise Exception("Cannot start up apache")


@pytest.fixture(scope="session")
def spin_up_haproxy():
    env = os.environ
    env['HAPROXY_CONFIG_DIR'] = os.path.join(common.HERE, 'compose')
    args = [
        "docker-compose",
        "-f", os.path.join(common.HERE, 'compose', 'haproxy.yaml')
    ]
    subprocess.check_call(args + ["up", "-d", "--build"], env=env)
    wait_for_haproxy()
    time.sleep(20)
    yield
    subprocess.check_call(args + ["down"], env=env)