import tuxsuite
import argparse

def run_tuxsuite_tests(kernel_url: str, modules_url: str | None, tests: list[str], device: str) -> str:
    params = {
        "device": device,
        "kernel": kernel_url,
        "tests": tests
    }
    if modules_url is not None:
        params["modules"] = modules_url
    test = tuxsuite.Test(**params)
    test.test()
    uid = test.uid
    return uid

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tuxsuite test from the command line")
    parser.add_argument("--kernel-url", required=True, help="Kernel URL")
    parser.add_argument("--modules-url", default=None, help="Modules URL")
    parser.add_argument("--tests", required=True, action="append", help="Tests to run. Support multiple tests")
    args = parser.parse_args()

    device = "qemu-riscv64"
    test_uid = run_tuxsuite_tests(args.kernel_url, args.modules_url, args.tests, device)
    print(f"Test uid: {test_uid}")
