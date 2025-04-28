from typing import Literal, Optional
from pydantic import BaseModel

# {'kind': 'test', 
# 'status': {'ap_romfw': None, 'bios': None, 'bl1': None, 'boot': None, 
# 'boot_args': None, 'commands': [], 'device': 'qemu-riscv64', 
# 'download_url': 'https://storage.tuxsuite.com/public/community/camila.alvarez/tests/2vimuB3RRKyuJDj2Yk2YM3zvony/', 
# 'dtb': None, 'duration': 67, 
# finished_time': '2025-04-14T13:16:27.979542', 
# 'fip': None, 'host': 'x86_64', 'is_canceling': False, 
# 'is_public': True, 'job_definition': None,
#  'kernel': 'https://files.kernelci.org/kbuild-gcc-12-riscv-67f82f96b76f1f0f9d83eb3e/Image', 
# 'lab': 'https://lkft.validation.linaro.org', 'lava_test_plans_project': None, 'mcp_fw': None,
# 'mcp_romfw': None, 'modules': None, 'notify_emails': None, 'overlays': [], 'parameters': {}, 'plan': None, 
# 'project': 'community/camila.alvarez', 'provisioning_time': '2025-04-14T13:14:48.701202', 'qemu_image': None, 
# 'result': 'pass', 'results': {'boot': 'pass', 'ltp-smoke': 'pass'}, 'retries': 0, 'retries_messages': [], 
# 'rootfs': None, 'running_time': '2025-04-14T13:15:21.170874', 'scp_fw': None, 'scp_romfw': None, 
# 'setup_duration': 37, 'shared': None, 'state': 'finished', 'test_name': None, 
# 'tests': ['boot', 'ltp-smoke'], 'timeouts': {}, 'token_name': 'RISCV', 'tuxbuild': None,
#  'uefi': None, 'uid': '2vimuB3RRKyuJDj2Yk2YM3zvony', 'user': 'cam.alvarez.i@gmail.com',
# 'user_agent': 'tuxsuite/1.42.2', 'waited_by': [], 'waiting_for': None}}

class TuxSuiteTestStatus(BaseModel):
    tests: list[str]
    download_url: str
    uid: str
    device: str


class TuxSuiteTestRequest(BaseModel):
    kind: Literal['test']
    status: TuxSuiteTestStatus
