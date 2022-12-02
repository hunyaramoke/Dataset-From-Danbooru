import launch

if not launch.is_installed("selenium"):
    launch.run_pip("install selenium")
if not launch.is_installed("requests"):
    launch.run_pip("install requests")
if not launch.is_installed("BeautifulSoup4"):
    launch.run_pip("install BeautifulSoup4")