# disable notify "InsecureRequestWarning: Unverified HTTPS request is being made"
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
