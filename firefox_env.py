from webdriver_manager.firefox import GeckoDriverManager

driver_location = GeckoDriverManager().install()
with open(".env.local", "w+") as f:
    print(f'export FIREFOX_DRIVER="{driver_location}"', file=f)