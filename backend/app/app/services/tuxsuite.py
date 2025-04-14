import tuxsuite

def run_tuxsuite_tests(kernel_url: str, modules_url: str, tests: list[str], device: str):
    params = {
        "device": device,
        "kernel": kernel_url,
        "tests": tests,
        "modules": modules_url
    }
    test = tuxsuite.Test(**params)
    test.test()
    # TODO: obtain and return uuid
