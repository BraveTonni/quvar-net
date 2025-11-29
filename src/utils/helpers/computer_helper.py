import os
import platform
import getpass
import time

import cpuinfo
import psutil

import socket

import GPUtil

from src.domain.entities.client import ClientInfo, ClientRole


class ComputerHelper:
    @staticmethod
    async def get_client_info() -> ClientInfo:
        local_ip = ComputerHelper.__get_local_ipv4()

        return ClientInfo(
            role=ClientRole.ALL,
            os_info=platform.uname()._asdict(),
            local_ip=local_ip,
            user=getpass.getuser(),
            is_admin=ComputerHelper.__is_admin(),
            cpu=ComputerHelper.__get_cpu(),
            ram_gb=ComputerHelper.__get_ram_gb(),
            gpu=ComputerHelper.__get_gpu(),
            created_at=int(time.time())
        )

    @staticmethod
    def __is_admin() -> bool:
        try:
            if platform.system() == "Windows":
                from ctypes import windll

                return windll.shell32.IsUserAnAdmin() != 0

            return os.getuid() == 0
        except Exception:
            return False

    @staticmethod
    def __get_local_ipv4() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect(("8.8.8.8", 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    @staticmethod
    def __get_cpu() -> str:
        return cpuinfo.get_cpu_info().get(
            "brand_raw", platform.processor() or "Unknown CPU"
        )

    @staticmethod
    def __get_ram_gb() -> float:
        return round(psutil.virtual_memory().total / (1024**3), 2)

    @staticmethod
    def __get_gpu() -> str:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].name

            return "No GPU"
        except Exception:
            return "Unknown GPU"
