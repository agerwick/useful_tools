import subprocess
import platform

def get_disk_uuid(mountpoint):
    if platform.system() == "Linux":
        output = subprocess.check_output(f"blkid -s UUID -o value {mountpoint}", shell=True)
        return output.strip()
    elif platform.system() == "Windows":
        # if mountpoint has any characters after the first :, strip them to make a simple C: / D: / etc
        mountpoint = mountpoint.split(":")[0] + ":"
        output = subprocess.check_output(f"vol {mountpoint}", shell=True)
        lines = [o.strip() for o in output.decode("utf-8").split("\n") if o]
        vol_name = lines[0].split()[-1]
        vol_serial = lines[1].split()[-1]
        # as Windows doesn't provide a proper UUID like blkid does, we'll use the volume serial number and volume name
        return f"{vol_serial}/{vol_name}"
    elif platform.system() == "Darwin":
        output = subprocess.check_output(f"diskutil info {mountpoint} | grep 'Volume UUID'", shell=True)
        return output.strip().split(":")[-1].strip()
    else:
        return None