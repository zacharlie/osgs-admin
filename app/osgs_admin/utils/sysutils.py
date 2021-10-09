from flask import current_app
import psutil
import os
import subprocess
import statistics
from time import time, sleep

# https://stackoverflow.com/questions/44434838/how-to-run-psutil-inside-a-docker-container


def format_float(value, rounding=2):
    """default formatting operation for establishing a consistent
    representation of floating point and numeric values returned by API."""
    return float("{:.{}f}".format(round(float(value), rounding), rounding))


def get_sys_stats():
    """Get a dictionary of some useful system resource statistics"""
    (totalRAMgb, freeRAMgb, usedRAMgb, usedRAMp, freeRAMp) = get_ram_stats()
    (
        cpu_count,
        cpu_percent,
        cpu_distinct_stats,
        cpu_freq_current_mhz,
        cpu_freq_min_mhz,
        cpu_freq_max_mhz,
    ) = get_cpu_stats()
    (disks, disk_io) = get_disks_stats()
    (nio_rate_total, nio_rate_nic, nio_total, nio_nic) = get_net_stats()
    stats = {
        "time": time(),
        "cpu": {
            "count": cpu_count,
            "percent": {
                "mean": format_float(statistics.mean(cpu_percent)),
                "interval": 0.1,
                "values": cpu_percent,
            },
            "frequency": {
                "ghz": {
                    "current": format_float(cpu_freq_current_mhz / 1000),
                    "min": format_float(cpu_freq_min_mhz / 1000),
                    "max": format_float(cpu_freq_max_mhz / 1000),
                },
                "mhz": {
                    "current": format_float(cpu_freq_current_mhz),
                    "min": format_float(cpu_freq_min_mhz),
                    "max": format_float(cpu_freq_max_mhz),
                },
            },
            "cores": {},
        },
        "ram": {
            "gb": {
                "total": totalRAMgb,
                "available": freeRAMgb,
                "used": usedRAMgb,
            },
            "percent": {
                "used": usedRAMp,
                "free": freeRAMp,
            },
        },
        "diskio": {
            "read_count": format_float(disk_io.read_count),
            "write_count": format_float(disk_io.write_count),
            "read_bytes": format_float(disk_io.read_bytes),
            "write_bytes": format_float(disk_io.write_bytes),
            "read_time": format_float(disk_io.read_time),
            "write_time": format_float(disk_io.write_time),
        },
        "disks": {},
        "network": {
            "bytes_sent": nio_total.bytes_sent,
            "bytes_recv": nio_total.bytes_recv,
            "packets_sent": nio_total.packets_sent,
            "packets_recv": nio_total.packets_recv,
            "errin": nio_total.errin,
            "errout": nio_total.errout,
            "dropin": nio_total.dropin,
            "dropout": nio_total.dropout,
            "adapters": {},
            "rates": {
                "bytes_ps_sent": nio_rate_total.bytes_sent,
                "bytes_ps_recv": nio_rate_total.bytes_recv,
                "adapters": {},
            },
        },
    }

    for cpu_core in cpu_distinct_stats:
        core_stats = cpu_distinct_stats[cpu_core]
        stats["cpu"]["cores"][cpu_core] = {}
        stats["cpu"]["cores"][cpu_core]["percent"] = {}
        stats_key = stats["cpu"]["cores"][cpu_core]["percent"]
        stats_key["mean"] = format_float(statistics.mean(core_stats))
        stats_key["interval"] = 0.1
        stats_key["values"] = core_stats

    checked_devices = []

    for disk in disks:
        if not disks[disk]["device"] in checked_devices:
            stats["disks"][disk] = disks[disk]
            del stats["disks"][disk]["mount"]
            checked_devices.append(disks[disk]["device"])

    for nic in nio_nic:
        nic_io = nio_nic[nic]
        nic_io_stats = {
            "bytes_sent": nic_io.bytes_sent,
            "bytes_recv": nic_io.bytes_recv,
            "packets_sent": nic_io.packets_sent,
            "packets_recv": nic_io.packets_recv,
            "errin": nic_io.errin,
            "errout": nic_io.errout,
            "dropin": nic_io.dropin,
            "dropout": nic_io.dropout,
        }
        stats["network"]["adapters"][nic] = nic_io_stats

    for nic in nio_rate_nic:
        nic_rate_io = nio_rate_nic[nic]
        nic_rate_stats = {
            "bytes_ps_sent": nic_rate_io.bytes_sent,
            "bytes_ps_recv": nic_rate_io.bytes_recv,
        }
        stats["network"]["rates"]["adapters"][nic] = nic_rate_stats

    current_app.logger.warn(f"stats collected: {stats}")

    return stats


