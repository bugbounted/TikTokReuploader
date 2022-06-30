from tiktok import launch_browser, DIR

# launch browser
#launch_browser(f"--profile-directory={DIR}/profile")
driver = launch_browser()

# simply login to the tiktok and you can close the chrome
driver.get("https://www.tiktok.com/login")