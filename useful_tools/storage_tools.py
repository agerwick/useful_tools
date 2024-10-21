import psutil
from .disk_uuid import get_disk_uuid

def get_logical_device_info():
    """
    Get information about logical disk drives.
    """
    disk_info = {}
    for partition in psutil.disk_partitions():
        device = partition.device
        if device in disk_info:
            device += "_1"
        disk_info[device] = {
            'mountpoint': partition.mountpoint,
            'fstype': partition.fstype,
            'opts': partition.opts,
            'device_uuid': get_disk_uuid(partition.mountpoint),
            'storage_total': psutil.disk_usage(partition.mountpoint).total,
            'storage_free': psutil.disk_usage(partition.mountpoint).free,
            'storage_used': psutil.disk_usage(partition.mountpoint).used,
            'storage_used_percent': psutil.disk_usage(partition.mountpoint).percent,
        }
    return disk_info

def get_physical_device_info():
    """
    Get information about physical disk drives.
    The numbers here are reset when the system is restarted.
    """
    disk_io_counters = psutil.disk_io_counters(perdisk=True)
    """ example output:
    {'PhysicalDrive0': sdiskio(read_count=6616502, write_count=4992928, read_bytes=257992072192, write_bytes=142347117056, read_time=3293, write_time=1003), 'PhysicalDrive1': sdiskio(read_count=96, write_count=9, read_bytes=498688, write_bytes=160768, read_time=6, write_time=0)}
    """
    # convert to dict
    physical_disk_info = {disk: dict(counters._asdict()) for disk, counters in disk_io_counters.items()}
    return physical_disk_info
