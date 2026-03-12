import time
import threading
from typing import Optional
import os


class SnowflakeGenerator:
    """雪花算法ID生成器（单例+线程安全）"""
    _instance = None
    _lock = threading.Lock()

    # 起始时间戳（自定义：2024-01-01 00:00:00）
    START_TIMESTAMP = 1704067200000
    # 机器ID位数（支持1024个节点）
    MACHINE_ID_BITS = 10
    # 序列号位数（每毫秒最多生成4096个ID）
    SEQUENCE_BITS = 12

    # 位移计算
    MACHINE_ID_SHIFT = SEQUENCE_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + MACHINE_ID_BITS

    # 最大值限制
    MAX_MACHINE_ID = (1 << MACHINE_ID_BITS) - 1
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化（从环境变量获取机器ID，适配分布式部署）"""
        if hasattr(self, '_initialized'):
            return

        # 机器ID默认1，可通过环境变量MACHINE_ID设置
        machine_id = int(os.getenv("MACHINE_ID", 1))
        if not 0 <= machine_id <= self.MAX_MACHINE_ID:
            raise ValueError(f"机器ID必须在0-{self.MAX_MACHINE_ID}之间")

        self.machine_id = machine_id
        self.last_timestamp = -1
        self.sequence = 0
        self._lock = threading.Lock()
        self._initialized = True

    def _get_current_timestamp(self) -> int:
        """获取当前毫秒级时间戳"""
        return int(time.time() * 1000)

    def _wait_next_millisecond(self, last_timestamp: int) -> int:
        """等待下一毫秒，处理序列号溢出"""
        timestamp = self._get_current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_current_timestamp()
        return timestamp

    def generate_id(self) -> int:
        """生成雪花ID（核心方法）"""
        with self._lock:
            current_timestamp = self._get_current_timestamp()

            # 处理时钟回拨
            if current_timestamp < self.last_timestamp:
                raise RuntimeError(
                    f"时钟回拨异常！当前时间戳({current_timestamp}) < 上一次时间戳({self.last_timestamp})"
                )

            # 同一毫秒，序列号自增
            if current_timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                # 序列号溢出，等待下一毫秒
                if self.sequence == 0:
                    current_timestamp = self._wait_next_millisecond(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = current_timestamp

            # 拼接雪花ID
            snowflake_id = (
                    ((current_timestamp - self.START_TIMESTAMP) << self.TIMESTAMP_SHIFT)
                    | (self.machine_id << self.MACHINE_ID_SHIFT)
                    | self.sequence
            )
            return snowflake_id


# 全局单例实例
snowflake_generator = SnowflakeGenerator()