def get_cpu_stats():
    cpu_count = psutil.cpu_count()
    # sampling interval can be useful at 0.5 seconds to prevent spikes
    # Getting numerous shorter samples is useful when post-processing
    cpu_percent = [
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
        psutil.cpu_percent(interval=0.1),
    ]
    cpu_percents = [
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
        psutil.cpu_percent(interval=0.1, percpu=True),
    ]
    cpu_distinct_stats = {}
    usage_lists = [list(x) for x in zip(*cpu_percents)]
    for idx, stats_list in enumerate(usage_lists):
        core_id = idx + 1
        cpu_distinct_stats[core_id] = stats_list
    cpu_freq_current_mhz = psutil.cpu_freq().current
    cpu_freq_min_mhz = psutil.cpu_freq().min
    cpu_freq_max_mhz = psutil.cpu_freq().max
    return (
        cpu_count,
        cpu_percent,
        cpu_distinct_stats,
        cpu_freq_current_mhz,
        cpu_freq_min_mhz,
        cpu_freq_max_mhz,
    )


def get_ram_stats():
    # various stats as object
    RAMstats = psutil.virtual_memory()
    # converted to a dictionary
    # RAMstats = dict(psutil.virtual_memory()._asdict())
    # bytes => kb => mb => gb == 1024*1024*1024
    totalRAMgb = round(RAMstats.total / 1024 ** 3)
    freeRAMgb = round(RAMstats.available / 1024 ** 3)
    usedRAMgb = round(RAMstats.used / 1024 ** 3)
    # percentage of RAM in use
    usedRAMp = round(psutil.virtual_memory().percent, 1)
    # percentage of available memory
    freeRAMp = round(
        psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 1
    )
    return (totalRAMgb, freeRAMgb, usedRAMgb, usedRAMp, freeRAMp)


def get_disks_stats():
    # on windows we need to run diskperf before diskio counters
    if os.name == "nt":
        subprocess.run(
            [
                "cmd",
                "/k",
                "diskperf -y",
            ],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        ).stdout
    disk_io = psutil.disk_io_counters()
    # disks_io = psutil.disk_io_counters(perdisk=True)

    disks = {}
    for i, disk in enumerate(psutil.disk_partitions(all=False), start=1):
        # for io in disks_io:
        #     if io.id == disks[disk].mount:
        #         disks[disk]["io"] = io
        usage = psutil.disk_usage(disk.mountpoint)

        disks[i] = {
            "device": disk.device,
            "mount": disk.mountpoint,
            "total": round(usage.total / 1024 ** 3),
            "used": round(usage.used / 1024 ** 3),
            "free": round(usage.free / 1024 ** 3),
            "percent": round(usage.percent / 1024 ** 3),
        }

    # partitions = []
    # for i, partition in enumerate(psutil.disk_partitions(all=True), start=1):
    #     partitions.append(
    #         {"id": i, "device": partition.device, "mount": partition.mountpoint}
    #     )

    return (disks, disk_io)


def get_net_stats():
    nio_rate_total, nio_rate_nic = poll_net_io(1)
    nio_total = psutil.net_io_counters()
    nio_nic = psutil.net_io_counters(pernic=True)
    return (nio_rate_total, nio_rate_nic, nio_total, nio_nic)


def poll_net_io(interval):
    """Diff nic stats to get usage rate (e.g kb/s)"""
    from collections import namedtuple

    nicIO = namedtuple(
        "nicIO",
        "bytes_sent bytes_recv packets_sent packets_recv errin errout dropin dropout",
    )
    pre_nio_total = psutil.net_io_counters()
    pre_nio_nic = psutil.net_io_counters(pernic=True)
    sleep(interval)
    post_nio_total = psutil.net_io_counters()
    nio_rate_total = tuple(
        map(lambda i, j: i - j, tuple(post_nio_total), tuple(pre_nio_total))
    )
    current_app.logger.warn(f"{nio_rate_total}")
    nio_rate_total = nicIO(*nio_rate_total)
    post_nio_nic = psutil.net_io_counters(pernic=True)
    nio_rate_nic = {}
    # current_app.logger.warn(f"pre_nio_nic: {pre_nio_nic}")
    # current_app.logger.warn(f"post_nio_nic: {post_nio_nic}")
    for key, val in pre_nio_nic.items():
        v = post_nio_nic[key]
        nic_rate = tuple(map(lambda i, j: i - j, tuple(v), tuple(val)))
        nio_rate_nic[key] = nicIO(*nic_rate)
    return nio_rate_total, nio_rate_nic


def bytes2human(n):
    # https://psutil.readthedocs.io/en/latest/index.html#recipes
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n
